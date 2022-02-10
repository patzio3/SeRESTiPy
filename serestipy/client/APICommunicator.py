import os
import requests
import time
from multiprocessing import Process
import asyncio
import serestipy.client.JsonHelper as jh
from concurrent.futures import ThreadPoolExecutor
from serestipy.client.Singleton import Singleton

@Singleton
class APICommunicator():
    def __processResponse(self, response):
        response.raise_for_status()
        return response.json()

    def __postRequest(self, host_address, resource_id, json_data):
        session = requests.Session()
        session.trust_env = False
        response = session.post(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response)

    def __putRequest(self, host_address, resource_id, json_data):
        session = requests.Session()
        session.trust_env = False
        response = session.put(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response)

    def __patchRequest(self, host_address, resource_id, json_data):
        session = requests.Session()
        session.trust_env = False
        response = session.patch(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response)

    def __getRequest(self, host_address, resource_id, json_data):
        session = requests.Session()
        session.trust_env = False
        response = session.get(host_address + "/api/" + str(resource_id), json = json_data)
        return self.__processResponse(response)

    def __deleteRequest(self, host_address, resource_id, json_data):
        session = requests.Session()
        session.trust_env = False
        response = session.delete(host_address + "/api/" + str(resource_id))
        return self.__processResponse(response)

    async def __asyncRequestWrapper(self, request_type, hosts_list, resource_id_list, json_data_list=['{}']):
        return_values = []
        switcher = {
            "POST": self.__postRequest,
            "GET": self.__getRequest,
            "DELETE": self.__deleteRequest,
            "PATCH": self.__patchRequest,
            "PUT": self.__putRequest
        }
        try:
            method = switcher[request_type.upper()]
        except KeyError:
            raise KeyError("Invalid HTTP request type! Allowed: POST, PUT, PATCH, GET, DELETE")
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
                if (isinstance(val,dict) or isinstance(val,list)):
                    return_values.append(val.copy())
                else:
                    return_values.append(val)
        return return_values

    def requestEvent(self, request_type, hosts_list, resource_id_list=[''], json_data_list=['{}']):
        if (json_data_list == ['{}'] and len(hosts_list) > 1):
            json_data_list = ['{}' for i in range(len(hosts_list))] 
        if (resource_id_list == [''] and len(hosts_list) > 1):
            resource_id_list = ['' for i in range(len(hosts_list))]
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self.__asyncRequestWrapper(request_type, hosts_list, resource_id_list, json_data_list))
        return loop.run_until_complete(future)

    def endpointsOnline(self, hosts_list):
        while(True):
            ans = []
            try:
                ans = self.requestEvent("GET", hosts_list)
            except:
                pass
            if (all(element == {'STATE: ': 'ONLINE'} for element in ans)):
                break
            time.sleep(1.0)

    def resourcesFinished(self, hosts_list, resource_id_list):
        while(True):
            ans = []
            try:
                ans = self.requestEvent("GET", hosts_list, resource_id_list)
            except:
                pass            
            if (all(element == {'STATE: ': 'IDLE'} for element in ans)):
                break
