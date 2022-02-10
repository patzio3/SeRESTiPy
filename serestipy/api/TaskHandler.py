#!/usr/bin/env  python3
#@file   TaskHandler.py
#
#@date   Feb 9, 2022
#@author Patrick Eschenbach
#@copyright \n
# This file is part of the program SeRESTiPy.\n\n
# SeRESTiPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.\n\n
# SeRESTiPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.\n\n
# You should have received a copy of the GNU Lesser General
# Public License along with SeRESTiPy.
# If not, see <http://www.gnu.org/licenses/>.\n

import os
import shutil as su
import time

import serestipy.api.SettingsConverter as sc
import serestipy.api.JsonResolver as jr
import serestipy.client.JsonHelper as jh

import serenipy as spy

## @class TaskHandler
#   This class accepts a JSON input file and prepares
#   serenipy objects to run a serenity calculation.
#   @param args: Provided JSON input
class TaskHandler():
    def __init__(self, args):
        self.__args = args
        self.__id = ""
        self.__taskName = ""
        self.__act = []
        self.__env = []
        self.__actSettings = []
        self.__envSettings = []

    ## @brief Prepares the Serenity Settings and Task for the run.
    #   @param job_id: The job_id URI that is provided by the API.
    #   @param jobstate_list: A list of the jobstate which is shared
    #                         between multiple processes.
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
                self.__scfmode = jr.resolveSCFMode(setting.scfMode).upper()
            elif (jr.resolveSCFMode(setting.scfMode).upper() == "RESTRICTED"):
                self.__scfmode = jr.resolveSCFMode(setting.scfMode).upper()
        self.__serenityTaskObject = jr.resolveTask(self.__scfmode, self.__taskName, self.__act, self.__env, taskSettingsDict)

    ## @brief Performs the Serenity Calculation and stores the results.
    #   @param job_id: The job_id URI that is provided by the API.
    #   @param jobstate_list: A list of the jobstate which is shared
    #                         between multiple processes.
    #   @param results_list: A list of the calculation results which is shared
    #                         between multiple processes.
    def perform(self, jobstate_list, job_id, results_list):  
        def getDensMatrix(system):
            if (self.__scfmode == "UNRESTRICTED"):
                return [jh.array2json(system.getElectronicStructure_U().alphaDens()), jh.array2json(system.getElectronicStructure_U().betaDens())]
            else:
                return [jh.array2json(system.getElectronicStructure_R().totalDens())]
        def getCoeffs(system):
            if (self.__scfmode == "UNRESTRICTED"):
                return [jh.array2json(system.getElectronicStructure_U().alphaCoeff()), jh.array2json(system.getElectronicStructure_U().betaCoeff())]
            else:
                return [jh.array2json(system.getElectronicStructure_R().coeff())]
        def getEnergy(system):
            return system.getEnergy()
        parent = os.getcwd()
        os.chdir(self.__baseDir)
        start = time.time()
        self.__serenityTaskObject.run()
        end = time.time()
        results_list[job_id] = { "DMAT" : { str(key):getDensMatrix(system) for key,system in enumerate(self.__act) },
                                 "COEF" : { str(key):getCoeffs(system) for key,system in enumerate(self.__act) },
                                 "ENERGY" : { str(key):getEnergy(system) for key,system in enumerate(self.__act) }
                                }
        spy.printTimes()
        print("Time taken for ENTIRE run", end - start, "s")
        os.chdir(parent)
        jobstate_list[job_id] = "IDLE"

    ## @brief Cleans up the file-system tree.
    def cleanUp(self):
        if (os.path.exists(self.__baseDir)):
            su.rmtree(self.__baseDir)

    ## @brief Converts the results into JSON format and passes them to the Api.
    #         Therefore, a user can receive those results
    #   @param job_id: The job_id URI that is provided by the API.
    #   @param type: The type of results needed
    #   @param results_list: A list of the calculation results which is shared
    #                         between multiple processes.
    #   @return JSON object containing density and coefficient matrix as well as
    #           the total energy
    def getResults(self,job_id,results_list,type):
        switcher = {
        "DENSITYMATRIX" : results_list[job_id]["DMAT"],
        "COEFFICIENTMATRIX" : results_list[job_id]["COEF"],
        "COEFFICIENTS" : results_list[job_id]["COEF"],
        "ENERGY": results_list[job_id]["ENERGY"]
        }
        return switcher.get(type.upper(), "Invalid Result type!")