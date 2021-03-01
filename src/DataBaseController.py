import os, h5py
import numpy as np

class DataBaseController():
    def __init__(self, identifier):
        self.__id = identifier
        self.__baseDir = os.path.join(os.getenv('H5PY_DATABASE_DIR'), str(self.__id))



    def writeEntry(self, entryName, data):
        hf = h5py.File(entryName+".h5", 'w')
        for key, value in data.items():
            hf.create_dataset(key, data=value)
        hf.close()
    # def editEntry(self):

    def readEntry(self, entryName):
        data = {}
        hf = h5py.File(entryName+".h5", 'r')
        for key in hf.keys():
            val = hf.get(key)
            data[key] = val
        hf.close()
        return data

    # def deleteEntry(self):



resDummy = {"TOTALENERGY"      : 123,
            "DENSITYMATRIX"    : np.zeros((50,50)),
            "COEFFICIENTMATRIX": 789
        }

dbController = DataBaseController(2)
dbController.writeEntry("resDummy", resDummy)
print(dbController.readEntry("resDummy"))