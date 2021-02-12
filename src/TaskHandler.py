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
        self.__actSettings = []
        self.__envSettings = []
        self.__actDensityMatrix = []
        self.__actnOcc = []
        self.__envnOcc = []
        self.__actCoefficients = []
        self.__envDensityMatrix = []
        self.__envCoefficients = []
        self.__nAct = 0
        self.__nEnv = 0
        checker = jc.JobFormatChecker(self.__args)
        checker.run()

    def __updateSystems(self):
        for iAct in range(len(self.__actDensityMatrix)):
            if (jr.resolveSCFMode(self.__act[iAct].getSettings().scfMode).upper() == "RESTRICTED"):
                self.__act[iAct].getElectronicStructure_R().getDensityMatrix().set(jr.json2array(self.__actDensityMatrix[iAct]))
            elif (jr.resolveSCFMode(self.__act[iAct].getSettings().scfMode).upper() == "UNRESTRICTED"):
                # es = spy.ElectronicStructure_U(self.__act[iAct], jr.json2array(self.__actDensityMatrix[iAct][0]),
                #                                jr.json2array(self.__actDensityMatrix[iAct][1]), int(self.__actnOcc[iAct][0]), int(self.__actnOcc[iAct][1]))
                # self.__act[iAct].setElectronicStructure_U(es)

                self.__act[iAct].getElectronicStructure_U().getDensityMatrix().set(jr.json2array(self.__actDensityMatrix[iAct][0]),\
                                                                                  jr.json2array(self.__actDensityMatrix[iAct][1]))
            else: 
                print("Invalid SCFMode!")
        for iEnv in range(len(self.__envDensityMatrix)):
            if (jr.resolveSCFMode(self.__env[iEnv].getSettings().scfMode).upper() == "RESTRICTED"):
                 self.__env[iEnv].getElectronicStructure_R().getDensityMatrix().set(jr.json2array(self.__envDensityMatrix[iEnv]))
                # es = spy.ElectronicStructure_R(self.__act[iAct], jr.json2array(self.__actDensityMatrix[iAct]), int(self.__envnOcc[iEnv]))
                # self.__act[iAct].setElectronicStructure_R(es)
            elif (jr.resolveSCFMode(self.__env[iEnv].getSettings().scfMode).upper() == "UNRESTRICTED"):
                 self.__env[iEnv].getElectronicStructure_U().getDensityMatrix().set(jr.json2array(self.__envDensityMatrix[iEnv][0]),\
                                                                                   jr.json2array(self.__envDensityMatrix[iEnv][1]))
                # es = spy.ElectronicStructure_U(self.__act[iAct], jr.json2array(self.__actDensityMatrix[iAct][0]),
                #                                jr.json2array(self.__actDensityMatrix[iAct][1]), int(self.__envnOcc[iEnv][0]), int(self.__envnOcc[iEnv][1]))
                # self.__act[iAct].setElectronicStructure_U(es)
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
        jobstate = ""
        for outer, _ in self.__args.items():
            if (outer.upper() == "TASK"):
                self.__taskName = self.__args[outer.upper()]
            elif (outer.upper() in ["ACTIVESYSTEMSETTINGS", "ACTSETTINGS", "SYSTEMSETTINGS"]):
                actSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["ENVIRONMENTSYSTEMSETTINGS", "ENVSETTINGS"]):
                envSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["JOBSTATE","STATE"]):
                jobstate = self.__args[outer.upper()]
            else:
                print("KeyError: Parsed JSON dict has not the correct form in outermost scope!")
                sys.exit()

        for outer, _ in actSettingsDict.items():
            if (outer[0:6].upper() in ["SYSTEM","SYS"] and \
                outer[0:3].upper() in ["SYSTEM","SYS"]):
                print(outer)
                # converter = sc.SettingsConverter(jr.dict2json(outer))
            
        




            # elif (inner["system"]["type"].lower() == "active" or inner["system"]["type"].lower() == "act"):
            #     converter = sc.SettingsConverter(jr.dict2json(inner))
            #     self.__actSettings.append(converter.getSerenipySettings())
            #     #check if densityMatrix and coefficients are sent
            #     if ("densityMatrix" in inner):
            #         self.__actDensityMatrix.append(inner["densityMatrix"])
            #     if ("densityMatrixAlpha" in inner):
            #         self.__actDensityMatrix.append([])
            #         self.__actDensityMatrix[self.__nAct].append(inner["densityMatrixAlpha"])
            #     if ("densityMatrixBeta" in inner):
            #         self.__actDensityMatrix[self.__nAct].append(inner["densityMatrixBeta"])
            #     if ("coefficients" in inner):
            #         self.__actCoefficients.append(inner["coefficients"])
            #     if ("coefficientsAlpha" in inner):
            #         self.__actCoefficients.append([])
            #         self.__actCoefficients[self.__nAct].append(inner["coefficientsAlpha"])
            #     if ("coefficientsBeta" in inner):
            #         self.__actCoefficients[self.__nAct].append(inner["coefficientsBeta"])
            #     self.__nAct += 1

            # elif (inner["system"]["type"].lower() == "environment" or inner["system"]["type"].lower() == "env"):
            #     converter = sc.SettingsConverter(jr.dict2json(inner))
            #     self.__envSettings.append(converter.getSerenipySettings())
            #     #check if densityMatrix and coefficients are sent
            #     if ("densityMatrix" in inner):
            #         self.__envDensityMatrix.append(inner["densityMatrix"])
            #     if ("densityMatrixAlpha" in inner):
            #         self.__envDensityMatrix.append([])
            #         self.__envDensityMatrix[self.__nEnv].append(inner["densityMatrixAlpha"])
            #     if ("densityMatrixBeta" in inner):
            #         self.__envDensityMatrix[self.__nEnv].append(inner["densityMatrixBeta"])
            #     if ("coefficients" in inner):
            #         self.__envCoefficients.append(inner["coefficients"])
            #     if ("coefficientsAlpha" in inner):
            #         self.__envCoefficients.append([])
            #         self.__envCoefficients[self.__nEnv].append(inner["coefficientsAlpha"])
            #     if ("coefficientsBeta" in inner):
            #         self.__envCoefficients[self.__nEnv].append(inner["coefficientsBeta"])
            #     self.__nEnv += 1
            # else:
            #     print("System has no type! E.g. enter 'type : active' in the system block in the input!")
            #     sys.exit()

        for act in self.__actSettings:
            act = spy.System(act)
            self.__act.append(act)

        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self):
        if (len(self.__actSettings) == 0):
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
        if (len(self.__actDensityMatrix) > 0):
            self.__updateSystems()
        task = jr.resolveTask(mode, self.__taskName, self.__act, self.__env)
        task.run()

    def processResults(self):
        results = {}
        systemCounter = 0
        for act in self.__act:
            scfMode = jr.resolveSCFMode(act.getSettings().scfMode).upper()
            if (scfMode == "RESTRICTED"):
                actDensityMatrix = act.getElectronicStructure_R().getDensityMatrix().total()
                actCoefficients = act.getElectronicStructure_R().coeff()
                actTotalEnergy = act.getEnergy()
                results[systemCounter] = {"densityMatrix" : jr.array2json(actDensityMatrix),
                                          "coefficients"  : jr.array2json(actCoefficients),
                                          "totalEnergy"   : actTotalEnergy}
            elif (scfMode == "UNRESTRICTED"):
                actDensityMatrixAlpha = act.getElectronicStructure_U().getDensityMatrix().alpha()
                actDensityMatrixBeta = act.getElectronicStructure_U().getDensityMatrix().beta()
                actCoefficientsAlpha = act.getElectronicStructure_U().alphaCoeff()
                actCoefficientsBeta = act.getElectronicStructure_U().betaCoeff()
                actTotalEnergy = act.getEnergy()
                results[systemCounter] = {"densityMatrixAlpha" : jr.array2json(actDensityMatrixAlpha),
                                          "densityMatrixBeta"  : jr.array2json(actDensityMatrixBeta), 
                                          "coefficientsAlpha"  : jr.array2json(actCoefficientsAlpha),
                                          "coefficientsBeta"   : jr.array2json(actCoefficientsBeta),
                                          "totalEnergy"        : actTotalEnergy}
            else:
                print("SCFMode invalid!")
            systemCounter += 1
        return results

    def cleanUp(self):
        for act in self.__actSettings:
            #os.remove(act.geometry)
            if (os.path.exists(os.path.join(act.path, act.name))):
                su.rmtree(os.path.join(act.path, act.name))
        for env in self.__envSettings:
            #os.remove(env.geometry)
            if (os.path.exists(os.path.join(env.path, env.name))):
                su.rmtree(os.path.join(env.path, env.name))
