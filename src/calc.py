import JsonResolver as jr
import os, requests, time

import BatchSender as bs
import RequestHandler as rh

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

hosts = ["http://128.176.214.100:5000", "http://128.176.214.100:5000"]
job_ids = [0,1]
nJobs = 2
inputs = [wholeSettings, wholeSettings]

# sender = bs.BatchSender(hosts, job_ids, nJobs)
# sender.batchPost(wholeSettings, 0)

#handler = rh.RequestHandler(hosts[0],0)
#handler.postJob(wholeSettings)
#handler.getJob()
#handler.deleteJob()
#print(handler.getResponseContent())

sender = bs.BatchSender(hosts, job_ids, nJobs)
sender.sendJobs(inputs)

# BASE = "http://128.176.214.100:5000/"
# putResponse = requests.post(BASE + "api/"+str(0), json = jr.dict2json(wholeSettings))
# _ = requests.get(BASE + "api/"+str(0))


