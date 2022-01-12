import os, sys
import requests
import time
import json
from multiprocessing import Process
import asyncio
from concurrent.futures import ThreadPoolExecutor
import JsonHelper as jh
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
                *(wholeSettings[iTask], os.path.join(slaveHosts[iTask], "api", str(taskID[iTask])))
            )
            for iTask in range(len(wholeSettings))
        ]
        for _ in await asyncio.gather(*tasks):
            pass


def postRequest(wholeSettings, adress):
    _ = requests.post(adress, json=jh.dict2json(wholeSettings))


def getRequest(adress):
    _ = (requests.get(adress)).json()


def allOnline(hostslist):
    addresses = [hostslist[i] + "/api/" for i in range(len(hostslist))]
    online = [False for i in range(len(hostslist))]
    while(True):
        for i, address in enumerate(addresses):            
            getResponse = requests.get(address)
            ans = getResponse.json()
            print(i, address, ans)
            if (ans == {'STATE: ': 'ONLINE'}):
                online[i] = True
        if (all(element == True for element in online)):
            break
        time.sleep(1.0)


def getFDE(activeSystemID, slaveHost):
    while(True):
        getResponse = requests.get(slaveHost + "/api/"+str(activeSystemID))
        ans = getResponse.json()
        # print(ans)
        if (ans["STATE: "] == "IDLE"):
            _ = getResponse.json()
            break
        # time.sleep(1.0)


def rearrange(wholeSettings, newActName, newTaskId, load=""):
    newDict = {}
    task, act, env = jh.dismemberJson(wholeSettings)
    if (list(jh.find("NAME", act))[0] == newActName):
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
        sysname = list(jh.find("NAME", env[iSys]))[0]
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
        systemnames.append(list(jh.find("NAME", tasks[i]["ACT"]))[0])
    dockerLoadPath = os.path.join("/home/calc", name)
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
    return dockerLoadPath


def perform(wholeSettings, locusts, nCycles):
    systemnames = list(jh.find("NAME", wholeSettings))
    taskIDs = [i for i in range(len(systemnames))]
    tasks = [rearrange(wholeSettings.copy(), systemnames[i], i, "")
             for i in range(len(systemnames))]
    batchWise = True if (len(systemnames) > len(locusts)) else False
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
        if (batchWise):
            print(
                "Specified less worker nodes than systems! We will send jobs batch-wise!")
            nBatches = len(systemnames) // len(locusts)
            rest = len(systemnames) % len(locusts)
            for iBatch in range(0, nBatches * len(locusts), len(locusts)):
                batchTasks = tasks[iBatch:(iBatch+len(locusts))]
                batchIDs = taskIDs[iBatch:(iBatch+len(locusts))]
                print("Sending batch with tasks ", batchIDs)
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(
                    postFDEAsync(batchTasks, batchIDs, locusts,))
                loop.run_until_complete(future)
                runInParallel([getFDE(batchIDs[iSystem], locusts[iSystem])
                               for iSystem in range(len(batchIDs))])
            if (rest > 0):
                end = -1 * rest
                batchTasks = tasks[end:]
                batchIDs = taskIDs[end:]
                print("Sending batch with tasks ", batchIDs)
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(
                    postFDEAsync(batchTasks, batchIDs, locusts,))
                loop.run_until_complete(future)
                runInParallel([getFDE(batchIDs[iSystem], locusts[iSystem])
                               for iSystem in range(len(batchIDs))])
        else:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(
                postFDEAsync(tasks, taskIDs, locusts,))
            start = time.time()
            loop.run_until_complete(future)
            runInParallel([getFDE(taskIDs[iSystem], locusts[iSystem])
                           for iSystem in range(len(taskIDs))])
            end = time.time()
            print("Time taken for cycle: ", end - start, "s")

    resultsPath = bundleResults(tasks)
    # clean-up
    for slaveHost in locusts:
        _ = [requests.delete(slaveHost + "/api/"+str(i))
             for i in range(len(systemnames) * nCycles)]
    return resultsPath


def determineSettings(nSystems, nCPU = 4, nRAM = 20000):
    maxRAM = 500000
    maxCPU = 94
    if (nCPU != 4):
        maxWorker = (maxCPU // nCPU)
    elif (nRAM != 20000):
        maxWorker = (maxRAM // nRAM)
    elif (nRAM != 20000 and nCPU != 4):
        if (nCPU > maxCPU and nRAM > maxRAM):
            print("Specified settigns are too large!")
            sys.exit()
        maxWorker = (maxCPU // nCPU) if ((maxCPU // nCPU) <= maxRAM // nRAM) else (maxRAM // nRAM)
    nWorkerPerNode = nSystems if (nSystems <= maxWorker) else maxWorker
    nNodes = (nSystems // nWorkerPerNode) if (nSystems % nWorkerPerNode == 0) else (nSystems // nWorkerPerNode + 1)
    return nCPU, nRAM, nNodes, nWorkerPerNode




if __name__ == "__main__":
    print("Cleaning left-overs...")
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc"
    ips_file = os.path.join(os.getenv('DATABASE_DIR'), "ips_hosts")
    if (os.path.exists(ips_file)):
        os.remove(ips_file)
    out_file = os.path.join(os.getenv('DATABASE_DIR'), "out")
    if (os.path.exists(out_file)):
        os.remove(out_file)

    print("Reading input and preparing calculation...")
    json = jh.input2json(os.path.join(os.getcwd(), sys.argv[1]))[0]
    nCycles = 3
    nSystems = len(list(jh.find("NAME", json)))
    nCPU, nRAM, nNodes, nWorkerPerNode = determineSettings(nSystems, int(sys.argv[2]), int(sys.argv[3]))
    print("Individual worker specs: CPU "+str(nCPU)+", Memory: "+str(nRAM)+"MB with "+str(nWorkerPerNode)+" Worker(s) per node on "+str(nNodes)+" Node(s)...")
    print("Submitting worker launcher instances...")
    for i in range(nNodes):
        os.system("python PrepareSLURM.py " + str(nWorkerPerNode) + " 4 LYRA2 " + str(nCPU) + " " +  str(nRAM) )
    print("Wait until all of them are running...")
    while(True):
        launcher_running = os.popen(
            "squeue | grep worker-l").read().split().count('R')
        launcher_queued = os.popen(
            "squeue | grep worker-l").read().split().count('Q')
        if (launcher_queued == 0 and launcher_running == nNodes):
            break
    print("All are running! Starting containers and gather ip addresses...")
    host_addresses = []
    while(True):
        if (os.path.exists(ips_file)):
            break
    old_time = os.path.getmtime(ips_file)
    time.sleep(2.0)
    while(True):
        new_time = os.path.getmtime(ips_file)
        if (new_time == old_time):
            break
        old_time = new_time
        time.sleep(2.0)
    with open(ips_file) as handle:
        content = handle.readlines()
        for line in content:
            host_addresses.append(os.path.join(line.strip()))
    print("Read addresses\n", host_addresses)
    base_set = set()
    for address in host_addresses:
        base_set.add(address[7:-5])
    base_addresses = list(base_set)
    print("Addresses for shutdown endpoint\n", base_addresses)
    allOnline(host_addresses)
    print("Starting parallel Freeze-and-Thaw calculation...")
    # start = time.time()
    resultsDir = perform(json, host_addresses, nCycles)
    # end = time.time()
    # print("Time taken for run: ", end - start, "s")

    print("Everything finished! Shutting down worker containers...")
    for address in base_addresses:
        _ = requests.post("http://" + address + ":5000/api/")
