import os, requests, time, json, sys
import serenipy as spy
import JsonResolver as jr
import SettingsConverter as sc
from multiprocessing import Process
import numpy as np

#Arrakis http://128.176.214.100:5000
#Regulus http://128.176.214.105:5000


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def postFDE(wholeSettings, activeSystemID, slaveHost):
    if (wholeSettings["task"] != "FDE"):
        print("Must specify FDE Task in input!")
        sys.exit()
    counter = 0
    for outer, inner in wholeSettings.items():
        if (outer == "task"):
            continue
        if (counter == activeSystemID):
            inner["system"]["type"] = "active"
        else:
            inner["system"]["type"] = "environment"
        counter += 1
    _ = requests.post(slaveHost + "serenityAPI/"+str(activeSystemID), json = jr.dict2json(wholeSettings))

    

def getFDE(results, activeSystemID, slaveHost):
    getResponse = requests.get(slaveHost + "api/"+str(activeSystemID))
    _ = requests.delete(slaveHost + "api/"+str(activeSystemID))
    results[activeSystemID] = getResponse.json()

    

parentDir = os.getcwd()
np.set_printoptions(precision = 5, suppress = True)


settingsDct = {
                "system" : {"name"  : "SOOOS",
                            "geometry" : os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "path" : "./",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED"
                            #"charge" : 1,
                            #"spin" : 1
                            },
                "dft"   : {"functional" : "PBE",
                           "densityFitting" : "RI",
                           "dispersion" : "D3"
                           },
                "basis" : {"label" : "def2-svp",
                           }
                }

settingsDct2 = {
                "system" : {"name"  : "SOOOS2",
                            "geometry" : os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "path" : "./",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED"
                            },
                "dft"   : {"functional" : "PBE",
                           "densityFitting" : "RI",
                           "dispersion" : "D3"
                           },
                "basis" : {"label" : "def2-svp",
                           }
                }


systemSettings = [settingsDct, settingsDct2]
initialSystems = []

#prepare everything for the provided systems
for iSystem in range(len(systemSettings)):
    converter = sc.SettingsConverter(jr.dict2json(systemSettings[iSystem]))
    initialSystem = spy.System(converter.getSerenipySettings())
    initialSystems.append(initialSystem)
    #Initial SCF is needed
    if (systemSettings[iSystem]["system"]["scfMode"].upper() == "RESTRICTED"):
        initialSystemOrbitalController = initialSystem.getElectronicStructure_R().getDensityMatrix()
        systemSettings[iSystem]["densityMatrix"] = jr.array2json(initialSystemOrbitalController.total())
        systemSettings[iSystem]["coefficients"] = jr.array2json(initialSystem.getElectronicStructure_R().coeff())
    elif (systemSettings[iSystem]["system"]["scfMode"].upper() == "UNRESTRICTED"):
        initialSystemOrbitalController = initialSystem.getElectronicStructure_U().getDensityMatrix()
        systemSettings[iSystem]["densityMatrixAlpha"] = jr.array2json(initialSystemOrbitalController.alpha())
        systemSettings[iSystem]["densityMatrixBeta"] = jr.array2json(initialSystemOrbitalController.beta())
        systemSettings[iSystem]["coefficientsAlpha"] = jr.array2json(initialSystem.getElectronicStructure_U().alphaCoeff())
        systemSettings[iSystem]["coefficientsBeta"] = jr.array2json(initialSystem.getElectronicStructure_U().betaCoeff())
    else: 
        print("SCFMode invalid!")
        sys.exit()

totalEnergies = np.zeros((6,2))

for iCycle in range(6):
    results = {}
    #Task settings
    wholeSettings = {"task" : "FDE"}
    for iSystem in range(len(systemSettings)):
        wholeSettings["system" + str(iSystem)] = systemSettings[iSystem]
        #print("SETTINGS IN CYCLE " + str(iCycle) + "\n", wholeSettings["system" + str(iSystem)])
    
    runInParallel(postFDE(wholeSettings, 0, "http://128.176.214.100:5000/"),\
                  postFDE(wholeSettings, 1, "http://128.176.214.105:5000/"))  

    runInParallel(getFDE(results, 0, "http://128.176.214.100:5000/"),\
                  getFDE(results, 1, "http://128.176.214.105:5000/"))

    totalEnergies[iCycle,0] = results[0]["0"]["totalEnergy"]
    totalEnergies[iCycle,1] = results[1]["0"]["totalEnergy"]
    
    print("densityMatrixAlpha of benz1 in Cycle ", iCycle, "\n", jr.json2array(results[0]["0"]["densityMatrixAlpha"]))
    print("densityMatrixAlpha of benz2 in Cycle ", iCycle, "\n", jr.json2array(results[1]["0"]["densityMatrixAlpha"]))

    #update Density matrix and coefficients
    for iSystem in range(len(systemSettings)):
        if (systemSettings[iSystem]["system"]["scfMode"].upper() == "RESTRICTED"):
            systemSettings[iSystem]["densityMatrix"] = results[iSystem]["0"]["densityMatrix"]
            systemSettings[iSystem]["coefficients"] = results[iSystem]["0"]["coefficients"]
        elif (systemSettings[iSystem]["system"]["scfMode"].upper() == "UNRESTRICTED"):
            systemSettings[iSystem]["densityMatrixAlpha"] = results[iSystem]["0"]["densityMatrixAlpha"]
            systemSettings[iSystem]["densityMatrixBeta"] = results[iSystem]["0"]["densityMatrixBeta"]
            systemSettings[iSystem]["coefficientsAlpha"] = results[iSystem]["0"]["coefficientsAlpha"]
            systemSettings[iSystem]["coefficientsBeta"] = results[iSystem]["0"]["coefficientsBeta"]
        else: 
            print("SCFMode invalid!")
            sys.exit()
        
print("Total energies in different cycles\n", totalEnergies)


#    runInParallel(performFDE(results, wholeSettings, 0, "http://127.0.1.1:5000/"),\
#                  performFDE(results, wholeSettings, 1, "http://127.0.1.1:5000/"))  #home
#rhoOld = activeSystem.getElectronicStructure_R().getDensityMatrix().total()