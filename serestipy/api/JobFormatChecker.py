#!/usr/bin/env  python3
#@file   JobFormatChecker.py
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


## @class JobFormatChecker
#   This class accepts a JSON input file and checks
#   whether the Keys and Values have the correct format.
#   Additionally it checks whether needed values are missing.
class JobFormatChecker():
    def __init__(self, json):
        self.__json = json
        self.__allowedOuterKeys = ["TASK",
                                   "ID",
                                   "ACTIVESYSTEMSETTINGS",
                                   "ACTSETTINGS",
                                   "ENVIRONMENTSYSTEMSETTINGS",
                                   "ENVSETTINGS",
                                   "ACT",
                                   "ENV",
                                   "TASK_SETTINGS"
                                   ]
        self.__allowedSystemKeys = ["SYSTEM",
                                    "SYS"
                                    ]
        self.__allowedInnerKeys = ["NAME",
                                   "GEOMETRY",
                                   "XYZ",
                                   "METHOD",
                                   "SCFMODE",
                                   "CHARGE",
                                   "SPIN",
                                   "DFT",
                                   "BASIS",
                                   "SCF",
                                   "GRID",
                                   "EFIELD",
                                   "LOAD",
                                   "PATH"
                                   ]

    ## @brief Makes all strings in JSON uppercase.
    #         It uses recursion
    #   @param oldDict: The old dictionary
    #   @param newDict: The new dictionary with 
    #                   upper case key:value pairs
    def __upperCase(self, oldDict, newDict):
        for k, v in oldDict.items():
            if (isinstance(v,dict)):
                newDict[k] = {}
                self.__upperCase(v, newDict[k])
            else:
                newDict[k.upper()] = v.upper() if isinstance(v, str) else v

    ## @brief Checks doubly occuring keys
    #   @param oldDict: The old dictionary
    #   @param newDict: The new dictionary with 
    #                   upper case key:value pairs
    def __checkDoubles(self, oldDict):
        for _, v in oldDict.items():
            if (isinstance(v,dict)):
                self.__checkDoubles(v)
            else:
                seen = set()
                dupes = [x.upper() for x in oldDict.keys() if x.upper() in seen or seen.add(x.upper())]
                if (len(dupes) > 0):
                    return True

    ## @brief Runs the check.
    def run(self):
        # print(self.__json)
        if (self.__checkDoubles(self.__json)):
            print(f"KeyError: Double Keys found!")
            return False

        newDict = dict()
        self.__upperCase(self.__json, newDict)
        self.__json = newDict.copy()
        actSettingsDict = ""
        envSettingsDict = ""
        # check if only allowed outer keys are present
        for outer, _ in self.__json.items():
            if (outer not in self.__allowedOuterKeys):
                print(
                    f"KeyError: Field '{outer}' not allowed in outermost scope!")
                return False

        # look for tasks key
        try:
            _ = self.__json["TASK"]
        except KeyError as error:
            print(f"KeyError: {error} key not present, but required in JSON")
            return False

        try:
            _ = self.__json["ID"]
        except KeyError as errorOne:
            try:
                _ = self.__json["FILEID"]
            except KeyError as errorTwo:
                print(f"KeyError: FILEID or ID key not present, but required in JSON")
                return False
        # look for active system settings
        try:
            actSettingsDict = self.__json["ACTSETTINGS"]
        except KeyError as errorOne:
            try:
                actSettingsDict = self.__json["ACTIVESYSTEMSETTINGS"]
            except KeyError as errorTwo:
                try:
                    actSettingsDict = self.__json["ACT"]
                except KeyError as errorThree:
                    print(
                        f"KeyError: '{errorOne}', '{errorTwo}' or '{errorThree}' key not present, but required in JSON")
                    return False

        # look for environment system settings, do not throw error because not always required
        try:
            envSettingsDict = self.__json["ENVSETTINGS"]
        except KeyError as errorOne:
            try:
                envSettingsDict = self.__json["ENVIRONMENTSYSTEMSETTINGS"]
            except KeyError as errorTwo:
                try:
                    envSettingsDict = self.__json["ENV"]
                except KeyError as errorThree:
                    pass
        # check settings of active systems
        for system, settings in actSettingsDict.items():
            if (system[0:6].upper() not in self.__allowedSystemKeys and system[0:3].upper() not in self.__allowedSystemKeys):
                print(
                    f"KeyError: Field '{system.upper()}' not allowed in activesystem scope! Must be 'SYSTEM<xyz>' or 'SYS<xyz>'!")
                return False
            for sysSettings, _ in settings.items():
                if (sysSettings.upper() not in self.__allowedInnerKeys):
                    print(
                        f"KeyError: Field '{sysSettings.upper()}' not allowed in settings scope! Check manual!")
                    return False
        # check settings of environment systems
        if (envSettingsDict != ""):
            for system, settings in envSettingsDict.items():
                if (system[0:6].upper() not in self.__allowedSystemKeys and system[0:3].upper() not in self.__allowedSystemKeys):
                    print(
                        f"KeyError: Field '{system.upper()}' not allowed in activesystem scope! Must be 'SYSTEM<xyz>' or 'SYS<xyz>'!")
                    return False
                for sysSettings, _ in settings.items():
                    if (sysSettings.upper() not in self.__allowedInnerKeys):
                        print(
                            f"KeyError: Field '{sysSettings.upper()}' not allowed in settings scope! Check manual!")
                        return False
        return True
