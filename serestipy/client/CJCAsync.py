import os
import sys
import time
import json
import asyncio
import errno
from unicodedata import name
import numpy as np
import shutil as sh
import serestipy.client.JsonHelper as jh
from serestipy.client.APICommunicator import APICommunicator
import serestipy.client.akcluster


def prepTasks(wholeSettings, newTaskID, namesToTaskIDsMap, nAct = 1, load = os.getenv('DATABASE_DIR'), saveall = False):
    task, tasksettings, act, env = jh.dismemberJson(wholeSettings)
    newDict = {}
    newDict["TASK"] = task
    newDict["TASK_SETTINGS"] = tasksettings
    newDict["ID"] = str(newTaskID)
    allSysSettings = dict(act, **env)
    for iKey, key in enumerate(allSysSettings.keys()):
        if (iKey < nAct):
            act[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[act[key]["NAME"]]))
            act[key]["SAVEONDISK"] = True
            continue
        env[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[env[key]["NAME"]]))
        if (not saveall):
            env[key]["SAVEONDISK"] = False
    newDict["ACT"] = act
    newDict["ENV"] = env
    return newDict.copy()



# def rearrange(wholeSettings, systemNames, oldTaskID, newTaskIDs, iAct, load = os.getenv('DATABASE_DIR'), saveall = False):
#     task, tasksettings, act, env = jh.dismemberJson(wholeSettings)
#     allSysSettings = dict(act, **env)
#     newDict = {}
#     newDict["TASK"] = task
#     newDict["TASK_SETTINGS"] = tasksettings
#     newDict["ACT"] = {}
#     newDict["ENV"] = {}
#     allKeys = list(allSysSettings.keys())
#     for iSys in range(len(systemNames)):
#         if (iSys == iAct):
#             newDict["ID"] = str(newTaskIDs[iAct])
#             newDict["ACT"][allKeys[0]] = list(jh.find(str(allKeys[iSys]), allSysSettings))[0]
#             newDict["ACT"][allKeys[0]]["SAVEONDISK"] = True
#             if (not load == ""):
#                 newDict["ACT"][allKeys[0]]["LOAD"] = os.path.join(load, str(oldTaskID[iSys]))
#         else:
#             newDict["ENV"][str(allKeys[iSys])] = list(jh.find(str(allKeys[iSys]), allSysSettings))[0]
#             if (not saveall):
#                 newDict["ENV"][str(allKeys[iSys])]["SAVEONDISK"] = False
#             if (not load == ""):
#                 newDict["ENV"][str(allKeys[iSys])]["LOAD"] = os.path.join(load, str(oldTaskID[iSys]))
#     return newDict.copy()

# def prepTasks(wholeSettings, oldTaskID, newTaskID, namesToTaskIDsMap, load = os.getenv('DATABASE_DIR')):
#     task, tasksettings, act, env = jh.dismemberJson(wholeSettings)
#     newDict = {}
#     newDict["TASK"] = task
#     newDict["TASK_SETTINGS"] = tasksettings
#     newDict["ID"] = str(newTaskID)
#     allSysSettings = dict(act, **env)
#     for iKey, key in enumerate(allSysSettings.keys()):
#         if (iKey < 2):
#             act[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[act[key]["NAME"]]))
#             continue
#         env[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[env[key]["NAME"]]))
#     newDict["ACT"] = act
#     newDict["ENV"] = env
#     return newDict.copy()



# def prepFDEc(wholeSettings, newTaskID, namesToTaskIDsMap, load = os.getenv('DATABASE_DIR')):
#     task, tasksettings, act, env = jh.dismemberJson(wholeSettings)
#     newDict = {}
#     newDict["TASK"] = task
#     newDict["TASK_SETTINGS"] = tasksettings
#     newDict["ID"] = str(newTaskID)
#     allSysSettings = dict(act, **env)
#     for iKey, key in enumerate(allSysSettings.keys()):
#         if (iKey < 2):
#             act[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[act[key]["NAME"]]))
#             continue
#         env[key]["LOAD"] = os.path.join(load, str(namesToTaskIDsMap[env[key]["NAME"]]))
#     newDict["ACT"] = act
#     newDict["ENV"] = env
#     return newDict.copy()


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


