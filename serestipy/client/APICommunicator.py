#!/usr/bin/env  python3
#@file   APICommunicator.py
#
#@date   Feb 9, 2022
#@author Patrick Eschenbach
#@copyright \n
# This file is part of the program SeRESTiPy.\n\n
# SeRESTiPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.\n\n
# SeRESTiPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.\n\n
# You should have received a copy of the GNU Lesser General
# Public License along with SeRESTiPy.
# If not, see <http://www.gnu.org/licenses/>.\n

import requests
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import serestipy.client.JsonHelper as jh
from serestipy.client.Singleton import Singleton

@Singleton
class APICommunicator():
    def __processResponse(self, response, host_address, resource_id, debug):
        response.raise_for_status()
        if (debug):
            return response.json(), host_address, resource_id
        else:
            return [response.json()]

    def __postRequest(self, host_address, resource_id, json_data, debug):
        session = requests.Session()
        session.trust_env = False
        response = session.post(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response, host_address, resource_id, debug)

    def __putRequest(self, host_address, resource_id, json_data, debug):
        session = requests.Session()
        session.trust_env = False
        response = session.put(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response, host_address, resource_id, debug)

    def __patchRequest(self, host_address, resource_id, json_data, debug):
        session = requests.Session()
        session.trust_env = False
        response = session.patch(host_address + "/api/" + str(resource_id), json=jh.dict2json(json_data))
        return self.__processResponse(response, host_address, resource_id, debug)

    def __getRequest(self, host_address, resource_id, json_data, debug):
        session = requests.Session()
        session.trust_env = False
        response = session.get(host_address + "/api/" + str(resource_id), json = json_data)
        return self.__processResponse(response, host_address, resource_id, debug)

    def __deleteRequest(self, host_address, resource_id, json_data, debug):
        session = requests.Session()
        session.trust_env = False
        response = session.delete(host_address + "/api/" + str(resource_id))
        return self.__processResponse(response, host_address, resource_id, debug)

    async def __asyncRequestWrapper(self, request_type, hosts_list, resource_id_list, debug, json_data_list=['{}']):
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
            print("Invalid HTTP request type! Allowed: POST, PUT, PATCH, GET, DELETE")
        with ThreadPoolExecutor(max_workers=int(len(hosts_list))) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    method,
                    *(hosts_list[iTask], resource_id_list[iTask], json_data_list[iTask], debug)
                )
                for iTask in range(len(hosts_list))
            ]
            for val in await asyncio.gather(*tasks):
                if (debug):
                    print(val)
                if (isinstance(val[0],dict) or isinstance(val[0],list)):
                    return_values.append(val[0].copy())
                else:
                    return_values.append(val[0])
        return return_values

    def requestEvent(self, request_type, hosts_list, resource_id_list=[''], json_data_list=['{}'], debug = False):
        if (json_data_list == ['{}'] and len(hosts_list) > 1):
            json_data_list = ['{}' for i in range(len(hosts_list))] 
        if (resource_id_list == [''] and len(hosts_list) > 1):
            resource_id_list = ['' for i in range(len(hosts_list))]
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self.__asyncRequestWrapper(request_type, hosts_list, resource_id_list, debug, json_data_list))
        return loop.run_until_complete(future)

    def endpointsOnline(self, hosts_list, debug = False):
        while(True):
            ans = []
            try:
                ans = self.requestEvent("GET", hosts_list, debug = debug)
            except:
                pass
            if (all(element == {'STATE: ': 'ONLINE'} for element in ans)):
                break
            time.sleep(1.0)

    def resourcesFinished(self, hosts_list, resource_id_list, debug = False):
        while(True):
            ans = []
            try:
                ans = self.requestEvent("GET", hosts_list, resource_id_list, debug = debug)
            except:
                pass            
            if (all(element == {'STATE: ': 'IDLE'} for element in ans)):
                break
            time.sleep(5.0)
