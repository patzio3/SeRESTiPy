import TaskHandler as th
import JobFormatChecker as jc
import sys

class TaskUpdater():
    def __init__(self, task, args):
        self.__task = task
        self.__args = args
        checker = jc.JobFormatChecker(self.__args)
        checker.run()

    def run(self):
        #check if given job and task have the same system names
        self.__checkSystemConsistency()
        # - if systems and task is the same get stuff from disk and run job
        # - if systems are the same and task is different get stuff from disk,
        #   setup new dbController for writing the new results. Keep old dbController?
        # - We need to check for basis set consistency when loading from disk!!!!
        # - the roles of active and environment systems can change as far as the overall
        #   systems stay the same

    def __checkSystemConsistency(self):
        presentNames = self.__task.getActNames().copy()
        presentNames += self.__task.getEnvNames().copy()
        newNames = []
        for outer, _ in self.__args.items():
            if (outer.upper() in ["ACTIVESYSTEMSETTINGS", "ACTSETTINGS", "SYSTEMSETTINGS"]):
                actSettingsDict = self.__args[outer.upper()]
            elif (outer.upper() in ["ENVIRONMENTSYSTEMSETTINGS", "ENVSETTINGS"]):
                envSettingsDict = self.__args[outer.upper()]
        settingsDict = dict(actSettingsDict, **envSettingsDict)
        for outer, _ in settingsDict.items():
            if (outer[0:6].upper() in ["SYSTEM","SYS"] or \
                outer[0:3].upper() in ["SYSTEM","SYS"]):
                newNames.append(outer)
        if(set(presentNames) != set(newNames)):
            print("Task and sent request contain different systems. Please submit a new task with those systems!")
            sys.exit()