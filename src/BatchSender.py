import asyncio
from concurrent.futures import ThreadPoolExecutor
import RequestHandler as rh

class BatchSender():
    def __init__(self, wholeSettings, hosts, activeSystemID):
        self.__settings = wholeSettings
        self.__hosts = hosts
        self.__actIds = activeSystemID

    def sendPostRequestWithSettings(self, wholeSettings, host, activeSystemID):
        handler = rh.RequestHandler()
        handler.postRequest()

    async def sendBatchAsync(self):
        with ThreadPoolExecutor(max_workers = int(len(self.__settings.items()) - 1)) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    sendPostRequestWithSettings,
                    *(wholeSettings, activeSystemID[iSystem], slaveHosts[iSystem])
                )
                for iSystem in range(len(wholeSettings.items()) - 1)
            ]
            for response in await asyncio.gather(*tasks):
                pass