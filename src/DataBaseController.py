import os, h5py
import numpy as np
import shutil as su

class DataBaseController():
    def __init__(self, identifier):
        self.__id = identifier
        self.__baseDir = os.path.join(os.getenv('H5PY_DATABASE_DIR'), str(self.__id))
        if (not os.path.exists(self.__baseDir)):
            try:
                os.mkdir(self.__baseDir)
            except OSError:
                print ("Creation of the directory %s failed" % self.__baseDir)

    def eradicate(self):
        su.rmtree(os.path.join(self.__baseDir))

    def writeEntry(self, entryName, data):
        hf = h5py.File(os.path.join(self.__baseDir,entryName+".h5"), 'w')
        for key, value in data.items():
            hf.create_dataset(key, data=value)
        hf.close()

    # def editEntry(self):

    def readEntry(self, entryName):
        data = {}
        hf = h5py.File(os.path.join(self.__baseDir,entryName+".h5"), 'r')
        for key in hf.keys():
            val = np.array(hf.get(key))
            data[key] = val
        hf.close()
        return data

    # def deleteEntry(self):