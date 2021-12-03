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

    def jsonValid(self):
        checker = jc.JobFormatChecker(self.__args)
        return checker.run()

    def enroll(self, jobstate_list, job_id):
        jobstate_list[job_id] = "RUN"
        self.__id = list(jr.find("ID", self.__args))[0]
        try:
            self.__baseDir = os.path.join(
                os.getenv('DATABASE_DIR'), str(self.__id))
            if (not os.path.exists(self.__baseDir)):
                os.mkdir(self.__baseDir)
        except KeyError as identifier:
            pass
        actSettingsDict = list(jr.find("ACT", self.__args))[0]
        try:
            envSettingsDict = list(jr.find("ENV", self.__args))[0]
        except:
            envSettingsDict = {}
        self.__taskName = list(jr.find("TASK", self.__args))[0]
        self.__actNames = list(jr.find("NAME", actSettingsDict))
        self.__actPaths = [os.path.join(self.__baseDir + name)
                           for name in self.__actNames]
        self.__envNames = list(jr.find("NAME", envSettingsDict))
        self.__envPaths = [os.path.join(self.__baseDir + name)
                           for name in self.__envNames]
        geometries = list(jr.find("GEOMETRY", self.__args))
        actGeometries = list(jr.find("GEOMETRY", actSettingsDict))
        envGeometries = list(jr.find("GEOMETRY", envSettingsDict))
        xyzfiles = list(jr.find("XYZ", self.__args))
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
            converter = sc.SettingsConverter(jr.dict2json(
                list(jr.find(actSystemKeys[i], actSettingsDict))[0]))
            self.__actSettings.append(converter.getSerenipySettings())

        if (envSettingsDict):
            envSystemKeys = list(envSettingsDict.keys())
            for i in range(len(envSystemKeys)):
                envSettingsDict[envSystemKeys[i]]["GEOMETRY"] = os.path.join(
                    self.__baseDir, envGeometries[i])
                envSettingsDict[envSystemKeys[i]]["PATH"] = os.path.join(
                    self.__baseDir) + "/"
                converter = sc.SettingsConverter(jr.dict2json(
                    list(jr.find(envSystemKeys[i], envSettingsDict))[0]))
                self.__envSettings.append(converter.getSerenipySettings())
        for act in self.__actSettings:
            self.__act.append(spy.System(act))
        for env in self.__envSettings:
            self.__env.append(spy.System(env))

    def perform(self, jobstate_list, job_id):
        parent = os.getcwd()
        os.chdir(self.__baseDir)
        spy.takeTime("the entire run")
        for setting in self.__actSettings:
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