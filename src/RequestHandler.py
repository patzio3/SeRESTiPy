import requests
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

    def getJob(self):
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id))
        self.__response = getResponse.json()

    def patchJob(self, requestJson):
        checker = jc.JobFormatChecker(requestJson)
        checker.run()
        _ = requests.patch(self.__host + "/api/" + str(self.__job_id), json = requestJson)

    def getJobInfo(self):
        getResponse = requests.get(self.__host + "/api/" + str(self.__job_id) + "/info")
        return getResponse.json()

    def deleteJob(self):
        _ = requests.delete(self.__host + "/api/" + str(self.__job_id))

    def getResponseContent(self):
        return self.__response
