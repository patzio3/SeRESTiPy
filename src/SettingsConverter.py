import json, sys
import JsonResolver as jr
from serenipy import Settings

class SettingsConverter():
    #+-------------+
    #| Constructor |
    #+-------------+
    def __init__(self, jsonSettings):
        self.__jsonSettings = jsonSettings
        #o----------o
        #| Settings |
        #o----------o
        self.__sereniypySettings = Settings()
        if ("system" not in jsonSettings):
            print("Error 404: No system specified!!!")
            sys.exit()
        else:
            if ("name" in jsonSettings["system"]): 
                self.__sereniypySettings.name = jsonSettings["system"]["name"]
            if ("path" in jsonSettings["system"]): 
                self.__sereniypySettings.path = jsonSettings["system"]["path"]
            if ("charge" in jsonSettings["system"]): 
                self.__sereniypySettings.charge = jsonSettings["system"]["charge"]
            if ("spin" in jsonSettings["system"]): 
                self.__sereniypySettings.spin = jsonSettings["system"]["spin"]
            if ("geometry" in jsonSettings["system"]): 
                self.__sereniypySettings.geometry = jsonSettings["system"]["geometry"]
            if ("scfMode" in jsonSettings["system"]): 
                self.__sereniypySettings.scfMode = jr.resolveSCFMode(jsonSettings["system"]["scfMode"].upper())
            if ("method" in jsonSettings["system"]): 
                self.__sereniypySettings.method = jr.resolveElectronicStructureTheory(jsonSettings["system"]["method"].upper())
        #o--------------o
        #| DFT Settings |
        #o--------------o
        if ("dft" in jsonSettings):
            if ("functional" in jsonSettings["dft"]):
                self.__sereniypySettings.dft.functional = jr.resolveFunctional(jsonSettings["dft"]["functional"].upper())
            if ("densityFitting" in jsonSettings["dft"]):
                self.__sereniypySettings.dft.densityFitting = jr.resolveDensityFitting(jsonSettings["dft"]["densityFitting"].upper())
            if ("dispersion" in jsonSettings["dft"]):
                self.__sereniypySettings.dft.dispersion = jr.resolveDispersionCorrection(jsonSettings["dft"]["dispersion"].upper())
        #o--------------o
        #| SCF Settings |
        #o--------------o
        if ("scf" in jsonSettings):
            if ("initialguess" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.initialguess = jr.resolveInitialGuess(jsonSettings["scf"]["initialguess"].upper())
            if ("maxCycles" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.maxCycles = jsonSettings["scf"]["maxCycles"]
            if ("writeRestart" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.writeRestart = jsonSettings["scf"]["writeRestart"]
            if ("energyThreshold" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.energyThreshold = jsonSettings["scf"]["energyThreshold"]
            if ("rmsdThreshold" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.rmsdThreshold = jsonSettings["scf"]["rmsdThreshold"]
            if ("damping" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.damping = jr.resolveDamping(jsonSettings["scf"]["damping"].upper())
            if ("seriesDampingStart" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingStart = jsonSettings["scf"]["seriesDampingStart"]
            if ("seriesDampingEnd" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingEnd = jsonSettings["scf"]["seriesDampingEnd"]
            if ("seriesDampingStep" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingStep = jsonSettings["scf"]["seriesDampingStep"]
            if ("seriesDampingInitialSteps" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingInitialSteps = jsonSettings["scf"]["seriesDampingInitialSteps"]
            if ("staticDampingFactor" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.staticDampingFactor = jsonSettings["scf"]["staticDampingFactor"]
            if ("endDampErr" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.endDampErr = jsonSettings["scf"]["endDampErr"]
            if ("useLevelshift" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.useLevelshift = jsonSettings["scf"]["useLevelshift"]
            if ("useOffDiagLevelshift" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.useOffDiagLevelshift = jsonSettings["scf"]["useOffDiagLevelshift"]
            if ("minimumLevelshift" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.minimumLevelshift = jsonSettings["scf"]["minimumLevelshift"]
            if ("diisFlush" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisFlush = jsonSettings["scf"]["diisFlush"]
            if ("diisStartError" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisStartError = jsonSettings["scf"]["diisStartError"]
            if ("diisMaxStore" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisMaxStore = jsonSettings["scf"]["diisMaxStore"]
            if ("diisThreshold" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisThreshold = jsonSettings["scf"]["diisThreshold"]
            if ("useADIIS" in jsonSettings["scf"]):
                self.__sereniypySettings.scf.useADIIS = jsonSettings["scf"]["useADIIS"]
        #o----------------o
        #| BASIS Settings |
        #o----------------o
        if ("basis" in jsonSettings):
            if ("label" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.label = jsonSettings["basis"]["label"]
            if ("auxCLabel" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.auxCLabel = jsonSettings["basis"]["auxCLabel"]
            if ("auxJLabel" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.auxJLabel = jsonSettings["basis"]["auxJLabel"]
            if ("makeSphericalBasis" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.makeSphericalBasis = jsonSettings["basis"]["makeSphericalBasis"]
            if ("integralThreshold" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.integralThreshold = jsonSettings["basis"]["integralThreshold"]
            if ("basisLibPath" in jsonSettings["basis"]):
                self.__sereniypySettings.basis.basisLibPath = jsonSettings["basis"]["basisLibPath"]
        #o---------------o
        #| GRID Settings |
        #o---------------o
        if ("grid" in jsonSettings):
            if ("gridType" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.gridType = jr.resolveGridType(jsonSettings["grid"]["gridType"].upper())
            if ("radialGridType" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.radialGridType = jr.resolveRadialGridType(jsonSettings["grid"]["radialGridType"].upper())
            if ("sphericalGridType" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.sphericalGridType = jr.resolveSphericalGridType(jsonSettings["grid"]["sphericalGridType"].upper())
            if ("blocksize" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.blocksize = jsonSettings["grid"]["blocksize"]
            if ("accuracy" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.accuracy = jsonSettings["grid"]["accuracy"]
            if ("smallGridAccuracy" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.smallGridAccuracy = jsonSettings["grid"]["smallGridAccuracy"]
            if ("blockAveThreshold" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.blockAveThreshold = jsonSettings["grid"]["blockAveThreshold"]
            if ("basFuncRadialThreshold" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.basFuncRadialThreshold = jsonSettings["grid"]["basFuncRadialThreshold"]
            if ("weightThreshold" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.weightThreshold = jsonSettings["grid"]["weightThreshold"]
            if ("smoothing" in jsonSettings["grid"]):
                self.__sereniypySettings.grid.smoothing = jsonSettings["grid"]["smoothing"]
    #+------------------+
    #| Member functions |
    #+------------------+
    def getJsonSettings(self):
        return self.__jsonSettings

    def getSerenipySettings(self):
        return self.__sereniypySettings

    def setJsonSettings(self, json):
        self.__jsonSettings = json

    def setSerenipySettings(self, serSettings):
        self.__sereniypySettings = serSettings