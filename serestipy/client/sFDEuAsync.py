import os
import sys
import time
import json
import serestipy.client.JsonHelper as jh
from serestipy.client.APICommunicator import APICommunicator
import serestipy.client.akcluster


def perform(hosts_list, json_data):
    communicator = APICommunicator.getInstance()
    taskIDs = [i for i in range(len(json_data))]
    for iJson, json in enumerate(json_data):
        if (iJson > 0):
            load = os.path.join(os.environ["DATABASE_DIR"], str(taskIDs[0]))
            actSys_list = json["ACT"].keys()
            for sys in actSys_list:
                json["ACT"][sys]["LOAD"] = load
            envSys_list = json["ENV"].keys()
            for sys in envSys_list:
                json["ENV"][sys]["LOAD"] = load
        start = time.time()
        communicator.requestEvent("POST", hosts_list, [taskIDs[iJson]], [json])
        communicator.resourcesFinished(hosts_list, [taskIDs[iJson]])
        end = time.time()
        print("Time taken for run: ", end - start, "s")
    _ = communicator.requestEvent("DELETE", [hosts_list[0] for i in range(len(taskIDs))], taskIDs)


if __name__ == "__main__":
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc/test"
    print("Reading input and preparing calculation...")
    json = jh.input2json(os.path.join(os.getcwd(), sys.argv[1]))
    #nSystems = len(list(jh.find("NAME", json)))
    perform(["http://128.176.214.100:5000"], json)
    # cluster = serestipy.client.akcluster.AKCluster()
    # nCPU, nRAM, nNodes, nWorkerPerNode = cluster.determineSettings(nSystems, sys.argv[4], int(sys.argv[2]), int(sys.argv[3]))
    # # cluster.runInDocker(perform, nCPU, nRAM, 1, 1, sys.argv[4], 4 , json)
    # cluster.runBareMetal(perform, nCPU, nRAM, 1, 1, sys.argv[4], 4 , json)
