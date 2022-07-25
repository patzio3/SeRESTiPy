import os
import sys
import time
import json
import errno
import shutil as sh
import serestipy.client.JsonHelper as jh
from serestipy.client.APICommunicator import APICommunicator
import serestipy.client.akcluster


def bundleResults(ids, localLoadPath, systemnames):
    os.mkdir(localLoadPath)
    def copyanything(src, dst):
        try:
            sh.copytree(src, dst)
        except OSError as exc:
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                sh.copy(src, dst)
            else:
                raise
    for i in range(len(ids)):
        dst = os.path.join(localLoadPath, systemnames[i])
        src = os.path.join(os.getenv('DATABASE_DIR'), str(ids[i]), systemnames[i])
        copyanything(src, dst)

def perform(hosts_list, json_data):
    communicator = APICommunicator.getInstance()
    taskIDs = [i for i in range(len(json_data))]
    systemnames = list(jh.find("NAME", json_data[0]))
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
    
    bundleResults(taskIDs[1:], "/WORK/p_esch01/scratch_calc/test/LOAD", systemnames)
    os.chdir("/WORK/p_esch01/scratch_calc/test/LOAD")
    systemString = ""
    for item in systemnames:
        systemString += item + " "
    os.system("python /scratch/p_esch01/programs/serenity/tools/couple.py "+str(len(systemnames))+" "+systemString)
    # clean-up
    _ = communicator.requestEvent("DELETE", [hosts_list[0] for i in range(len(taskIDs))], taskIDs)


if __name__ == "__main__":
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc/test2"
    print("Reading input and preparing calculation...")
    json = jh.input2json(os.path.join(os.getcwd(), sys.argv[1]))
    #nSystems = len(list(jh.find("NAME", json)))
    perform(["http://128.176.214.100:5000"], json)
    # cluster = serestipy.client.akcluster.AKCluster()
    # nCPU, nRAM, nNodes, nWorkerPerNode = cluster.determineSettings(nSystems, sys.argv[4], int(sys.argv[2]), int(sys.argv[3]))
    # # cluster.runInDocker(perform, nCPU, nRAM, 1, 1, sys.argv[4], 4 , json)
    # cluster.runBareMetal(perform, nCPU, nRAM, 1, 1, sys.argv[4], 4 , json)
