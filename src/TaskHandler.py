import sys, os
import shutil as su

import SettingsConverter as sc
import JsonResolver as jr
import JobFormatChecker as jc
import serenipy as spy

class TaskHandler():
    def __init__(self, args):
        self.__args = args
        self.__taskName = ""
        self.__act = []
        self.__env = []
        self.__actNames = []
        self.__envNames = []
        self.__actSettings = []
        self.__envSettings = []
        self.__actDensityMatrix = []
        # self.__actnOcc = []
        # self.__envnOcc = []
        self.__actCoefficients = []
        self.__envDensityMatrix = []
        self.__envCoefficients = []
        self.__actTotEn = []
        self.__envTotEn = []
        self.__nAct = 0
        self.__nEnv = 0
        self.__results = {}
        self.__jobstate = ""
        self.__update = False
        checker = jc.JobFormatChecker(self.__args)
        checker.run()

    def __updateSystems(self):
        for iAct in range(len(self.__actDensityMatrix)):
            if (jr.resolveSCFMode(self.__act[iAct].getSettings().scfMode).upper() == "RESTRICTED"):
                self.__act[iAct].getElectronicStructure_R().getDensityMatrix().set(jr.json2array(self.__actDensityMatrix[iAct]))
            elif (jr.resolveSCFMode(self.__act[iAct].getSettings().scfMode).upper() == "UNRESTRICTED"):
                self.__act[iAct].getElectronicStructure_U().getDensityMatrix().set(jr.json2array(self.__actDensityMatrix[iAct][0]),\
                                                                                   jr.json2array(self.__actDensityMatrix[iAct][1]))
            else: 
                print("Invalid SCFMode!")
        for iEnv in range(len(self.__envDensityMatrix)):
            if (jr.resolveSCFMode(self.__env[iEnv].getSettings().scfMode).upper() == "RESTRICTED"):
                 self.__env[iEnv].getElectronicStructure_R().getDensityMatrix().set(jr.json2array(self.__envDensityMatrix[iEnv]))
            elif (jr.resolveSCFMode(self.__env[iEnv].getSettings().scfMode).upper() == "UNRESTRICTED"):
                 self.__env[iEnv].getElectronicStructure_U().getDensityMatrix().set(jr.json2array(self.__envDensityMatrix[iEnv][0]),\
                                                                                   jr.json2array(self.__envDensityMatrix[iEnv][1]))
            else: 
                print("Invalid SCFMode!")

    def getActiveSystems(self):
        return self.__act

    def getEnvironmentSystems(self):
        return self.__env

    def getTaskInfo(self):
        return self.__args

    def enroll(self):
        actSettingsDict = ""
        envSettingsDict = ""
        for outer, _ in self.__args.items():
            if (outer.upper() == "TASK"):
                self.__taskName = self.__args[outer.upper()]
            elif (outer.upper() in ["ACTIVESYSTEMSETTINGS", "ACTSETTINGS", "SYSTEMSETTINGS"]):
                actSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["ENVIRONMENTSYSTEMSETTINGS", "ENVSETTINGS"]):
                envSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["JOBSTATE","STATE"]):
                self.__jobstate = self.__args[outer.upper()]
            else:
                print("KeyError: Parsed JSON dict has not the correct form in outermost scope!")
                sys.exit()

        for outer, inner in actSettingsDict.items():
            if (outer[0:6].upper() in ["SYSTEM","SYS"] or \
                outer[0:3].upper() in ["SYSTEM","SYS"]):
                converter = sc.SettingsConverter(jr.dict2json(inner))
                self.__actSettings.append(converter.getSerenipySettings())
                self.__actNames.append(outer)
                #write the sent XYZ to file
                #ToDo: create the xyz file in the a scratch directory
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "GEOMETRY"):
                        with open(os.path.join(os.getcwd(),inner[innerinner]), 'w') as file:
                            if ("XYZ" in inner):
                                file.write(inner["XYZ"])
                                file.close()
                            elif ("xyz" in inner):
                                file.write(inner["xyz"])
                                file.close()
                            else: 
                                print("No XYZ file infomation present! Missing key 'xyz' or 'XYZ'!")
                                sys.exit()
                        inner[innerinner] = os.path.join(os.getcwd(),inner[innerinner])
                    #check if any results are already present
                    if (innerinner.upper() == "RESULTS"):
                        for innerinnerinner, _ in innerinner.items():
                            if (innerinnerinner.upper() in ["TOTALENERGY"]):
                                self.__actTotEn.append(innerinner[innerinnerinner])
                            #restricted case 
                            if (jr.resolveSCFMode(self.__actSettings[self.__nAct].scfMode).upper() == "RESTRICTED"):
                                if (innerinnerinner.upper() == "DENSITYMATRIX"):
                                    self.__actDensityMatrix.append(innerinner[innerinnerinner])
                                if (innerinnerinner.upper() in ["COEFFICIENTMATRIX", "COEFFICIENTS"]):
                                    self.__actCoefficients.append(innerinner[innerinnerinner])
                            #unrestricted case
                            if (jr.resolveSCFMode(self.__actSettings[self.__nAct].scfMode).upper() == "UNRESTRICTED"):
                                self.__actDensityMatrix.append(["", ""])
                                self.__actCoefficients.append(["", ""])
                                if (innerinnerinner.upper() in ["DENSITYMATRIXALPHA"]):
                                    self.__actDensityMatrix[self.__nAct][0] = innerinner[innerinnerinner]
                                if (innerinnerinner.upper() in ["DENSITYMATRIXBETA"]):
                                    self.__actDensityMatrix[self.__nAct][1] = innerinner[innerinnerinner]
                                if (innerinnerinner.upper() in ["COEFFICIENTMATRIXALPHA"]):
                                    self.__actCoefficients[self.__nAct][0] = innerinner[innerinnerinner]
                                if (innerinnerinner.upper() in ["COEFFICIENTMATRIXBETA"]):
                                    self.__actCoefficients[self.__nAct][1] = innerinner[innerinnerinner]
                self.__nAct += 1
            else:
                print("KeyError: Parsed JSON dict has not the correct form in outermost scope!")
                sys.exit()

        if (envSettingsDict != ""):
            for outer, inner in envSettingsDict.items():
                if (outer[0:6].upper() in ["SYSTEM","SYS"] or \
                    outer[0:3].upper() in ["SYSTEM","SYS"]):
                    converter = sc.SettingsConverter(jr.dict2json(inner))
                    self.__envSettings.append(converter.getSerenipySettings())
                    self.__envNames.append(outer)
                    #write the sent XYZ to file
                    #ToDo: create the xyz file in the a scratch directory
                    for innerinner, _ in inner.items():
                        if (innerinner.upper() == "GEOMETRY"):
                            with open(os.path.join(os.getcwd(),inner[innerinner]), 'w') as file:
                                if ("XYZ" in inner):
                                    file.write(inner["XYZ"])
                                    file.close()
                                elif ("xyz" in inner):
                                    file.write(inner["xyz"])
                                    file.close()
                                else: 
                                    print("No XYZ file infomation present! Missing key 'xyz' or 'XYZ'!")
                                    sys.exit()
                            inner[innerinner] = os.path.join(os.getcwd(),inner[innerinner])
                        #check if any results are already present
                        if (innerinner.upper() == "RESULTS"):
                            self.__update = True
                            for innerinnerinner, _ in innerinner.items():
                                if (innerinnerinner.upper() in ["TOTALENERGY"]):
                                    self.__envTotEn.append(innerinner[innerinnerinner])
                                #restricted case 
                                if (jr.resolveSCFMode(self.__envSettings[self.__nEnv].scfMode).upper() == "RESTRICTED"):
                                    if (innerinnerinner.upper() == "DENSITYMATRIX"):
                                        self.__envDensityMatrix.append(innerinner[innerinnerinner])
                                    if (innerinnerinner.upper() in ["COEFFICIENTMATRIX", "COEFFICIENTS"]):
                                        self.__envCoefficients.append(innerinner[innerinnerinner])
                                #unrestricted case
                                if (jr.resolveSCFMode(self.__envSettings[self.__nEnv].scfMode).upper() == "UNRESTRICTED"):
                                    self.__envDensityMatrix.append(["", ""])
                                    self.__envCoefficients.append(["", ""])
                                    if (innerinnerinner.upper() in ["DENSITYMATRIXALPHA"]):
                                        self.__envDensityMatrix[self.__nEnv][0] = innerinner[innerinnerinner]
                                    if (innerinnerinner.upper() in ["DENSITYMATRIXBETA"]):
                                        self.__envDensityMatrix[self.__nEnv][1] = innerinner[innerinnerinner]
                                    if (innerinnerinner.upper() in ["COEFFICIENTMATRIXALPHA"]):
                                        self.__envCoefficients[self.__nEnv][0] = innerinner[innerinnerinner]
                                    if (innerinnerinner.upper() in ["COEFFICIENTMATRIXBETA"]):
                                        self.__envCoefficients[self.__nEnv][1] = innerinner[innerinnerinner]
                    self.__nEnv += 1
                else:
                    print("KeyError: Parsed JSON dict has not the correct form in outermost scope!")
                    sys.exit()
        #create systems from gathered settings            
        for act in self.__actSettings:
            self.__act.append(spy.System(act))
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self):
        if (len(self.__act) == 0):
            print("There is NO active system!!")
            sys.exit()
        for setting in self.__actSettings:
            if (jr.resolveSCFMode(setting.scfMode).upper() == "UNRESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            else: 
                print("Invalid SCFMode!")
                sys.exit()
        if (len(self.__actDensityMatrix) > 0 and self.__update):
            self.__updateSystems()
        task = jr.resolveTask(mode, self.__taskName, self.__act, self.__env)
        task.run()
        self.__results = self.processResults()
        #write database entry here
        
        self.__jobstate = "FIN"

    def processResults(self):
        results = {}
        resDummy = {"TOTALENERGY"      : 0,
                    "DENSITYMATRIX"    : 0,
                    "COEFFICIENTMATRIX": 0
        }
        unresDummy = {"TOTALENERGY"            : 0,
                      "DENSITYMATRIXALPHA"     : 0,
                      "DENSITYMATRIXBETA"      : 0,
                      "COEFFICIENTMATRIXALPHA" : 0,
                      "COEFFICIENTMATRIXBETA"  : 0
        }
        #active systems
        systemCounter = 0
        for act in self.__act:
            scfMode = jr.resolveSCFMode(act.getSettings().scfMode).upper()
            if (scfMode == "RESTRICTED"):
                sysresults = resDummy.copy()
                sysresults["TOTALENERGY"] =  act.getEnergy()
                sysresults["DENSITYMATRIX"] = jr.array2json(act.getElectronicStructure_R().getDensityMatrix().total())
                sysresults["COEFFICIENTMATRIX"] = jr.array2json(act.getElectronicStructure_R().coeff())
                results.update({self.__actNames[systemCounter] : sysresults})
            elif (scfMode == "UNRESTRICTED"):
                sysresults = unresDummy.copy()
                sysresults["TOTALENERGY"] =  act.getEnergy()
                sysresults["DENSITYMATRIXALPHA"] = jr.array2json(act.getElectronicStructure_U().getDensityMatrix().alpha())
                sysresults["DENSITYMATRIXBETA"] = jr.array2json(act.getElectronicStructure_U().getDensityMatrix().beta())
                sysresults["COEFFICIENTMATRIXALPHA"] = jr.array2json(act.getElectronicStructure_U().alphaCoeff())
                sysresults["COEFFICIENTMATRIXBETA"] = jr.array2json(act.getElectronicStructure_U().betaCoeff())
                results.update({self.__actNames[systemCounter] : sysresults})
            else:
                print("SCFMode invalid!")
            systemCounter += 1

        #environment systems
        systemCounter = 0
        for env in self.__env:
            scfMode = jr.resolveSCFMode(env.getSettings().scfMode).upper()
            if (scfMode == "RESTRICTED"):
                sysresults = resDummy.copy()
                sysresults["TOTALENERGY"] =  env.getEnergy()
                sysresults["DENSITYMATRIX"] = jr.array2json(env.getElectronicStructure_R().getDensityMatrix().total())
                sysresults["COEFFICIENTMATRIX"] = jr.array2json(env.getElectronicStructure_R().coeff())
                results.update({self.__envNames[systemCounter] : sysresults})
            elif (scfMode == "UNRESTRICTED"):
                sysresults = unresDummy.copy()
                sysresults["TOTALENERGY"] =  env.getEnergy()
                sysresults["DENSITYMATRIXALPHA"] = jr.array2json(env.getElectronicStructure_U().getDensityMatrix().alpha())
                sysresults["DENSITYMATRIXBETA"] = jr.array2json(env.getElectronicStructure_U().getDensityMatrix().beta())
                sysresults["COEFFICIENTMATRIXALPHA"] = jr.array2json(env.getElectronicStructure_U().alphaCoeff())
                sysresults["COEFFICIENTMATRIXBETA"] = jr.array2json(env.getElectronicStructure_U().betaCoeff())
                results.update({self.__envNames[systemCounter] : sysresults})
            else:
                print("SCFMode invalid!")
            systemCounter += 1
        return results

    def cleanUp(self):
        for act in self.__actSettings:
            os.remove(act.geometry)
            if (os.path.exists(os.path.join(act.name))):
                su.rmtree(os.path.join(act.name))
        for env in self.__envSettings:
            os.remove(env.geometry)
            if (os.path.exists(os.path.join(env.name))):
                su.rmtree(os.path.join(env.name))
        
    def getJobState(self):
        return self.__jobstate
