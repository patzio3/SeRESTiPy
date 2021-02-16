import requests, os
import JobFormatChecker as jc

class RequestHandler():
    def __init__(self, host, job_id):
        self.__host = host
        self.__job_id = job_id
        self.__response = ""

    def postJob(self, requestJson):
        checker = jc.JobFormatChecker(requestJson)
        checker.run()
        _ = requests.post(self.__host + "/api/" + str(self.__job_id), json = requestJson)
        # return status

    def getJob(self):
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id))
        self.__response = getResponse.json()

    def getJobInfo(self):
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id) + "/info")
        return getResponse.json()

    def deleteJob(self):
        status = requests.delete(self.__host + "/api/" + str(self.__job_id))

    def getResponseContent(self):
        return self.__response
