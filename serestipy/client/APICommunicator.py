import os
import requests
import time
from multiprocessing import Process
import asyncio
import serestipy.client.JsonHelper as jh
from concurrent.futures import ThreadPoolExecutor


class APICommunicator():
    def __postRequest(self, host_address, resource_id, json_data):
        return requests.post(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))

    def __getRequest(self, host_address, resource_id, json_data):
        return (requests.get(host_address + "/api/" + str(resource_id))).json()

    def __deleteRequest(self, host_address, resource_id, json_data):
        return requests.delete(host_address + "/api/" + str(resource_id))

    async def __asyncRequestWrapper(self, request_type, hosts_list, resource_id_list, json_data_list=['{}']):
        return_values = []
        switcher = {
            "POST": self.__postRequest,
            "GET": self.__getRequest,
            "DELETE": self.__deleteRequest
        }
        method = switcher.get(request_type.upper(),
                              "Invalid HTTP request type!")
        with ThreadPoolExecutor(max_workers=int(len(hosts_list))) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    method,
                    *(hosts_list[iTask], resource_id_list[iTask], json_data_list[iTask])
                )
                for iTask in range(len(hosts_list))
            ]
            for val in await asyncio.gather(*tasks):
                return_values.append(val)
        return return_values

    def requestEvent(self, request_type, hosts_list, resource_id_list, json_data_list=['{}']):
        if (json_data_list == ['{}'] and len(hosts_list) > 1):
            json_data_list = ['{}' for i in range(len(hosts_list))]
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self.__asyncRequestWrapper(request_type, hosts_list, resource_id_list, json_data_list))
        return loop.run_until_complete(future)

    def apiEndpointsOnline(self, hosts_list):
        while(True):
            ans = self.requestEvent("GET", hosts_list, [
                                    "" for i in range(len(hosts_list))])
            if (all(element == {'STATE: ': 'ONLINE'} for element in ans)):
                break
            time.sleep(1.0)

    def resourcesFinished(self, hosts_list, resource_id_list):
        while(True):
            ans = self.requestEvent("GET", hosts_list, resource_id_list)
            if (all(element == {'STATE: ': 'IDLE'} for element in ans)):
                break
            #time.sleep(5.0)
