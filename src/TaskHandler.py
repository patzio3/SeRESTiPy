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
        self.__state = "IDLE"

    def getState(self):
        return self.__state

    def jsonValid(self):
        checker = jc.JobFormatChecker(self.__args)
        return checker.run()

    def getActiveSystems(self):
        return self.__act

    def getEnvironmentSystems(self):
        return self.__env

    def getTaskInfo(self):
        return self.__args

    def enroll(self, job_id):
        self.__state = "RUN"
        os.mkdir(os.path.join(os.getcwd(), str(job_id)))
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
        for outer, inner in actSettingsDict.items():
            # write the sent XYZ to file
            # ToDo: create the xyz file in the a scratch directory
            for innerinner, _ in inner.items():
                if (innerinner.upper() == "GEOMETRY"):
                    with open(os.path.join(os.getcwd(), str(job_id),inner[innerinner]), 'w') as file:
                        if ("XYZ" in inner):
                            file.write(inner["XYZ"])
                            file.close()
                    inner["GEOMETRY"] = os.path.join(os.getcwd(), str(job_id), inner[innerinner])
            inner["PATH"] = os.path.join(os.getcwd(), str(job_id))
            if (outer[0:6].upper() in ["SYSTEM", "SYS"] or outer[0:3].upper() in ["SYSTEM", "SYS"]):
                converter = sc.SettingsConverter(jr.dict2json(inner))
                self.__actSettings.append(converter.getSerenipySettings())
                self.__actNames.append(outer)
                self.__nAct += 1

        if (envSettingsDict != ""):
            for outer, inner in envSettingsDict.items():
                # write the sent XYZ to file
                # ToDo: create the xyz file in the a scratch directory
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "GEOMETRY"):
                        with open(os.path.join(os.getcwd(), str(job_id),inner[innerinner]), 'w') as file:
                            if ("XYZ" in inner):
                                file.write(inner["XYZ"])
                                file.close()
                        inner["GEOMETRY"] = os.path.join(os.getcwd(), str(job_id), inner[innerinner])
                inner["PATH"] = os.path.join(os.getcwd(), str(job_id))
                if (outer[0:6].upper() in ["SYSTEM"] or
                        outer[0:3].upper() in ["SYS"]):
                    converter = sc.SettingsConverter(jr.dict2json(inner))
                    self.__envSettings.append(converter.getSerenipySettings())
                    self.__envNames.append(outer)
                    self.__nEnv += 1
        # create systems from gathered settings
        for act in self.__actSettings:
            self.__act.append(spy.System(act))
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self, job_id):
        parent = os.getcwd()
        os.chdir(os.path.join(parent, str(job_id)))
        spy.takeTime("the entire run");
        for setting in self.__actSettings:
            if (jr.resolveSCFMode(setting.scfMode).upper() == "UNRESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
        task = jr.resolveTask(mode, self.__taskName, self.__act, self.__env)
        task.run()
        self.__state = "IDLE"
        spy.printTimes()
        spy.timeTaken(0, "the entire run")
        os.chdir(parent)
        
        

        

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
