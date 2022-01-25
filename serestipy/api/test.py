import os

import serestipy.client.JsonHelper as jh
import serestipy.client.APICommunicator as comm
import serestipy.api.TaskHandler as th

json = jh.input2json(os.path.join(os.getcwd(), "/WORK/p_esch01/progs/restApi/serestipy/inp_faty"))[0]

communicator = comm.APICommunicator()

communicator.requestEvent("POST", ["http://128.176.214.100:5000/"], [0], [json])
communicator.resourcesFinished(["http://128.176.214.100:5000/"], [0])
communicator.requestEvent("DELETE", ["http://128.176.214.100:5000/"], [0], [json])

# print(jh.dismemberJson(json)[0],"\n\n")
# print(jh.dismemberJson(json)[1],"\n\n")
# print(jh.dismemberJson(json)[2],"\n\n")
# print(jh.dismemberJson(json)[3],"\n\n")

# task = th.TaskHandler(json)
# task.enroll({},1)
# print("HERE ARE THE SETTINGS",task.getSettings().embedding.naddXCFunc)

# task.perform({},1)
# print("HERE ARE THE SETTINGS",task.getSettings().embedding.naddXCFunc)