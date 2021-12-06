import os
import requests
import time
import json
from multiprocessing import Process
import asyncio
from concurrent.futures import ThreadPoolExecutor
import JsonResolver as jr
import shutil as sh
import errno


def runInParallel(fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


async def postFDEAsync(wholeSettings, taskID, slaveHosts):
    with ThreadPoolExecutor(max_workers=int(len(wholeSettings))) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                postRequest,
                *(wholeSettings[iTask], os.path.join(slaveHosts[iTask],"api",str(taskID[iTask])))
            )
            for iTask in range(len(wholeSettings))
        ]
        for _ in await asyncio.gather(*tasks):
            pass


def postRequest(wholeSettings, adress):
    _ = requests.post(adress, json=jr.dict2json(wholeSettings))

def getRequest(adress):
    _ = (requests.get(adress)).json()


def allOnline(hostslist): 
    adresses = [os.path.join(hostslist[i],"api") for i in range(len(hostslist))]
    while True:
        try:
            runInParallel([getRequest(adress) for adress in adresses])
            break
        except:
            time.sleep(15.0)

def getFDE(activeSystemID, slaveHost):
    while(True):
        getResponse = requests.get(slaveHost + "api/"+str(activeSystemID))
        ans = getResponse.json()
        print(ans)
        if (ans["STATE: "] == "IDLE"):
            _ = getResponse.json()
            break
        time.sleep(15.0)


def rearrange(wholeSettings, newActName, newTaskId, load=""):
    newDict = {}
    task, act, env = jr.dismemberJson(wholeSettings)
    if (list(jr.find("NAME", act))[0] == newActName):
        newDict["TASK"] = task
        newDict["ID"] = newTaskId
        newDict["ACT"] = act
        newDict["ENV"] = env
        newDict["ACT"][list(act.keys())[0]]["LOAD"] = load
        return newDict

    newDict["TASK"] = task
    newDict["ID"] = newTaskId
    newDict["ACT"] = {}
    newDict["ENV"] = {}
    iEnv = 0
    key = list(act.keys())[0]
    for iSys in env.keys():
        sysname = list(jr.find("NAME", env[iSys]))[0]
        if (sysname == newActName):
            newDict["ACT"][str(iSys)] = env[iSys]
            newDict["ACT"][str(iSys)]["LOAD"] = load
        else:
            newDict["ENV"][str(iSys)] = env[iSys]
            newDict["ENV"][str(iSys)]["LOAD"] = load
        iEnv += 1
    newDict["ENV"]["SYS"+str(iEnv+1)] = act[key]
    newDict["ENV"]["SYS"+str(iEnv+1)]["LOAD"] = load
    return newDict.copy()


def bundleResults(tasks):
    name = "LOAD"
    ids = []
    systemnames = []
    for i in range(len(tasks)):
        name += str(tasks[i]["ID"])
        ids.append(str(tasks[i]["ID"]))
        systemnames.append(list(jr.find("NAME", tasks[i]["ACT"]))[0])
    path = os.path.join(os.getenv('DATABASE_DIR'), name)
    if (not os.path.exists(path)):
        os.mkdir(path)

    def copyanything(src, dst):
        try:
            sh.copytree(src, dst)
        except OSError as exc:
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                sh.copy(src, dst)
            else:
                raise
    for i in range(len(systemnames)):
        dst = os.path.join(path, systemnames[i])
        src = os.path.join(os.getenv('DATABASE_DIR'), ids[i], systemnames[i])
        copyanything(src, dst)
    return path


def perform(wholeSettings, locusts, nCycles):
    session = requests.Session()
    session.trust_env = False
    systemnames = list(jr.find("NAME", wholeSettings))
    taskIDs = [i for i in range(len(systemnames))]
    tasks = [rearrange(wholeSettings.copy(), systemnames[i], i, "")
             for i in range(len(systemnames))]
    for iCycle in range(nCycles):
        print("o--------------------o")
        print("|       Cycle %2i     |" % (iCycle+1))
        print("o--------------------o")
        if (iCycle > 0):
            load = bundleResults(tasks)
            for i in range(len(taskIDs)):
                taskIDs[i] += len(systemnames)
            tasks = [rearrange(wholeSettings.copy(), systemnames[i],
                               taskIDs[i], load) for i in range(len(systemnames))]
        # send post requests to slave nodes asynchronously
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(postFDEAsync(tasks, taskIDs, locusts,))
        loop.run_until_complete(future)

        # get results synchronously
        runInParallel([getFDE(taskIDs[iSystem], locusts[iSystem])
                       for iSystem in range(len(taskIDs))])

    resultsPath = bundleResults(tasks)
    # clean-up
    for slaveHost in locusts:
        _ = [requests.delete(slaveHost + "api/"+str(i))
             for i in range(len(systemnames) * nCycles)]
    return resultsPath


json = jr.input2json(os.path.join(os.getcwd(), "inp"))[0]
allOnline(["http://10.223.1.1:5000/", "http://10.223.1.3:5000/","http://10.223.1.5:5000/"])
resultsDir = perform(json, ["http://10.223.1.1:5000/", "http://10.223.1.3:5000/","http://10.223.1.5:5000/"], 5)
