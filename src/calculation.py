import sys
sys.path.insert(0,"/scratch/p_esch01/ownCloud/restApi/src")
import requests, os
import parallelFaTAsync as pFAT
import serenipy as spy

import JsonResolver as jr
import SettingsConverter as sc

def checkConnection(slaveIPs):
    hostsUP = []
    allHostsUp = False
    counter = 0
    for slaveHost in locusts:
        while True:
            try:
                r = requests.get(os.path.join(slaveHost, "serenityAPI"))
                r.raise_for_status()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                continue
            except requests.exceptions.HTTPError:
                hostsUP.append(slaveHost)
                break
        print("Locust "+str(counter)+" operational!")
        counter += 1
    if (len(hostsUP) == len(locusts)):
        print("All hosts are up!\n", hostsUP)
        allHostsUp = True
        return allHostsUp
    else: 
        print("Something went wrong in swarming locusts!")
        sys.exit()



parentDir = os.getcwd()

parDir = '/scratch/p_esch01/workspace/prm21/geos/'
geo1 = os.path.join(parDir,"geo1.xyz")
with open(geo1, 'r') as file:
    data1 = file.read()
    file.close()

geo2 = os.path.join(parDir,"geo2.xyz")
with open(geo2, 'r') as file:
    data2 = file.read()
    file.close()

geo3 = os.path.join(parDir,"geo3.xyz")
with open(geo3, 'r') as file:
    data3 = file.read()
    file.close()

geo4 = os.path.join(parDir,"geo4.xyz")
with open(geo4, 'r') as file:
    data4 = file.read()
    file.close()
#with open(os.path.join(parDir,'text.xyz'), "w") as file:
#  file.write(data)
#  file.close()

settingsDct = {
                "sys0" : {"name"  : "SOOOS",
                            "geometry" : "geo1.xyz",#os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                            },
                            "xyz" : data1
                }
}

settingsDct2 = {
                "sys1" : {"name"  : "SOOOS2",
                            "geometry" : "geo2.xyz",#os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                             },
                            "basis" : {"label" : "def2-svp",
                            },
                            "xyz" : data2
                },
                "sys2" : {"name"  : "SOOOS3",
                            "geometry" : "geo3.xyz",#os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                            },
                            "xyz" : data3
                },
                "sys3" : {"name"  : "SOOOS4",
                            "geometry" : "geo4.xyz",#os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                             },
                            "basis" : {"label" : "def2-svp",
                             },
                            "xyz" : data4
                },
}

wholeSettings = {"TASK" : "FDE",
                 "STATE" : "INI",
                 "ACTSETTINGS" : settingsDct,
                 "ENVSETTINGS" : settingsDct2
                 }
                 
locusts = ["http://128.176.214.105:5000/", "http://128.176.214.100:5000/"]


if(checkConnection(locusts)):
    pFAT.perform(systemSettings, locusts, 15)

for iSystem in range(len(systemSettings)):
    converter = sc.SettingsConverter(systemSettings[iSystem])
    system = spy.System(converter.getSerenipySettings())
    system.getElectronicStructure_R().getDensityMatrix().set(jr.json2array(systemSettings[iSystem]["densityMatrix"]))
    task = spy.PlotTask_R([system],[])
    task.settings.density = True
    task.run()