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
        status = requests.post(self.__host + "/api/" + str(self.__job_id), json = requestJson)
        return status

    def getJob(self):
        print(self.__host + "/api/" + str(self.__job_id))
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id))
        self.__response = getResponse.json()

    def getJobInfo(self):
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id) + "/info")
        return getResponse.json()

    def deleteJob(self):
        status = requests.delete(self.__host + "/api/" + str(self.__job_id))
        return status

    def getResponseContent(self):
        return self.__response
