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
        for outer, inner in self.__jsonSettings.items():
            if (outer.upper() == "NAME"): 
                self.__sereniypySettings.name = self.__jsonSettings[outer]
            if (outer.upper() == "CHARGE"): 
                self.__sereniypySettings.charge = self.__jsonSettings[outer]
            if (outer.upper() == "SPIN"): 
                self.__sereniypySettings.spin = self.__jsonSettings[outer]
            if (outer.upper() == "GEOMETRY"): 
                self.__sereniypySettings.geometry = self.__jsonSettings[outer]
            if (outer.upper() == "SCFMODE"): 
                self.__sereniypySettings.scfMode = jr.resolveSCFMode(self.__jsonSettings[outer].upper())
            if (outer.upper() == "METHOD"): 
                self.__sereniypySettings.method = jr.resolveElectronicStructureTheory(self.__jsonSettings[outer].upper())
        #o--------------o
        #| DFT Settings |
        #o--------------o
            if (outer.upper() == "DFT"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "FUNCTIONAL"):
                        self.__sereniypySettings.dft.functional = jr.resolveFunctional(self.__jsonSettings[outer][innerinner].upper())
                    if (innerinner.upper() == "DENSITYFITTING"):
                        self.__sereniypySettings.dft.densityFitting = jr.resolveDensityFitting(self.__jsonSettings[outer][innerinner].upper())
                    if (innerinner.upper() == "DISPERSION"):
                        self.__sereniypySettings.dft.dispersion = jr.resolveDispersionCorrection(self.__jsonSettings[outer][innerinner].upper())
        #o--------------o
        #| SCF Settings |
        #o--------------o
            if (outer.upper() == "SCF"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "INITIALGUESS"):
                        self.__sereniypySettings.scf.initialguess = jr.resolveInitialGuess(self.__jsonSettings[outer][innerinner].upper())
                    if (innerinner.upper() == "MAXCYCLES"):
                        self.__sereniypySettings.scf.maxCycles = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "WRITERESTART"):
                        self.__sereniypySettings.scf.writeRestart = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "ENERGYTHRESHOLD"):
                        self.__sereniypySettings.scf.energyThreshold = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "RMSDTHRESHOLD"):
                        self.__sereniypySettings.scf.rmsdThreshold = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "DAMPING"):
                        self.__sereniypySettings.scf.damping = jr.resolveDamping(self.__jsonSettings[outer][innerinner].upper())
                    if (innerinner.upper() == "SERIESDAMPINGSTART"):
                        self.__sereniypySettings.scf.seriesDampingStart = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "SERIESDAMPINGEND"):
                        self.__sereniypySettings.scf.seriesDampingEnd = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "SERIESDAMPINGSTEP"):
                        self.__sereniypySettings.scf.seriesDampingStep = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "SERIESDAMPINGINITIALSTEPS"):
                        self.__sereniypySettings.scf.seriesDampingInitialSteps = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "STATICDAMPINGFACTOR"):
                        self.__sereniypySettings.scf.staticDampingFactor = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "ENDDAMPERR"):
                        self.__sereniypySettings.scf.endDampErr = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "USELEVELSHIFT"):
                        self.__sereniypySettings.scf.useLevelshift = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "USEOFFDIAGLEVELSHIFT"):
                        self.__sereniypySettings.scf.useOffDiagLevelshift = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "MINIMUMLEVELSHIFT"):
                        self.__sereniypySettings.scf.minimumLevelshift = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "DIISFLUSH"):
                        self.__sereniypySettings.scf.diisFlush = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "DISSSTARTERROR"):
                        self.__sereniypySettings.scf.diisStartError = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "DISSMAXSTORE"):
                        self.__sereniypySettings.scf.diisMaxStore = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "DIISTHRESHOLD"):
                        self.__sereniypySettings.scf.diisThreshold = self.__jsonSettings[outer][innerinner]
                    if (innerinner.upper() == "USEADIIS"):
                        self.__sereniypySettings.scf.useADIIS = self.__jsonSettings[outer.upper() == "SCF"][innerinner]
        #o----------------o
        #| BASIS Settings |
        #o----------------o
        if (outer.upper() == "BASIS"):
            for innerinner, _ in inner.items():
                if (innerinner.upper() == "LABEL"):
                    self.__sereniypySettings.basis.label = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "AUXCLABEL"):
                    self.__sereniypySettings.basis.auxCLabel = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "AUXJLABEL"):
                    self.__sereniypySettings.basis.auxJLabel = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "MAKESPHERICALBASIS"):
                    self.__sereniypySettings.basis.makeSphericalBasis = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "INTEGRALTHRESHOLD"):
                    self.__sereniypySettings.basis.integralThreshold = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "BASISLIBPATH"):
                    self.__sereniypySettings.basis.basisLibPath = self.__jsonSettings[outer][innerinner]
        #o---------------o
        #| GRID Settings |
        #o---------------o
        if (outer.upper() == "GRID"):
            for innerinner, _ in inner.items():
                if (innerinner.upper() == "GRIDTYPE"):
                    self.__sereniypySettings.grid.gridType = jr.resolveGridType(self.__jsonSettings[outer][innerinner].upper())
                if (innerinner.upper() == "RADIALGRIDTYPE"):
                    self.__sereniypySettings.grid.radialGridType = jr.resolveRadialGridType(self.__jsonSettings[outer][innerinner].upper())
                if (innerinner.upper() == "SPHERICALGRIDTYPE"):
                    self.__sereniypySettings.grid.sphericalGridType = jr.resolveSphericalGridType(self.__jsonSettings[outer][innerinner].upper())
                if (innerinner.upper() == "BLOCKSIZE"):
                    self.__sereniypySettings.grid.blocksize = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "ACCURACY"):
                    self.__sereniypySettings.grid.accuracy = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "SMALLGRIDACCURACY"):
                    self.__sereniypySettings.grid.smallGridAccuracy = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "BLOCKAVETHRESHOLD"):
                    self.__sereniypySettings.grid.blockAveThreshold = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "BASFUNCRADIALTHRESHOLD"):
                    self.__sereniypySettings.grid.basFuncRadialThreshold = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "WEIGHTTHRESHOLD"):
                    self.__sereniypySettings.grid.weightThreshold = self.__jsonSettings[outer][innerinner]
                if (innerinner.upper() == "SMOOTHING"):
                    self.__sereniypySettings.grid.smoothing = self.__jsonSettings[outer][innerinner]
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