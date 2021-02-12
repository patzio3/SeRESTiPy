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
        if ("name" in self.__jsonSettings): 
            self.__sereniypySettings.name = self.__jsonSettings["name"]
        if ("path" in self.__jsonSettings): 
            self.__sereniypySettings.path = self.__jsonSettings["path"]
        if ("charge" in self.__jsonSettings): 
            self.__sereniypySettings.charge = self.__jsonSettings["charge"]
        if ("spin" in self.__jsonSettings): 
            self.__sereniypySettings.spin = self.__jsonSettings["spin"]
        if ("geometry" in self.__jsonSettings): 
            self.__sereniypySettings.geometry = self.__jsonSettings["geometry"]
        if ("scfMode" in self.__jsonSettings): 
            self.__sereniypySettings.scfMode = jr.resolveSCFMode(self.__jsonSettings["scfMode"].upper())
        if ("method" in self.__jsonSettings): 
            self.__sereniypySettings.method = jr.resolveElectronicStructureTheory(self.__jsonSettings["method"].upper())
        #o--------------o
        #| DFT Settings |
        #o--------------o
        if ("dft" in self.__jsonSettings):
            if ("functional" in self.__jsonSettings["dft"]):
                self.__sereniypySettings.dft.functional = jr.resolveFunctional(self.__jsonSettings["dft"]["functional"].upper())
            if ("densityFitting" in self.__jsonSettings["dft"]):
                self.__sereniypySettings.dft.densityFitting = jr.resolveDensityFitting(self.__jsonSettings["dft"]["densityFitting"].upper())
            if ("dispersion" in self.__jsonSettings["dft"]):
                self.__sereniypySettings.dft.dispersion = jr.resolveDispersionCorrection(self.__jsonSettings["dft"]["dispersion"].upper())
        #o--------------o
        #| SCF Settings |
        #o--------------o
        if ("scf" in self.__jsonSettings):
            if ("initialguess" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.initialguess = jr.resolveInitialGuess(self.__jsonSettings["scf"]["initialguess"].upper())
            if ("maxCycles" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.maxCycles = self.__jsonSettings["scf"]["maxCycles"]
            if ("writeRestart" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.writeRestart = self.__jsonSettings["scf"]["writeRestart"]
            if ("energyThreshold" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.energyThreshold = self.__jsonSettings["scf"]["energyThreshold"]
            if ("rmsdThreshold" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.rmsdThreshold = self.__jsonSettings["scf"]["rmsdThreshold"]
            if ("damping" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.damping = jr.resolveDamping(self.__jsonSettings["scf"]["damping"].upper())
            if ("seriesDampingStart" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingStart = self.__jsonSettings["scf"]["seriesDampingStart"]
            if ("seriesDampingEnd" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingEnd = self.__jsonSettings["scf"]["seriesDampingEnd"]
            if ("seriesDampingStep" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingStep = self.__jsonSettings["scf"]["seriesDampingStep"]
            if ("seriesDampingInitialSteps" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.seriesDampingInitialSteps = self.__jsonSettings["scf"]["seriesDampingInitialSteps"]
            if ("staticDampingFactor" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.staticDampingFactor = self.__jsonSettings["scf"]["staticDampingFactor"]
            if ("endDampErr" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.endDampErr = self.__jsonSettings["scf"]["endDampErr"]
            if ("useLevelshift" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.useLevelshift = self.__jsonSettings["scf"]["useLevelshift"]
            if ("useOffDiagLevelshift" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.useOffDiagLevelshift = self.__jsonSettings["scf"]["useOffDiagLevelshift"]
            if ("minimumLevelshift" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.minimumLevelshift = self.__jsonSettings["scf"]["minimumLevelshift"]
            if ("diisFlush" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisFlush = self.__jsonSettings["scf"]["diisFlush"]
            if ("diisStartError" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisStartError = self.__jsonSettings["scf"]["diisStartError"]
            if ("diisMaxStore" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisMaxStore = self.__jsonSettings["scf"]["diisMaxStore"]
            if ("diisThreshold" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.diisThreshold = self.__jsonSettings["scf"]["diisThreshold"]
            if ("useADIIS" in self.__jsonSettings["scf"]):
                self.__sereniypySettings.scf.useADIIS = self.__jsonSettings["scf"]["useADIIS"]
        #o----------------o
        #| BASIS Settings |
        #o----------------o
        if ("basis" in self.__jsonSettings):
            if ("label" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.label = self.__jsonSettings["basis"]["label"]
            if ("auxCLabel" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.auxCLabel = self.__jsonSettings["basis"]["auxCLabel"]
            if ("auxJLabel" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.auxJLabel = self.__jsonSettings["basis"]["auxJLabel"]
            if ("makeSphericalBasis" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.makeSphericalBasis = self.__jsonSettings["basis"]["makeSphericalBasis"]
            if ("integralThreshold" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.integralThreshold = self.__jsonSettings["basis"]["integralThreshold"]
            if ("basisLibPath" in self.__jsonSettings["basis"]):
                self.__sereniypySettings.basis.basisLibPath = self.__jsonSettings["basis"]["basisLibPath"]
        #o---------------o
        #| GRID Settings |
        #o---------------o
        if ("grid" in self.__jsonSettings):
            if ("gridType" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.gridType = jr.resolveGridType(self.__jsonSettings["grid"]["gridType"].upper())
            if ("radialGridType" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.radialGridType = jr.resolveRadialGridType(self.__jsonSettings["grid"]["radialGridType"].upper())
            if ("sphericalGridType" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.sphericalGridType = jr.resolveSphericalGridType(self.__jsonSettings["grid"]["sphericalGridType"].upper())
            if ("blocksize" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.blocksize = self.__jsonSettings["grid"]["blocksize"]
            if ("accuracy" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.accuracy = self.__jsonSettings["grid"]["accuracy"]
            if ("smallGridAccuracy" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.smallGridAccuracy = self.__jsonSettings["grid"]["smallGridAccuracy"]
            if ("blockAveThreshold" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.blockAveThreshold = self.__jsonSettings["grid"]["blockAveThreshold"]
            if ("basFuncRadialThreshold" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.basFuncRadialThreshold = self.__jsonSettings["grid"]["basFuncRadialThreshold"]
            if ("weightThreshold" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.weightThreshold = self.__jsonSettings["grid"]["weightThreshold"]
            if ("smoothing" in self.__jsonSettings["grid"]):
                self.__sereniypySettings.grid.smoothing = self.__jsonSettings["grid"]["smoothing"]
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