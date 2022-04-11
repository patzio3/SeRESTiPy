import os
import sys
import time
import json
import errno
import numpy as np
import shutil as sh
import serestipy.client.JsonHelper as jh
from serestipy.client.APICommunicator import APICommunicator
import serestipy.client.akcluster


def rearrange(wholeSettings, systemNames, oldTaskID, newTaskIDs, iAct, load="/WORK/p_esch01/scratch_calc/test"):
    task, tasksettings, act, env = jh.dismemberJson(wholeSettings)
    allSysSettings = dict(act, **env)
    newDict = {}
    newDict["TASK"] = task
    newDict["TASK_SETTINGS"] = tasksettings
    newDict["ACT"] = {}
    newDict["ENV"] = {}
    allKeys = list(allSysSettings.keys())
    for iSys in range(len(systemNames)):
        if (iSys == iAct):
            newDict["ID"] = str(newTaskIDs[iAct])
            newDict["ACT"][allKeys[0]] = list(jh.find(str(allKeys[iSys]), allSysSettings))[0]
            if (not load == ""):
                newDict["ACT"][allKeys[0]]["LOAD"] = os.path.join(load, str(oldTaskID[iSys]))
        else:
            newDict["ENV"][str(allKeys[iSys])] = list(jh.find(str(allKeys[iSys]), allSysSettings))[0]
            newDict["ENV"][str(allKeys[iSys])]["WRITETODISK"] = False
            if (not load == ""):
                newDict["ENV"][str(allKeys[iSys])]["LOAD"] = os.path.join(load, str(oldTaskID[iSys]))
    return newDict.copy()


def initialscf(wholeSettings, newActName, newTaskId):
    newDict = {}
    _, _, act, env = jh.dismemberJson(wholeSettings)
    if (list(jh.find("NAME", act))[0] == newActName):
        newDict["TASK"] = "SCF"
        newDict["ID"] = newTaskId
        newDict["ACT"] = act
        return newDict
    newDict["TASK"] = "SCF"
    newDict["ID"] = newTaskId
    newDict["ACT"] = {}
    _ = list(act.keys())[0]
    for iSys in env.keys():
        sysname = list(jh.find("NAME", env[iSys]))[0]
        if (sysname == newActName):
            newDict["ACT"][str(iSys)] = env[iSys]
    return newDict.copy()


def bundleResults(tasks):
    name = "LOAD"
    ids = []
    systemnames = []
    for i in range(len(tasks)):
        ids.append(str(tasks[i]["ID"]))
        systemnames.append(list(jh.find("NAME", tasks[i]["ACT"]))[0])
    name += str(tasks[-1]["ID"])
    localLoadPath = os.path.join(os.getenv('DATABASE_DIR'), name)
    if (not os.path.exists(localLoadPath)):
        os.mkdir(localLoadPath)

    def copyanything(src, dst):
        try:
            sh.copytree(src, dst)
        except OSError as exc:
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                sh.copy(src, dst)
            else:
                raise
    for i in range(len(systemnames)):
        dst = os.path.join(localLoadPath, systemnames[i])
        src = os.path.join(os.getenv('DATABASE_DIR'), ids[i], systemnames[i])
        copyanything(src, dst)
    return localLoadPath


