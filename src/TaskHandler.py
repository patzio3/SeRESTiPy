import os
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
        self.__nAct = 0
        self.__nEnv = 0

    def jsonValid(self):
        checker = jc.JobFormatChecker(self.__args)
        return checker.run()

    def getActiveSystems(self):
        return self.__act

    def getEnvironmentSystems(self):
        return self.__env

    def getTaskInfo(self):
        return self.__args

    def enroll(self):
        print("LOL!!!!1ELF!!")
        actSettingsDict = ""
        envSettingsDict = ""
        for outer, _ in self.__args.items():
            if (outer.upper() == "TASK"):
                self.__taskName = self.__args[outer.upper()]
            elif (outer.upper() in ["ACTIVESYSTEMSETTINGS", "ACTSETTINGS", "ACT"]):
                actSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["ENVIRONMENTSYSTEMSETTINGS", "ENVSETTINGS", "ENV"]):
                envSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["ID"]):
                continue
        print("LOL!!!!1ELF!!")
        for outer, inner in actSettingsDict.items():
            if (outer[0:6].upper() in ["SYSTEM", "SYS"] or
                    outer[0:3].upper() in ["SYSTEM", "SYS"]):
                converter = sc.SettingsConverter(jr.dict2json(inner))
                self.__actSettings.append(converter.getSerenipySettings())
                self.__actNames.append(outer)
                # write the sent XYZ to file
                # ToDo: create the xyz file in the a scratch directory
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "GEOMETRY"):
                        with open(os.path.join(os.getcwd(), inner[innerinner]), 'w') as file:
                            if ("XYZ" in inner):
                                print(inner["XYZ"])
                                file.write(inner["XYZ"])
                                file.close()
                        inner[innerinner] = os.path.join(
                            os.getcwd(), inner[innerinner])
                self.__nAct += 1
        print("LOL!!!!1ELF!!")
        if (envSettingsDict != ""):
            for outer, inner in envSettingsDict.items():
                if (outer[0:6].upper() in ["SYSTEM"] or
                        outer[0:3].upper() in ["SYS"]):
                    converter = sc.SettingsConverter(jr.dict2json(inner))
                    self.__envSettings.append(converter.getSerenipySettings())
                    self.__envNames.append(outer)
                    # write the sent XYZ to file
                    # ToDo: create the xyz file in the a scratch directory
                    for innerinner, _ in inner.items():
                        if (innerinner.upper() == "GEOMETRY"):
                            with open(os.path.join(os.getcwd(), inner[innerinner]), 'w') as file:
                                if ("XYZ" in inner):
                                    print(inner["XYZ"])
                                    file.write(inner["XYZ"])
                                    file.close()
                    self.__nEnv += 1
        # create systems from gathered settings
        print("LOL!!!!1ELF!!")
        for act in self.__actSettings:
            print(act)
            self.__act.append(spy.System(act))
        print("LOL!!!!1ELF!!")
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self, job_id):
        for setting in self.__actSettings:
            if (jr.resolveSCFMode(setting.scfMode).upper() == "UNRESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
        task = jr.resolveTask(mode, self.__taskName, self.__act, self.__env)
        task.run()

    # def processResults(self):
    #     results = {}
    #     resDummy = {"TOTALENERGY": 0,
    #                 "DENSITYMATRIX": 0,
    #                 "COEFFICIENTMATRIX": 0
    #                 }
    #     unresDummy = {"TOTALENERGY": 0,
    #                   "DENSITYMATRIXALPHA": 0,
    #                   "DENSITYMATRIXBETA": 0,
    #                   "COEFFICIENTMATRIXALPHA": 0,
    #                   "COEFFICIENTMATRIXBETA": 0
    #                   }
    #     # active systems
    #     systemCounter = 0
    #     for act in self.__act:
    #         scfMode = jr.resolveSCFMode(act.getSettings().scfMode).upper()
    #         if (scfMode == "RESTRICTED"):
    #             sysresults = resDummy.copy()
    #             sysresults["TOTALENERGY"] = act.getEnergy()
    #             sysresults["DENSITYMATRIX"] = act.getElectronicStructure_R(
    #             ).getDensityMatrix().total()
    #             sysresults["COEFFICIENTMATRIX"] = act.getElectronicStructure_R(
    #             ).coeff()
    #             results.update({self.__actNames[systemCounter]: sysresults})
    #         elif (scfMode == "UNRESTRICTED"):
    #             sysresults = unresDummy.copy()
    #             sysresults["TOTALENERGY"] = act.getEnergy()
    #             sysresults["DENSITYMATRIXALPHA"] = act.getElectronicStructure_U(
    #             ).getDensityMatrix().alpha()
    #             sysresults["DENSITYMATRIXBETA"] = act.getElectronicStructure_U(
    #             ).getDensityMatrix().beta()
    #             sysresults["COEFFICIENTMATRIXALPHA"] = act.getElectronicStructure_U(
    #             ).alphaCoeff()
    #             sysresults["COEFFICIENTMATRIXBETA"] = act.getElectronicStructure_U(
    #             ).betaCoeff()
    #             results.update({self.__actNames[systemCounter]: sysresults})
    #         else:
    #             print("SCFMode invalid!")
    #         systemCounter += 1

    #     # environment systems
    #     systemCounter = 0
    #     for env in self.__env:
    #         scfMode = jr.resolveSCFMode(env.getSettings().scfMode).upper()
    #         if (scfMode == "RESTRICTED"):
    #             sysresults = resDummy.copy()
    #             sysresults["TOTALENERGY"] = env.getEnergy()
    #             sysresults["DENSITYMATRIX"] = env.getElectronicStructure_R(
    #             ).getDensityMatrix().total()
    #             sysresults["COEFFICIENTMATRIX"] = env.getElectronicStructure_R(
    #             ).coeff()
    #             results.update({self.__envNames[systemCounter]: sysresults})
    #         elif (scfMode == "UNRESTRICTED"):
    #             sysresults = unresDummy.copy()
    #             sysresults["TOTALENERGY"] = env.getEnergy()
    #             sysresults["DENSITYMATRIXALPHA"] = env.getElectronicStructure_U(
    #             ).getDensityMatrix().alpha()
    #             sysresults["DENSITYMATRIXBETA"] = env.getElectronicStructure_U(
    #             ).getDensityMatrix().beta()
    #             sysresults["COEFFICIENTMATRIXALPHA"] = env.getElectronicStructure_U(
    #             ).alphaCoeff()
    #             sysresults["COEFFICIENTMATRIXBETA"] = env.getElectronicStructure_U(
    #             ).betaCoeff()
    #             results.update({self.__envNames[systemCounter]: sysresults})
    #         else:
    #             print("SCFMode invalid!")
    #         systemCounter += 1
    #     return results

    def cleanUp(self):
        for act in self.__actSettings:
            try:
                os.remove(act.geometry)
            except:
                pass
            if (os.path.exists(os.path.join(act.name))):
                su.rmtree(os.path.join(act.name))
        for env in self.__envSettings:
            try:
                os.remove(env.geometry)
            except:
                pass
            if (os.path.exists(os.path.join(env.name))):
                su.rmtree(os.path.join(env.name))

    def getActNames(self):
        return self.__actNames

    def getEnvNames(self):
        return self.__envNames