# def bundleResults(tasks):
#     name = "LOAD"
#     ids = []
#     systemnames = []
#     for i in range(len(tasks)):
#         ids.append(str(tasks[i]["ID"]))
#         systemnames.append(list(jh.find("NAME", tasks[i]["ACT"]))[0])
#     name += str(tasks[-1]["ID"])
#     localLoadPath = os.path.join(os.getenv('DATABASE_DIR'), name)
#     if (os.path.exists(localLoadPath)):
#         sh.rmtree(localLoadPath)
#         os.mkdir(localLoadPath)

#     def copyanything(src, dst):
#         try:
#             sh.copytree(src, dst)
#         except OSError as exc:
#             if exc.errno in (errno.ENOTDIR, errno.EINVAL):
#                 sh.copy(src, dst)
#             else:
#                 raise
#     for i in range(len(systemnames)):
#         dst = os.path.join(localLoadPath, systemnames[i])
#         src = os.path.join(os.getenv('DATABASE_DIR'), ids[i], systemnames[i])
#         copyanything(src, dst)
#     return localLoadPath


def performParallelFaT(hosts_list, json_data, nCycles):
    communicator = APICommunicator.getInstance()
    systemnames = sorted(list(set(jh.find("NAME", json_data))))
    taskIDs = [i for i in range(len(systemnames))]
    namesToTaskIDsMap = {systemnames[i] : taskIDs[i] for i in range(len(taskIDs))}
    tasks = [initialscf(json_data[5].copy(), systemnames[i], i)
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
    print("o-------------------------o")
    print("| Send parallel FDE runs  |")
    print("o-------------------------o")
    #
    # parallel FAT runs
    #
    
    newTaskIDs = []
    for i in range(len(taskIDs)):
        newTaskIDs.append(taskIDs[i] + len(systemnames))
    tasks = [prepTasks(json_data[i].copy(), newTaskIDs[i], namesToTaskIDsMap) for i in range(len(json_data))]
    namesToTaskIDsMap = {systemnames[i] : newTaskIDs[i] for i in range(len(newTaskIDs))}
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
            tasks = [prepTasks(json_data[i].copy(), newTaskIDs[i], namesToTaskIDsMap) for i in range(len(json_data))]
            namesToTaskIDsMap = {systemnames[i] : newTaskIDs[i] for i in range(len(newTaskIDs))}
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
                communicator.resourcesFinished(hosts_list[end:], batchIDs)
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
    print(namesToTaskIDsMap)
    return taskIDs, namesToTaskIDsMap

def performParallelFDEu(hosts_list, json_data, taskIDs, namesToTaskIDsMap):
    print("o-------------------------o")
    print("| Send parallel FDEu runs |")
    print("o-------------------------o")
    communicator = APICommunicator.getInstance()
    systemnames = sorted(list(set(jh.find("NAME", json_data))))
    newTaskIDs = []
    for i in range(len(taskIDs)):
        newTaskIDs.append(taskIDs[i] + len(systemnames))
    tasks = [prepTasks(json_data[i].copy(), newTaskIDs[i], namesToTaskIDsMap) for i in range(len(json_data))]
    namesToTaskIDsMap = {systemnames[i] : newTaskIDs[i] for i in range(len(newTaskIDs))}
    print(namesToTaskIDsMap)
    taskIDs = newTaskIDs.copy()
    start = time.time()
    communicator.requestEvent("POST", hosts_list, taskIDs, tasks)
    communicator.resourcesFinished(hosts_list, taskIDs)
    end = time.time()
    print("Time taken for FDEu runs: ", end - start, "s")
    return taskIDs, namesToTaskIDsMap

def performParallelFDEc(hosts_list, json_data, taskIDs, namesToTaskIDsMap):
    print("o-------------------------o")
    print("| Send parallel FDEc runs |")
    print("o-------------------------o")
    communicator = APICommunicator.getInstance()
    newTaskIDs = []
    for i in range(len(json_data)):
        newTaskIDs.append(i + 6000)
    # namesToTaskIDsMap = {systemnames[i] : newTaskIDs[i] for i in range(len(newTaskIDs))}
    print(namesToTaskIDsMap)
    print(len(json_data))
    tasks = [prepTasks(json_data[i].copy(), newTaskIDs[i], namesToTaskIDsMap, 2) for i in range(len(json_data))]
    taskIDs = newTaskIDs.copy()
    start = time.time()
    batchWise = True if (len(tasks) > len(hosts_list)) else False
    if (batchWise):
        print(
            "Specified less worker nodes than FDEc coupling runs! We will send jobs batch-wise!")
        nBatches = len(tasks) // len(hosts_list)
        rest = len(tasks) % len(hosts_list)
        for iBatch in range(0, nBatches * len(hosts_list), len(hosts_list)):
            batchTasks = tasks[iBatch:(iBatch+len(hosts_list))]
            batchIDs = taskIDs[iBatch:(iBatch+len(hosts_list))]
            print("Sending batch with tasks ", batchIDs)
            communicator.requestEvent("POST", hosts_list, batchIDs, batchTasks)
            communicator.resourcesFinished(hosts_list, batchIDs)
        if (rest > 0):
            end = -1 * rest
            batchTasks = tasks[end:]
            batchIDs = taskIDs[end:]
            print("Sending batch with tasks ", batchIDs)
            communicator.requestEvent("POST", hosts_list[end:], batchIDs, batchTasks)
            communicator.resourcesFinished(hosts_list, batchIDs)
    end = time.time()
    print("Time taken for FDEc runs: ", end - start, "s")
    return taskIDs
    

def main(hosts_list, jsons, nCycles):
    taskIDsPFaT, namesToTaskIDsMap = performParallelFaT(hosts_list, jsons[0], nCycles)
    taskIDsFDEu, namesToTaskIDsMap = performParallelFDEu(hosts_list, jsons[1], taskIDsPFaT, namesToTaskIDsMap)
    taskIDsFDEc = performParallelFDEc(hosts_list, jsons[2], taskIDsFDEu, namesToTaskIDsMap)



    # allTaskIDs = taskIDsPFaT + taskIDsFDEu + taskIDsFDEc
    # print("o----------------o")
    # print("| Free used URIs |")
    # print("o----------------o")
    # # clean-up
    # communicator = APICommunicator.getInstance()
    # for i in range(len(allTaskIDs)):
    #     try:
    #         _ = communicator.requestEvent("DELETE", [hosts_list[i] for j in range(len(allTaskIDs))], allTaskIDs)
    #     except:
    #         pass
   
    

if __name__ == "__main__":
    nCycles = 20
    print("Reading input and preparing calculation...")
    jsons = [
        jh.input2json(os.path.join(os.getcwd(), sys.argv[1])), #pFaT  inp
        jh.input2json(os.path.join(os.getcwd(), sys.argv[2])), #pFDEu inp
        jh.input2json(os.path.join(os.getcwd(), sys.argv[3]))  #pFDEc inp
        ]
    nSystems = len(list(set(jh.find("NAME", jsons[0]))))
    start_entire = time.time()
    hosts_list = ["http://127.0.1.1:5000" for i in range(nSystems)]
    main(hosts_list, jsons, nCycles)
    # cluster = serestipy.client.akcluster.AKCluster()
    # cluster.runBareMetal(main, 2, 20000, nSystems, 1, "LYRA2,LYRA1", 7 , json, 3)
    end_entire = time.time()
    print("Time taken for ENTIRE run: ", end_entire - start_entire, "s")
    

    # finalLoad = bundleResults(allTaskIDs)
    # systemnames = list(jh.find("NAME", json[0]))
    # systemString = ""
    # for item in systemnames:
    #     systemString += item + " "
    # os.chdir(finalLoad)
    # os.system("python /home/patrick/Programs/restApi/serestipy/client/couple.py "+ \
    #           str(len(systemnames))+" "+systemString)
    