def perform(hosts_list, json_data, nCycles):
    start_entire = time.time()
    communicator = APICommunicator.getInstance()
    systemnames = list(jh.find("NAME", json_data[0]))
    taskIDs = [i for i in range(len(systemnames))]
    tasks = [initialscf(json_data[0].copy(), systemnames[i], i)
             for i in range(len(systemnames))]
    #
    # parallel SCF runs
    #
    print("o------------------------o")
    print("| Send isolated SCF runs |")
    print("o------------------------o")
    start = time.time()
    communicator.requestEvent("POST", hosts_list, taskIDs, tasks)
    communicator.resourcesFinished(hosts_list, taskIDs)
    end = time.time()
    print("Time taken for initial SCFs: ", end - start, "s")

    #
    # parallel FAT runs
    #
    newTaskIDs = []
    for i in range(len(taskIDs)):
        newTaskIDs.append(taskIDs[i] + len(systemnames))
    tasks = [rearrange(json_data[0].copy(), systemnames, taskIDs, newTaskIDs, i)
             for i in range(len(systemnames))]
    taskIDs = newTaskIDs.copy()
    batchWise = True if (len(systemnames) > len(hosts_list)) else False

    for iCycle in range(nCycles):
        print("o--------------------o")
        print("|       Cycle %2i     |" % (iCycle+1))
        print("o--------------------o")
        if (iCycle > 0):
            newTaskIDs = []
            for i in range(len(taskIDs)):
                newTaskIDs.append(taskIDs[i] + len(systemnames))
            tasks = [rearrange(json_data[0].copy(), systemnames, taskIDs, newTaskIDs, i) for i in range(len(systemnames))]
            taskIDs = newTaskIDs.copy()
        if (batchWise):
            print(
                "Specified less worker nodes than systems! We will send jobs batch-wise!")
            nBatches = len(systemnames) // len(hosts_list)
            rest = len(systemnames) % len(hosts_list)
            for iBatch in range(0, nBatches * len(hosts_list), len(hosts_list)):
                batchTasks = tasks[iBatch:(iBatch+len(hosts_list))]
                batchIDs = taskIDs[iBatch:(iBatch+len(hosts_list))]
                print("Sending batch with tasks ", batchIDs)
                communicator.requestEvent(
                    "POST", hosts_list, batchIDs, batchTasks)
                communicator.resourcesFinished(hosts_list, batchIDs)
            if (rest > 0):
                end = -1 * rest
                batchTasks = tasks[end:]
                batchIDs = taskIDs[end:]
                print("Sending batch with tasks ", batchIDs)
                communicator.requestEvent(
                    "POST", hosts_list, batchIDs, batchTasks)
                communicator.resourcesFinished(hosts_list, batchIDs)
        else:
            start = time.time()
            communicator.requestEvent("POST", hosts_list, taskIDs, tasks)
            communicator.resourcesFinished(hosts_list, taskIDs)
            end = time.time()
            print("Time taken for cycle: ", end - start, "s")
            results_resources_list = [
                str(taskIDs[i]) + "/results/" for i in range(len(taskIDs))]
            payloads = [{"TYPE": "DENSITYMATRIX"} for i in range(len(taskIDs))]
            results_dict_list = communicator.requestEvent(
                "GET", hosts_list, results_resources_list, payloads)
            newDensityMatrices = [jh.json2array(
                results_dict_list[i]['0'][0]) for i in range(len(taskIDs))]

        if (iCycle == 0):
            oldDensityMatrices = newDensityMatrices.copy()
        else:
            converged = [False for i in range(len(systemnames))]
            print("Check for convergence")
            print("---------------------")
            for i in range(len(oldDensityMatrices)):
                converged[i] = True if (np.sqrt(np.mean(
                    np.square(oldDensityMatrices[i] - newDensityMatrices[i]))) <= 1e-5) else False
                print(converged[i], np.sqrt(
                    np.mean(np.square(oldDensityMatrices[i] - newDensityMatrices[i]))))
            if (all(converged)):
                print("Convergence Reached!")
                break
            oldDensityMatrices = newDensityMatrices.copy()

    #
    # parallel FDEu runs
    #
    print("o-------------------------o")
    print("| Send parallel FDEu runs |")
    print("o-------------------------o")
    newTaskIDs = []
    for i in range(len(taskIDs)):
        newTaskIDs.append(taskIDs[i] + len(systemnames))
    tasks = [rearrange(json_data[1].copy(), systemnames, taskIDs, newTaskIDs, i) for i in range(len(systemnames))]
    taskIDs = newTaskIDs.copy()
    start = time.time()
    communicator.requestEvent("POST", hosts_list, taskIDs, tasks)
    communicator.resourcesFinished(hosts_list, taskIDs)
    end = time.time()
    print("Time taken for FDEu runs: ", end - start, "s")
    end_entire = time.time()
    print("Time taken for ENTIRE run: ", end_entire - start_entire, "s")
    finalLoad = bundleResults(tasks)
    systemString = ""
    for item in systemnames:
        systemString += item + " "
    os.chdir(finalLoad)
    os.system("python /WORK/p_esch01/progs/restApi/serestipy/client/couple.py "+ \
              str(len(systemnames))+" "+systemString)
    ## clean-up
    #for i in range(len(hosts_list)):
    #    try:
    #        _ = communicator.requestEvent("DELETE", [hosts_list[i] for j in range(len(systemnames) * (iCycle + 3))] , list(range(len(systemnames) * (iCycle + 3))))
    #    except:
    #        pass


if __name__ == "__main__":
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc/test"
    print("Reading input and preparing calculation...")
    json = jh.input2json(os.path.join(os.getcwd(), sys.argv[1]))
    nSystems = len(list(jh.find("NAME", json[0])))
    # perform(["http://128.176.214.100:5000" for i in range(nSystems)], json, 8)
    cluster = serestipy.client.akcluster.AKCluster()
    cluster.runBareMetal(perform, 2, 20000, nSystems, 1, "LYRA2,LYRA1", 7 , json, 10)
