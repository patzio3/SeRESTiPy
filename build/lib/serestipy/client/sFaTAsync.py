import os
import sys
import time
import json
import JsonHelper as jh
import APICommunicator as comm
import akcluster


def perform(hosts_list, json_data):
    communicator = comm.APICommunicator()
    taskIDs = [0]
    start = time.time()
    communicator.requestEvent("POST", hosts_list, taskIDs, [json_data])
    communicator.resourcesFinished(hosts_list, taskIDs)
    end = time.time()
    print("Time taken for run: ", end - start, "s")
    # clean-up
    _ = communicator.requestEvent("DELETE", hosts_list, taskIDs)


if __name__ == "__main__":
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc"
    print("Reading input and preparing calculation...")
    json = jh.input2json(os.path.join(os.getcwd(), sys.argv[1]))[0]
    nSystems = len(list(jh.find("NAME", json)))
    cluster = akcluster.AKCluster()
    nCPU, nRAM, nNodes, nWorkerPerNode = cluster.determineSettings(nSystems, sys.argv[4], int(sys.argv[2]), int(sys.argv[3]))
    cluster.run(perform, nCPU, nRAM, 1, 1, sys.argv[4], 4 , json)
