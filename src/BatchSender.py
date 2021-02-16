import concurrent.futures
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


class BatchSender():
    def __init__(self, hosts, job_ids, nJobs):
        if (len(hosts) < nJobs):
            print("WARNING: You are sending more jobs than you have specified hosts. You are going to run some jobs on the same host!")
        self.__nJobs = nJobs
        self.__responses = []
        self.__reqHandlers = []
        for iJob in range(self.__nJobs):
            self.__reqHandlers.append(rh.RequestHandler(hosts[iJob], job_ids[iJob]))

    def getRequestHandler(self, iJob):
        return self.__reqHandlers[iJob]

    def batchPost(self, json, iJob):
        _ = self.__reqHandlers[iJob].postJob(json)

    def batchGet(self, iJob):
        _ = self.__reqHandlers[iJob].getJob()
        return self.__responses.append(self.__reqHandlers[iJob].getResponseContent())

    def sendJobs(self, jsons):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__nJobs) as executor:
            future_to_job = {executor.submit(self.batchPost, jsons[iJob], iJob): iJob for iJob in range(self.__nJobs)}
            for future in concurrent.futures.as_completed(future_to_job):
                iJob = future_to_job[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (iJob, exc))

    def getJobs(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__nJobs) as executor:
            future_to_job = {executor.submit(self.batchGet, iJob): iJob for iJob in range(self.__nJobs)}
            for future in concurrent.futures.as_completed(future_to_job):
                iJob = future_to_job[future]
                try:
                    data = future.result()
                    return data
                except Exception as exc:
                    print('%r generated an exception: %s' % (iJob, exc))

    def deleteJobs(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__nJobs) as executor:
            future_to_job = {executor.submit(self.__reqHandlers[iJob].deleteJob, iJob): iJob for iJob in range(self.__nJobs)}
            for future in concurrent.futures.as_completed(future_to_job):
                iJob = future_to_job[future]
                try:
                    _ = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (iJob, exc))