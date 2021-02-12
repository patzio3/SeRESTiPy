import requests
import JsonResolver as jr

class RequestHandler():
    def __init__(self, requestJson, host, activeSystemID):
        self.__reqForm = requestJson
        self.__host = host
        self.__actId = activeSystemID
        self.__results = {}

    def postRequest(self):
        _ = requests.post(self.__host + "api/"+str(self.__actId), json = self.__reqForm)

    def getRequest(self):
        getResponse = requests.get(self.__host + "api/"+str(self.__actId))
        self.__results[self.__actId] = getResponse.json()

    def deleteRequest(self):
        _ = requests.delete(self.__host + "api/"+str(self.__actId))

    def getResults(self):
        return self.__results[self.__actId]