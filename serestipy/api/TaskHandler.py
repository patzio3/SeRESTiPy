import os
import shutil as su
import time

import serestipy.api.SettingsConverter as sc
import serestipy.api.JsonResolver as jr
import serestipy.client.JsonHelper as jh
import serestipy.api.JobFormatChecker as jc
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

    def jsonValid(self):
        checker = jc.JobFormatChecker(self.__args)
        return checker.run()

    def enroll(self, jobstate_list, job_id):
        jobstate_list[job_id] = "RUN"
        self.__id = list(jh.find("ID", self.__args))[0]
        try:
            self.__baseDir = os.path.join(
                os.getenv('DATABASE_DIR'), str(self.__id))
            if (not os.path.exists(self.__baseDir)):
                os.mkdir(self.__baseDir)
        except KeyError as identifier:
            pass
        actSettingsDict = list(jh.find("ACT", self.__args))[0]
        try:
            envSettingsDict = list(jh.find("ENV", self.__args))[0]
        except:
            envSettingsDict = {}
        try:
            taskSettingsDict = list(jh.find("TASK_SETTINGS", self.__args))[0]
        except:
            taskSettingsDict = {}
        self.__taskName = list(jh.find("TASK", self.__args))[0]
        self.__actNames = list(jh.find("NAME", actSettingsDict))
        self.__actPaths = [os.path.join(self.__baseDir + name)
                           for name in self.__actNames]
        self.__envNames = list(jh.find("NAME", envSettingsDict))
        self.__envPaths = [os.path.join(self.__baseDir + name)
                           for name in self.__envNames]
        geometries = list(jh.find("GEOMETRY", self.__args))
        actGeometries = list(jh.find("GEOMETRY", actSettingsDict))
        envGeometries = list(jh.find("GEOMETRY", envSettingsDict))
        xyzfiles = list(jh.find("XYZ", self.__args))
        for i in range(len(xyzfiles)):
            with open(os.path.join(self.__baseDir, geometries[i]), "w") as inp:
                inp.write(xyzfiles[i])
            inp.close()
        actSystemKeys = list(actSettingsDict.keys())
        for i in range(len(actSystemKeys)):
            actSettingsDict[actSystemKeys[i]]["GEOMETRY"] = os.path.join(
                self.__baseDir, actGeometries[i])
            actSettingsDict[actSystemKeys[i]]["PATH"] = os.path.join(
                self.__baseDir) + "/"
            converter = sc.SettingsConverter(jh.dict2json(
                list(jh.find(actSystemKeys[i], actSettingsDict))[0]))
            self.__actSettings.append(converter.getSerenipySettings())

        if (envSettingsDict):
            envSystemKeys = list(envSettingsDict.keys())
            for i in range(len(envSystemKeys)):
                envSettingsDict[envSystemKeys[i]]["GEOMETRY"] = os.path.join(
                    self.__baseDir, envGeometries[i])
                envSettingsDict[envSystemKeys[i]]["PATH"] = os.path.join(
                    self.__baseDir) + "/"
                converter = sc.SettingsConverter(jh.dict2json(
                    list(jh.find(envSystemKeys[i], envSettingsDict))[0]))
                self.__envSettings.append(converter.getSerenipySettings())

        for act in self.__actSettings:
            self.__act.append(spy.System(act))
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

        for setting in self.__actSettings:
            if (jr.resolveSCFMode(setting.scfMode).upper() == "UNRESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                mode = jr.resolveSCFMode(setting.scfMode).upper()
        self.__serenityTaskObject = jr.resolveTask(mode, self.__taskName, self.__act, self.__env, taskSettingsDict)


        self.__serenityTaskSettings = self.__serenityTaskObject.settings

    def perform(self, jobstate_list, job_id):        
        parent = os.getcwd()
        os.chdir(self.__baseDir)
        start = time.time()
        self.__serenityTaskObject.run()
        end = time.time()
        spy.printTimes()
        print("Time taken for ENTIRE run", end - start, "s")
        os.chdir(parent)
        jobstate_list[job_id] = "IDLE"

    def cleanUp(self):
        if (os.path.exists(self.__baseDir)):
            su.rmtree(self.__baseDir)

    def getSettings(self):
        return self.__serenityTaskSettings