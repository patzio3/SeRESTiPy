import os, requests, time, json, sys
import serenipy as spy
import JsonResolver as jr
import SettingsConverter as sc
from multiprocessing import Process
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor

np.set_printoptions(precision = 8, suppress = True)


def runInParallel(fns):
    proc = []
    for fn in fns:
        p = Process(target = fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

async def postFDEAsync(wholeSettings, activeSystemID, slaveHosts):
    if (wholeSettings["task"] != "FDE"):
        print("Must specify FDE Task in input!")
        sys.exit()
    with ThreadPoolExecutor(max_workers = int(len(wholeSettings.items()) - 1)) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                postRequest,
                *(wholeSettings, activeSystemID[iSystem], slaveHosts[iSystem])
            )
            for iSystem in range(len(wholeSettings.items()) - 1)
        ]
        for response in await asyncio.gather(*tasks):
            pass

def postRequest(wholeSettings, activeSystemID, slaveHost):
    counter = 0
    for outer, inner in wholeSettings.items():
        if (outer == "task"):
            continue
        if (counter == activeSystemID):
            inner["system"]["type"] = "active"
        else:
            inner["system"]["type"] = "environment"
        counter += 1
    _ = requests.post(slaveHost + "api/"+str(activeSystemID), json = jr.dict2json(wholeSettings))

def getFDE(results, activeSystemID, slaveHost):
    getResponse = requests.get(slaveHost + "api/"+str(activeSystemID))
    _ = requests.delete(slaveHost + "api/"+str(activeSystemID))
    results[activeSystemID] = getResponse.json()

def perform(systemSettings, locusts, nCycles):
    initialSystems = []
    oldDmats = [0.0 for i in range(len(systemSettings))]
    oldTotalEnergy = [0.0 for i in range(len(systemSettings))]
    #prepare everything for the provided systems
    for iSystem in range(len(systemSettings)):
        converter = sc.SettingsConverter(jr.dict2json(systemSettings[iSystem]))
        initialSystem = spy.System(converter.getSerenipySettings())
        initialSystems.append(initialSystem)
        #Initial SCF is needed
        if (systemSettings[iSystem]["system"]["scfMode"].upper() == "RESTRICTED"):
            task = spy.ScfTask_R(initialSystem)
            task.run()
            initialSystemOrbitalController = initialSystem.getElectronicStructure_R().getDensityMatrix()
            systemSettings[iSystem]["densityMatrix"] = jr.array2json(initialSystemOrbitalController.total())
            systemSettings[iSystem]["coefficients"] = jr.array2json(initialSystem.getElectronicStructure_R().coeff())
            oldDmats[iSystem] = initialSystemOrbitalController.total()
            oldTotalEnergy[iSystem] = initialSystem.getEnergy()
        elif (systemSettings[iSystem]["system"]["scfMode"].upper() == "UNRESTRICTED"):
            task = spy.ScfTask_U(initialSystem)
            task.run()
            initialSystemOrbitalController = initialSystem.getElectronicStructure_U().getDensityMatrix()
            systemSettings[iSystem]["densityMatrixAlpha"] = jr.array2json(initialSystemOrbitalController.alpha())
            systemSettings[iSystem]["densityMatrixBeta"] = jr.array2json(initialSystemOrbitalController.beta())
            systemSettings[iSystem]["coefficientsAlpha"] = jr.array2json(initialSystem.getElectronicStructure_U().alphaCoeff())
            systemSettings[iSystem]["coefficientsBeta"] = jr.array2json(initialSystem.getElectronicStructure_U().betaCoeff())
            oldDmats[iSystem] = initialSystemOrbitalController.total()
            oldTotalEnergy[iSystem] = initialSystem.getEnergy()
        else: 
            print("SCFMode invalid!")
            sys.exit()

    totalEnergies = np.zeros((nCycles,len(systemSettings)))
    for iCycle in range(nCycles):
        print("o--------------------o")
        print("|       Cycle %2i     |" %(iCycle+1))
        print("o--------------------o")
        converged = [False for i in range(len(systemSettings))]
        results = {}
        activeSystemIDs = []
        #Task settings
        wholeSettings = {"task" : "FDE"}
        for iSystem in range(len(systemSettings)):
            wholeSettings["system" + str(iSystem)] = systemSettings[iSystem]
            activeSystemIDs.append(iSystem)

        #send post requests to slave nodes asynchronously
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(postFDEAsync(wholeSettings, activeSystemIDs, locusts))
        loop.run_until_complete(future)

        #get results synchronously
        runInParallel([getFDE(results, activeSystemIDs[iSystem], locusts[iSystem]) for iSystem in range(len(systemSettings))])
        #collect results, check for convergence and update
        newTotalEnergy = [0.0 for i in range(len(systemSettings))]
        for iSystem in range(len(systemSettings)):
            print("--- System %2i ---" %(iSystem))
            totalEnergies[iCycle,iSystem] = results[iSystem]["0"]["totalEnergy"]
            newTotalEnergy[iSystem] = float(results[iSystem]["0"]["totalEnergy"])
            if (systemSettings[iSystem]["system"]["scfMode"].upper() == "RESTRICTED"):
                systemSettings[iSystem]["densityMatrix"] = results[iSystem]["0"]["densityMatrix"]
                systemSettings[iSystem]["coefficients"] = results[iSystem]["0"]["coefficients"]
                # print("densityMatrix of system {} in Cycle {}\n {}".format(iSystem, iCycle + 1, jr.json2array(results[iSystem]["0"]["densityMatrix"])))
                newDmat = jr.json2array(results[iSystem]["0"]["densityMatrix"])
            elif (systemSettings[iSystem]["system"]["scfMode"].upper() == "UNRESTRICTED"):
                # print("densityMatrixAlpha of system {} in Cycle {}\n {}".format(iSystem, iCycle + 1, jr.json2array(results[iSystem]["0"]["densityMatrixAlpha"])))
                # print("densityMatrixBeta of system {} in Cycle {}\n {}".format(iSystem, iCycle + 1, jr.json2array(results[iSystem]["0"]["densityMatrixBeta"])))
                systemSettings[iSystem]["densityMatrixAlpha"] = results[iSystem]["0"]["densityMatrixAlpha"]
                systemSettings[iSystem]["densityMatrixBeta"] = results[iSystem]["0"]["densityMatrixBeta"]
                systemSettings[iSystem]["coefficientsAlpha"] = results[iSystem]["0"]["coefficientsAlpha"]
                systemSettings[iSystem]["coefficientsBeta"] = results[iSystem]["0"]["coefficientsBeta"]
                newDmat = jr.json2array(results[iSystem]["0"]["densityMatrixAlpha"]) + jr.json2array(results[iSystem]["0"]["densityMatrixBeta"])
            else:
                print("SCFMode invalid!")
                sys.exit()
            drho = np.sqrt( (np.square((oldDmats[iSystem] - newDmat).flatten())).sum() )
            dE = abs(newTotalEnergy[iSystem] - oldTotalEnergy[iSystem])
            if (drho < 1.0e-6 and dE < 1.0e-6):
                converged[iSystem] = True
            print("Difference density norm", drho)
            print("Difference in total energy", dE)
            #update convergence criteria
            oldTotalEnergy[iSystem] = newTotalEnergy[iSystem]
            oldDmats[iSystem] = newDmat

        #check convergence
        convergedSystems = 0
        for iSystem in range(len(systemSettings)):
            if(converged[iSystem]):
                convergedSystems += 1
        if (convergedSystems == len(systemSettings)):
            print("Parallel Freeze-and-Thaw converged!")
            break
    print("Total energies in different cycles\n", totalEnergies)