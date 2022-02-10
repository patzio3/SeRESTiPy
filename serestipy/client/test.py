from serestipy.client.APICommunicator import APICommunicator
import serestipy.client.JsonHelper as jh

communicator = APICommunicator.getInstance()

ip = "http://128.176.214.100"
port = 5000

json = jh.input2json("/WORK/p_esch01/serenitypaper/waterfde/calc/002.xyz/inp")
json["ACT"]["SYS0"]["BASIS"]["LABEL"] = "def2-tzVp"
json["ENV"]["SYS1"]["BASIS"]["LABEL"] = "def2-tzVp"
json["TASK"] = "fDe"
# jsonTwo = json.copy()
# jsonTwo["ID"] = 69
r = communicator.requestEvent("post", [ip+":"+str(port)], [69], [json])
print(r)
communicator.resourcesFinished([ip+":"+str(port)], [69])
r = communicator.requestEvent("delete", [ip+":"+str(port)], [69], [json])
print(r)