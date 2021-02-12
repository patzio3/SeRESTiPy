import JsonResolver as jr
import os, requests, time

parDir = '/scratch/p_esch01/workspace/prm21/geos/'
geo1 = os.path.join(parDir,"geo1.xyz")
with open(geo1, 'r') as file:
    data = file.read()
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
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                            },
                            "xyz" : data
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
                            "xyz" : ""
                },
}

settingsDct2 = {
                "sys0" : {"name"  : "SOOOS",
                            "geometry" : "geo3",#os.path.join(parentDir, "geo1.xyz"),
                            "method" : "DFT",
                            "type" : "active",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                            },
                            "basis" : {"label" : "def2-svp",
                            },
                            "xyz" : ""
                },
                "sys1" : {"name"  : "SOOOS2",
                            "geometry" : "geo4",#os.path.join(parentDir, "geo2.xyz"),
                            "method" : "DFT",
                            "type" : "environment",
                            "scfMode" : "UNRESTRICTED",
                            "dft"   : {"functional" : "PBE0",
                                       "densityFitting" : "RI",
                                       "dispersion" : "D3"
                             },
                            "basis" : {"label" : "def2-svp",
                             },
                            "xyz" : ""
                },
}

wholeSettings = {"TASK" : "FDE",
                 "STATE" : "INI",
                 "SYSTEMSETTINGS" : settingsDct,
                 "ENVSETTINGS" : settingsDct2
                 }


BASE = "http://128.176.214.100:5000/"
putResponse = requests.post(BASE + "api/"+str(0), json = jr.dict2json(wholeSettings))


