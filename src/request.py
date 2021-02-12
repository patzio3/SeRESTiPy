import os, requests, time
import serenipy as spy
import JsonResolver as jr

from multiprocessing import Process

import numpy as np
import json
import serenipy as spy
import SettingsConverter as sc


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def requestDmat(id, wholeSettings):
    putResponse = requests.put(BASE + "api/"+str(id), json = jr.dict2json(wholeSettings) )
    getResponse = requests.get(BASE + "api/"+str(id))
    responseData = getResponse.json()
    getResponse = requests.delete(BASE + "api/"+str(id))
    print(responseData[0])



parentDir = os.getcwd()

settingsDct = {
                "system" : {"name"  : "SOOOS",
                            "geometry" : os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "path" : "./",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED"
                            },
                "dft"   : {"functional" : "PBE0",
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
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED"
                            },
                "dft"   : {"functional" : "PBE0",
                           "densityFitting" : "RI",
                           "dispersion" : "D3"
                           },
                "basis" : {"label" : "def2-svp",
                           }
                }

wholeSettings = {"task" : "FDE", 
                 "actSettings" : settingsDct,
                 "envSettings" : settingsDct2}





BASE = "http://128.176.214.100:5000/"

id = 0
putResponse = requests.post(BASE + "serenityAPI/"+str(id), json = jr.dict2json(wholeSettings))
getResponse = requests.get(BASE + "serenityAPI/"+str(id))
delResponse = requests.delete(BASE + "serenityAPI/"+str(id))
responseData = getResponse.json()

#embedded system
alphaDmat = jr.json2array(responseData["0"]["densityMatrixAlpha"])
betaDmat = jr.json2array(responseData["0"]["densityMatrixBeta"])
totalEnergy = responseData["0"]["totalEnergy"]


#isolated system
converter = sc.SettingsConverter(jr.dict2json(settingsDct))
dummySys = spy.System(converter.getSerenipySettings())
dummyOrbitalController = dummySys.getElectronicStructure_U().getDensityMatrix()
print("Isolated density matrix\n", dummyOrbitalController.total())
iso = dummyOrbitalController.total()

#set embedded density to isolated system
dummyOrbitalController.set(alphaDmat, betaDmat)
print("Embedded density matrix\n", dummyOrbitalController.total())
#difference density matrix
print("Difference matrix\n", dummyOrbitalController.total() - iso)