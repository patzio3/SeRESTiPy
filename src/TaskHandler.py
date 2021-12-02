import os
import shutil as su

import SettingsConverter as sc
import JsonResolver as jr
import JobFormatChecker as jc
import serenipy as spy


class TaskHandler():
    def __init__(self, args):
        self.__args = args
        self.__id = ""
        self.__taskName = ""
        self.__act = []
        self.__env = []
        self.__actNames = []
        self.__envNames = []
        self.__actSettings = []
        self.__envSettings = []
        self.__actPaths = []
        self.__envPaths = []

    def __find(self,key,value):
        for k, v in (value.items() if isinstance(value, dict) else
                   enumerate(value) if isinstance(value, list) else []):
            if k == key:
              yield v
            elif isinstance(v, (dict, list)):
              for result in self.__find(key, v):
                yield result

    def jsonValid(self):
        checker = jc.JobFormatChecker(self.__args)
        return checker.run()

    def enroll(self, jobstate_list, job_id):
        jobstate_list[job_id] = "RUN"
        self.__id = list(self.__find("ID",self.__args))[0]
        try:
            self.__baseDir = os.path.join(os.getenv('DATABASE_DIR'), str(self.__id))
            if (not os.path.exists(self.__baseDir)):
                os.mkdir(self.__baseDir)
        except KeyError as identifier:
            pass
        actSettingsDict = list(self.__find("ACT",self.__args))[0]
        try:
            envSettingsDict = list(self.__find("ENV",self.__args))[0]
        except:
            envSettingsDict = {}
        self.__taskName = list(self.__find("TASK",self.__args))[0]
        self.__actNames = list(self.__find("NAME",actSettingsDict))
        self.__actPaths = [os.path.join(self.__baseDir + name) for name in self.__actNames]
        self.__envNames = list(self.__find("NAME",envSettingsDict))
        self.__envPaths = [os.path.join(self.__baseDir + name) for name in self.__envNames]
        geometries = list(self.__find("GEOMETRY",self.__args))
        actGeometries = list(self.__find("GEOMETRY",actSettingsDict))
        envGeometries = list(self.__find("GEOMETRY",envSettingsDict))
        xyzfiles = list(self.__find("XYZ",self.__args))
        for i in range(len(xyzfiles)):
            with open(os.path.join(self.__baseDir,geometries[i]), "w") as inp:
                inp.write(xyzfiles[i])
            inp.close()
        actSystemKeys = list(actSettingsDict.keys())
        for i in range(len(actSystemKeys)):
            actSettingsDict[actSystemKeys[i]]["GEOMETRY"] = os.path.join(self.__baseDir,actGeometries[i])
            actSettingsDict[actSystemKeys[i]]["PATH"] = os.path.join(self.__baseDir) + "/"
            converter = sc.SettingsConverter(jr.dict2json(list(self.__find(actSystemKeys[i],actSettingsDict))[0]))
            self.__actSettings.append(converter.getSerenipySettings())
        
        if (envSettingsDict):
            envSystemKeys = list(envSettingsDict.keys())
            for i in range(len(envSystemKeys)):
                envSettingsDict[envSystemKeys[i]]["GEOMETRY"] = os.path.join(self.__baseDir,envGeometries[i])
                envSettingsDict[envSystemKeys[i]]["PATH"] = os.path.join(self.__baseDir) + "/"
                converter = sc.SettingsConverter(jr.dict2json(list(self.__find(envSystemKeys[i],envSettingsDict))[0]))
                self.__envSettings.append(converter.getSerenipySettings())
        for act in self.__actSettings:
            self.__act.append(spy.System(act))
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self, jobstate_list, job_id):
        parent = os.getcwd()
        os.chdir(self.__baseDir)
        spy.takeTime("the entire run");
        for setting in self.__actSettings:
            print("IN LOOP", setting)
            if (jr.resolveSCFMode(setting.scfMode).upper() == "UNRESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
        task = jr.resolveTask(mode, self.__taskName, self.__act, self.__env)
        task.run()
        spy.printTimes()
        spy.timeTaken(0, "the entire run")
        os.chdir(parent)
        jobstate_list[job_id] = "IDLE"

    def cleanUp(self):
        if (os.path.exists(self.__baseDir)):
            su.rmtree(self.__baseDir)

    def getActNames(self):
        return self.__actNames

    def getEnvNames(self):
        return self.__envNames

        

        

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