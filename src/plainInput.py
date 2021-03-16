import os
import JsonResolver as jr

class InputCreator():
    def __init__(self, filename, onSame = True):
        self.__file = filename
        self.__systemDicts = self.__readSystems()
        self.__taskDicts = self.__readTasks()

    def __eraseDefaults(self, json, key = ""):
        for k in list(json.keys()):
            if isinstance(json[k], dict):
                self.__eraseDefaults(json[k], k)
            else:
                if json[k] == "":
                    json.pop(k, None)

    def __readTasks(self):
        taskInput = False
        taskDicts = []
        # taskDummy = 
        with open(self.__file, 'r') as inp:
            content = inp.readlines()
            for line in content:
                items = line.strip().split()
                if ("+TASK" in [item.upper() for item in items]):
                    taskInput = True
                elif ("-TASK" in [item.upper() for item in items]):
                    taskInput = False

                if (taskInput):
                    print([item.upper() for item in items])
        return None

    def __readSystems(self):
        systemDicts = []
        sysInput = False
        dftInput = False
        basisInput = False
        scfInput = False
        gridInput = False
        # efieldInput = False
        systemDummy = {"NAME" : "",
                       "GEOMETRY" : "",
                       "XYZ" : "",
                       "METHOD" : "",
                       "SCFMODE" : "",
                       "CHARGE" : "",
                       "SPIN" : "",
                       "DFT" : "",
                       "BASIS" : "",
                       "SCF" : "",
                       "GRID" : "",
                       "EFIELD" : ""
                       }
        dftDummy = {"FUNCTIONAL" : "",
                    "DENSITYFITTING" : "",
                    "DISPERSION" : ""
                    }
        scfDummy = {"INITIALGUESS" : "",
                    "MAXCYCLES" : "",
                    "WRITERESTART" : "",
                    "ENERGYTHRESHOLD" : "",
                    "RMSDTHRESHOLD" : "",
                    "DAMPING" : "",
                    "SERIESDAMPINGSTART" : "",
                    "SERIESDAMPINGEND" : "",
                    "SERIESDAMPINGSTEP" : "",
                    "SERIESDAMPINGINITIALSTEPS" : "",
                    "STATICDAMPINGFACTOR" : "",
                    "ENDDAMPERR" : "",
                    "USELEVELSHIFT" : "",
                    "USEOFFDIAGLEVELSHIFT" : "",
                    "MINIMUMLEVELSHIFT" : "",
                    "DIISFLUSH" : "",
                    "DISSSTARTERROR" : "",
                    "DISSMAXSTORE" : "",
                    "DIISTHRESHOLD" : "",
                    "USEADIIS" : ""
                    }
        basisDummy = { "LABEL" : ""}
        gridDummy = {"GRIDTYPE" : "",
                     "RADIALGRIDTYPE" : "",
                     "SPHERICALGRIDTYPE" : "",
                     "BLOCKSIZE" : "",
                     "ACCURACY" : "",
                     "SMALLGRIDACCURACY" : "",
                     "BLOCKAVETHRESHOLD" : "",
                     "BASFUNCRADIALTHRESHOLD" : "",
                     "WEIGHTTHRESHOLD" : "",
                     "SMOOTHING" : ""
                     }      
        with open(self.__file, 'r') as inp:
            content = inp.readlines()
            for line in content:
                items = line.strip().split()
                if ("+SYSTEM" in [item.upper() for item in items]):
                    sysInput = True
                    systemDict = systemDummy.copy()
                    continue
                elif ("-SYSTEM" in [item.upper() for item in items]):
                    sysInput = False
                    systemDicts.append(systemDict.copy())
                if(sysInput):
                    if(items[0].upper() == "NAME"):
                        systemDict["NAME"] = items[1] 
                    if(items[0].upper() == "METHOD"):
                        systemDict["METHOD"] = items[1]
                    if(items[0].upper() == "SCFMODE"):
                        systemDict["SCFMODE"] = items[1]
                    if(items[0].upper() == "CHARGE"):
                        systemDict["CHARGE"] = items[1]
                    if(items[0].upper() == "SPIN"):
                        systemDict["SPIN"] = items[1]
                    if(items[0].upper() == "+DFT"):
                        dftInput = True
                        dftDict = dftDummy.copy()
                    elif(items[0].upper() == "-DFT"): 
                        dftInput = False
                        systemDict["DFT"] = dftDict.copy()
                    if(items[0].upper() == "+BASIS"):
                        basisInput = True
                        basisDict = basisDummy.copy()
                    elif(items[0].upper() == "-BASIS"): 
                        basisInput = False
                        systemDict["BASIS"] = basisDict.copy()
                    if(items[0].upper() == "+SCF"):
                        scfInput = True
                        scfDict = scfDummy.copy()
                    elif(items[0].upper() == "-SCF"): 
                        scfInput = False
                        systemDict["SCF"] = scfDict.copy()
                    if(items[0].upper() == "+GRID"):
                        gridInput = True
                        gridDict = gridDummy.copy()
                    elif(items[0].upper() == "-GRID"): 
                        gridInput = False
                        systemDict["GRID"] = gridDict.copy()
                    # if(items[0].upper() == "+EFIELD"):
                    #     efieldInput = True
                    #     efieldDict = efieldDummy.copy()
                    # elif(items[0].upper() == "-EFIELD"): 
                    #     efieldInput = False
                    #     systemDict["EFIELD"] = efieldDict.copy()
                    if(items[0].upper() == "GEOMETRY"):
                        systemDict["GEOMETRY"] = items[1]
                        with open(os.path.join(items[1]), 'r') as file:
                            data = file.read()
                            file.close()
                        systemDict["XYZ"] = data
                    if(dftInput):
                        if (items[0].upper() == "FUNCTIONAL"):
                            dftDict["FUNCTIONAL"] = items[1]
                        if (items[0].upper() == "DENSITYFITTING"):
                            dftDict["DENSITYFITTING"] = items[1]
                        if (items[0].upper() == "DISPERSION"):
                            dftDict["DISPERSION"] = items[1]
                    if(scfInput):
                        if(items[0].upper() == "INITIALGUESS"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "MAXCYCLES"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "WRITERESTART"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "ENERGYTHRESHOLD"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "RMSDTHRESHOLD"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "DAMPING"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SERIESDAMPINGSTART"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SERIESDAMPINGEND"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SERIESDAMPINGSTEP"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SERIESDAMPINGINITIALSTEPS"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "STATICDAMPINGFACTOR"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "ENDDAMPERR"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "USELEVELSHIFT"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "USEOFFDIAGLEVELSHIFT"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "MINIMUMLEVELSHIFT"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "DIISFLUSH"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "DISSSTARTERROR"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "DISSMAXSTORE"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "DIISTHRESHOLD"):
                            scfDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "USEADIIS"):
                            scfDict[items[0].upper()] = items[1]
                    if(basisInput):
                        if(items[0].upper() == "LABEL"):
                            basisDict[items[0].upper()] = items[1]
                    if(gridInput):
                        if(items[0].upper() == "GRIDTYPE"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "RADIALGRIDTYPE"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SPHERICALGRIDTYPE"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "BLOCKSIZE"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "ACCURACY"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SMALLGRIDACCURACY"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "BLOCKAVETHRESHOLD"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "BASFUNCRADIALTHRESHOLD"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "WEIGHTTHRESHOLD"):
                            gridDict[items[0].upper()] = items[1]
                        if(items[0].upper() == "SMOOTHING"):
                            gridDict[items[0].upper()] = items[1]
        inp.close()
        for item in systemDicts:
            self.__eraseDefaults(item)
        return systemDicts






creator = InputCreator("inp_KSDFT")