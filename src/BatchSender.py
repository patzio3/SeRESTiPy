import asyncio
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import RequestHandler as rh

def runInParallel(fns):
    proc = []
    for fn in fns:
        p = Process(target = fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def runInParallelAsync(fns):
    proc = []
    for fn in fns:
        p = Process(target = fn)
        p.start()

class BatchSender():
    def __init__(self, hosts, job_ids, nJobs):
        if (len(hosts) < nJobs):
            print("WARNING: You are sending more jobs than you have specified hosts. You are going to run some jobs on the same host!")
        self.__nJobs = nJobs
        self.__responses = []
        self.__reqHandlers = []
        for iJob in range(self.__nJobs):
            self.__reqHandlers.append(rh.RequestHandler(hosts[iJob], job_ids[iJob]))

    def batchPost(self, jsons):
        runInParallelAsync([self.__reqHandlers[iJob].postJob(jsons[iJob]) for iJob in range(self.__nJobs)])

    def batchGet(self):
        runInParallel([self.__reqHandlers[iJob].getJob() for iJob in range(self.__nJobs)])
        runInParallel([self.__responses.append(self.__reqHandlers[iJob].getResposeContent()) for iJob in range(self.__nJobs)])

    def batchDelete(self):
        runInParallel([self.__reqHandlers[iJob].deleteJob() for iJob in range(self.__nJobs)])

    # async def sendJobs(self, jsons):
    #     with ThreadPoolExecutor(max_workers = self.__nJobs) as executor:
    #         loop = asyncio.get_event_loop()
    #         tasks = [
    #             loop.run_in_executor(
    #                 executor,
    #                 self.batchPost,
    #                 *(jsons[iJob], iJob)
    #             )
    #             for iJob in range(self.__nJobs)
    #         ]
    #         for response in await asyncio.gather(*tasks):
    #             pass
