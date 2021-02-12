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

settingsDct = {
                "sys0" : {"name"  : "SOOOS",
                            "geometry" : "geo1",#os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                           }
                },
                "sys1" : {"name"  : "SOOOS2",
                            "geometry" : "geo2",#os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                             },
                            "basis" : {"label" : "def2-svp",
                            },
                },
}

settingsDct2 = {
                "sys0" : {"name"  : "SOOOS",
                            "geometry" : "geo1",#os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                           }
                },
                "sys1" : {"name"  : "SOOOS2",
                            "geometry" : "geo2",#os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                             },
                            "basis" : {"label" : "def2-svp",
                            },
                },
}

wholeSettings = {"TASK" : "FDE", 
                 "SYSTEMSETTINGS" : settingsDct,
                 "ENVSETTINGS" : settingsDct2
                 }



systemSettings = [settingsDct, settingsDct2]
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