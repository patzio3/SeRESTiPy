import os, requests, time, json, sys
from multiprocessing import Process
import asyncio
from concurrent.futures import ThreadPoolExecutor
import JsonResolver as jr
import numpy as np
import time

def runInParallel(fns):
    proc = []
    for fn in fns:
        p = Process(target = fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

async def postFDEAsync(wholeSettings, activeSystemID, slaveHosts, load = ""):
    if (wholeSettings["TASK"] != "FDE"):
        print("Must specify FDE Task in input!")
        sys.exit()
    with ThreadPoolExecutor(max_workers = int(len(wholeSettings.items()) - 1)) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                postRequest,
                *(wholeSettings, activeSystemID[iSystem], slaveHosts[0], load[iSystem])
            )
            for iSystem in range(len(wholeSettings.items()) - 1)
        ]
        for response in await asyncio.gather(*tasks):
            pass

def postRequest(wholeSettings, activeSystemID, slaveHost, load =""):
    newDict = {}
    syssettings = {}
    i = 0
    for outer, inner in json.items():
        if (outer == "TASK"): 
            newDict["TASK"] = inner
        if (outer == "ID"): 
            newDict["ID"] = inner
        if (outer == "ACT"):
            for _, innerinnerinner in inner.items():
                cpy = innerinnerinner.copy()
                cpy["LOAD"] = load
                syssettings[i] = cpy
                i += 1
        if (outer == "ENV"):
            for _, innerinnerinner in inner.items():
                cpy = innerinnerinner.copy()
                cpy["LOAD"] = load
                syssettings[i] = cpy
                i += 1
    newDict["ACT"] = {}
    newDict["ENV"] = {}
    for k,v in syssettings.items():
        if (k == activeSystemID):
            newDict["ACT"]["SYS"+str(k)] = v
        else:
            newDict["ENV"]["SYS"+str(k)] = v
    _ = requests.post(slaveHost + "api/"+str(activeSystemID), json = jr.dict2json(newDict))

def getFDE(results, activeSystemID, slaveHost):
    while(True):
        getResponse = requests.get(slaveHost + "api/"+str(activeSystemID))
        ans = getResponse.json()
        #_ = requests.delete(slaveHost + "api/"+str(activeSystemID))
        print(ans)
        if (ans["STATE: "] == "IDLE"):
            results[activeSystemID] = getResponse.json()
            break
        time.sleep(5.0)
        

def perform(wholeSettings, locusts, nCycles):
    for iCycle in range(nCycles):
        print("o--------------------o")
        print("|       Cycle %2i     |" %(iCycle+1))
        print("o--------------------o")
        load = ["","",""]
        if (iCycle > 0):
            load = ["/WORK/p_esch01/progs/restApi/src"+str(activeSystemIDs[iSystem]) for iSystem in range(len(activeSystemIDs))]
        activeSystemIDs = np.array([0,1,2]) 
        #send post requests to slave nodes asynchronously
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(postFDEAsync(wholeSettings, activeSystemIDs, locusts, load))
        loop.run_until_complete(future)

        #get results synchronously
        results = {}
        runInParallel([getFDE(results, activeSystemIDs[iSystem], locusts[0]) for iSystem in range(len(activeSystemIDs))])

        activeSystemIDs += 1
    





json = {
  "TASK":"FDE",
  "ID":69,
  "ACT":{
    "SYS0":{
      "NAME":"SOOOS",

      "GEOMETRY":"geo1.xyz",
      "METHOD":"DFT",
      "SCFMODE":"UNRESTRICTED",
      "DFT":{
        "FUNCTIONAL":"PBE",
        "DISPERSION":"D3"
      },
      "BASIS":{
        "LABEL":"def2-svp",
        "DENSITYFITTING":"RI"
      },
      "XYZ":"12 \n \nC          1.39296        0.18607        6.06918 \nC          0.92094       -0.98469        5.46443\nC         -0.43002       -1.09548        5.11536\nC         -1.30881       -0.03635        5.37071\nC          0.51487        1.24569        6.32491\nC         -0.83594        1.13405        5.97550\nH          2.43796        0.27210        6.33934\nCl         2.02179       -2.31228        5.14419\nH         -0.79549       -2.00100        4.64753\nCl         1.10693        2.71265        7.08280\nCl        -3.00172       -0.17572        4.93305\nH         -1.51547        1.95355        6.17317"
    }
  },
  "ENV":{
    "SYS0":{
      "NAME":"ENV",

      "GEOMETRY":"geo2.xyz",
      "METHOD":"DFT",
      "SCFMODE":"UNRESTRICTED",
      "DFT":{
        "FUNCTIONAL":"PBE",
        "DISPERSION":"D3"
      },
      "BASIS":{
        "LABEL":"def2-svp",
        "DENSITYFITTING":"RI"
      },
      "basis":{
        "label":"def2-svp",
        "densityFitting":"RI"
      },
      "XYZ":"2 \n \nHe 0.0 0.0 0.0 \nHe 0.0 0.0 1.0 "
    },
    "SYS1":{
      "NAME":"ENV2",

      "GEOMETRY":"geo3.xyz",
      "METHOD":"DFT",
      "SCFMODE":"UNRESTRICTED",
      "DFT":{
        "FUNCTIONAL":"PBE",
        "DISPERSION":"D3"
      },
      "BASIS":{
        "LABEL":"def2-svp",
        "DENSITYFITTING":"RI"
      },
      "basis":{
        "label":"def2-svp",
        "densityFitting":"RI"
      },
      "XYZ":"2 \n \nHe 0.0 0.0 0.0 \nHe 0.0 0.0 2.0 "
    }
  }
}

perform(json,["http://10.4.137.8:5000/"],2)