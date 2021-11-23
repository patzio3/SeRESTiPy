def upperRecursive(oldDict):
    for k,v in oldDict.items():
        oldDict[k.upper()] = oldDict.pop(k)
        if isinstance(v, dict):    
            upperRecursive(v)
    return oldDict

class JobFormatChecker():
    def __init__(self, json):
        self.__json = upperRecursive(json)
        self.__allowedOuterKeys = ["JOBSTATE",
                                   "STATE",
                                   "TASK",
                                   "ID",
                                   "ACTIVESYSTEMSETTINGS",
                                   "ACTSETTINGS",
                                   "ENVIRONMENTSYSTEMSETTINGS",
                                   "ENVSETTINGS",
                                   "ACT",
                                   "ENV"
                                   ]
        # self.__jobstates = ["INITIAL",
        #                     "INIT",
        #                     "INI",
        #                     "RUNNING",
        #                     "RUN",
        #                     "FINISH",
        #                     "FINISHED",
        #                     "FIN"
        #                     ]
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
                                   "LOAD"
                                   ]
        # self.__allowedResultsKeys = ["DENSITYMATRIX",
        #                              "COEFFICIENTMATRIX",
        #                              "COEFFICIENTS",
        #                              "DENSITYMATRIXALPHA",
        #                              "DENSITYMATRIXBETA",
        #                              "COEFFICIENTMATRIXALPHA",
        #                              "COEFFICIENTMATRIXBETA",
        #                              "TOTALENERGY"
        #                              ]

    def run(self):
        actSettingsDict = ""
        envSettingsDict = ""
        # jobstate = ""
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
                __ = self.__json["FILEID"]
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
            for sysSettings, innerSys in settings.items():
                # if (sysSettings.upper() == "RESULTS" and (jobstate.upper() in ["INI", "INIT", "INITIAL"])):
                #     print(
                #         f"KeyError: Field '{sysSettings.upper()}' not allowed for 'INITIAL' jobstate!")
                #     return False
                # elif (sysSettings.upper() == "RESULTS"):
                #     for resKey, _ in innerSys.items():
                #         if (resKey.upper() not in self.__allowedResultsKeys):
                #             print(
                #                 f"KeyError: Field '{resKey.upper()}' not allowed for 'RESULTS' scope!")
                #             return False
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
                for sysSettings, innerSys in settings.items():
                    # if (sysSettings.upper() == "RESULTS" and (jobstate.upper() in ["INI", "INIT", "INITIAL"])):
                    #     print(
                    #         f"KeyError: Field '{sysSettings.upper()}' not allowed for 'INITIAL' jobstate!")
                    #     return False
                    # elif (sysSettings.upper() == "RESULTS"):
                    #     for resKey, _ in innerSys.items():
                    #         if (resKey.upper() not in self.__allowedResultsKeys):
                    #             print(
                    #                 f"KeyError: Field '{resKey.upper()}' not allowed for 'RESULTS' scope!")
                    #             return False
                    if (sysSettings.upper() not in self.__allowedInnerKeys):
                        print(
                            f"KeyError: Field '{sysSettings.upper()}' not allowed in settings scope! Check manual!")
                        return False
        return True