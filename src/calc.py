import JsonResolver as jr
import os, requests, time

import BatchSender as bs
import RequestHandler as rh

parDir = '/home/patrick/progs/restApi/geo'
geo1 = os.path.join(parDir,"3.xyz")
with open(geo1, 'r') as file:
    data1 = file.read()
    file.close()

geo2 = os.path.join(parDir,"4.xyz")
with open(geo2, 'r') as file:
    data2 = file.read()
    file.close()

geo3 = os.path.join(parDir,"5.xyz")
with open(geo3, 'r') as file:
    data3 = file.read()
    file.close()

geo4 = os.path.join(parDir,"6.xyz")
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
                 "ACTSETTINGS" : settingsDct,
                 "ENVSETTINGS" : settingsDct2
                 }


settingsDct = {
                "sys0" : {"name"  : "SOOadsfOS",
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
                "sys1" : {"name"  : "SOasdfOOS2",
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
                "sys2" : {"name"  : "SOadsfOOS3",
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
                "sys63" : {"name"  : "SOasdfOOS4",
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

wholeSettings2 = {"TASK" : "FDE",
                 "ACTSETTINGS" : settingsDct,
                 "ENVSETTINGS" : settingsDct2
                 }

hosts = ["http://127.0.1.1:5000"]#, "http://128.176.214.105:5000"]
job_ids = [0]
nJobs = 1
inputs = [wholeSettings]

sender = bs.BatchSender(hosts, job_ids, nJobs)
sender.sendJobs(inputs)
sender.patchJobs(inputs)
#sender.getJobs()
#print(sender.getRequestHandler(0).getResponseContent())
#print(sender.getRequestHandler(1).getResponseContent())
#sender.deleteJobs()
