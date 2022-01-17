import json
import numpy


def dict2json(dct):
    dct = json.dumps(dct)
    return json.loads(dct)


def array2json(dct):
    return json.dumps(dct.tolist())


def json2array(dct):
    return numpy.array(json.loads(dct))


def find(key, value):
    for k, v in (value.items() if isinstance(value, dict) else
                 enumerate(value) if isinstance(value, list) else []):
        if k == key:
            yield v
        elif isinstance(v, (dict, list)):
            for result in find(key, v):
                yield result


def input2json(filename):
    with open(filename, "r") as inp:
        content = inp.readlines()
    inp.close()
    systemblock = False
    dftblock = False
    basisblock = False
    scfblock = False
    gridblock = False
    efieldblock = False
    taskblock = False
    embeddingblock = False
    systems = {}
    tasks = {}
    iSys = 0
    iTask = 0
    for line in content:
        values = line.strip().split()
        if (len(values) > 0 and values[0][0] == "#"):
            continue
        if (len(values) > 0 and values[0].upper() == "+SYSTEM"):
            systemblock = True
            systems[iSys] = {}
            continue
        if (systemblock and len(values) > 0 and values[0].upper() == "-SYSTEM"):
            systemblock = False
            iSys += 1
            continue
        if (len(values) > 0 and values[0].upper() == "+DFT"):
            systems[iSys]["DFT"] = {}
            dftblock = True
            systemblock = False
            continue
        if (dftblock and len(values) > 0 and values[0].upper() == "-DFT"):
            dftblock = False
            systemblock = True
            continue
        if (len(values) > 0 and values[0].upper() == "+BASIS"):
            systems[iSys]["BASIS"] = {}
            basisblock = True
            systemblock = False
            continue
        if (basisblock and len(values) > 0 and values[0].upper() == "-BASIS"):
            basisblock = False
            systemblock = True
            continue
        if (len(values) > 0 and values[0].upper() == "+SCF"):
            systems[iSys]["SCF"] = {}
            scfblock = True
            systemblock = False
            continue
        if (scfblock and len(values) > 0 and values[0].upper() == "-SCF"):
            scfblock = False
            systemblock = True
            continue
        if (len(values) > 0 and values[0].upper() == "+GRID"):
            systems[iSys]["GRID"] = {}
            gridblock = True
            systemblock = False
            continue
        if (gridblock and len(values) > 0 and values[0].upper() == "-GRID"):
            gridblock = False
            systemblock = True
            continue
        if (len(values) > 0 and values[0].upper() == "+EFIELD"):
            systems[iSys]["EFIELD"] = {}
            efieldblock = True
            systemblock = False
            continue
        if (efieldblock and len(values) > 0 and values[0].upper() == "-EFIELD"):
            efieldblock = False
            systemblock = True
            continue
        if (len(values) > 0 and values[0].upper() == "+TASK"):
            taskblock = True
            tasks[iTask] = {}
            tasks[iTask]["TASK"] = values[1].upper()
            iAct = 0
            iEnv = 0
            tasks[iTask]["EMB"] = {}
            tasks[iTask]["ACT"] = {}
            tasks[iTask]["ENV"] = {}
            continue
        if (taskblock and len(values) > 0 and values[0].upper() == "-TASK"):
            taskblock = False
            iTask += 1
        if (len(values) > 0 and values[0].upper() == "+EMB"):
            taskblock = False
            embeddingblock = True
            continue
        if (embeddingblock and len(values) > 0 and values[0].upper() == "-EMB"):
            taskblock = True
            embeddingblock = False
            continue
        if (systemblock):
            if (len(values) > 1):
                if (values[0].upper() == "GEOMETRY"):
                    with open(values[1], 'r') as file:
                        data = file.read()
                    file.close()
                    systems[iSys]["XYZ"] = data
                    systems[iSys][values[0].upper()] = str(iSys)+".xyz"
                elif (values[0].upper() == "NAME"):
                    systems[iSys]["NAME"] = values[1]
                else:
                    systems[iSys][values[0].upper()] = values[1].upper()
        if (dftblock):
            systems[iSys]["DFT"][values[0].upper()] = values[1].upper()
        if (basisblock):
            systems[iSys]["BASIS"][values[0].upper()] = values[1].upper()
        if (scfblock):
            systems[iSys]["SCF"][values[0].upper()] = values[1].upper()
        if (gridblock):
            systems[iSys]["GRID"][values[0].upper()] = values[1].upper()
        if (efieldblock):
            systems[iSys]["EFIELD"][values[0].upper()] = values[1].upper()
        if (taskblock):
            if (values[0].upper() == "ACT" or values[0].upper() == "ACTIVE" or values[0].upper() == "SYSTEM"):
                tasks[iTask]["ACT"][iAct] = values[1]
                iAct += 1
            elif (values[0].upper() == "ENV" or values[0].upper() == "ENVIRONMENT"):
                tasks[iTask]["ENV"][iEnv] = values[1]
                iEnv += 1
            else:
                tasks[iTask][values[0].upper()] = values[1].upper()
        if (embeddingblock):
            tasks[iTask]["EMB"][values[0].upper()] = values[1].upper()
    taskJsons = []
    for iTask in tasks.keys():
        actNames = list(list(find("ACT", tasks[iTask]))[0].values())
        envNames = list(list(find("ENV", tasks[iTask]))[0].values())
        actSettings = {}
        envSettings = {}
        wholeSettings = {}
        for actName in actNames:
            for iSys in systems.keys():
                sysname = list(find("NAME", systems[iSys]))[0]
                if (sysname == actName):
                    actSettings["SYS"+str(iSys)] = systems[iSys]
        for envName in envNames:
            for iSys in systems.keys():
                sysname = list(find("NAME", systems[iSys]))[0]
                if (sysname == envName):
                    envSettings["SYS"+str(iSys)] = systems[iSys]

        wholeSettings["TASK"] = tasks[iTask]["TASK"]
        wholeSettings["TASK_SETTINGS"] = {}
        for setting in tasks[iTask].keys():
            if (setting == "ACT" or setting == "ENV" or setting == "TASK"):
                continue
            
            # print(setting, wholeSettings, tasks[iTask][setting])
            wholeSettings["TASK_SETTINGS"][setting] = tasks[iTask][setting]
        
        wholeSettings["ID"] = iTask
        wholeSettings["ACT"] = actSettings
        wholeSettings["ENV"] = envSettings
        taskJsons.append(wholeSettings)
    return dict2json(taskJsons)


def dismemberJson(json):
    actSettingsDict = list(find("ACT", json))[0]
    try:
        envSettingsDict = list(find("ENV", json))[0]
    except:
        envSettingsDict = {}
    try:
        taskSettingsDict = list(find("TASK_SETTINGS", json))[0]
    except:
        taskSettingsDict = {}
    taskName = list(find("TASK", json))[0]
    return taskName, taskSettingsDict, actSettingsDict, envSettingsDict
