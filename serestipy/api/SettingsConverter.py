#!/usr/bin/env  python3
#@file   SettingsConverter.py
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

import json
import serestipy.api.JsonResolver as jr
from serenipy import Settings

## @class SettingsConverter
#   This class accepts a JSON input file and converts it
#   to serenity settings objects. It can return the settings 
#   in both formats.
class SettingsConverter():
    def __init__(self, jsonSettings):
        self.__jsonSettings = jsonSettings
        # o----------o
        # | Settings |
        # o----------o
        self.__sereniypySettings = Settings()
        for outer, inner in self.__jsonSettings.items():
            if (outer.upper() == "NAME"):
                self.__sereniypySettings.name = self.__jsonSettings[outer]
            elif (outer.upper() == "LOAD"):
                self.__sereniypySettings.load = self.__jsonSettings[outer]
            elif (outer.upper() == "SAVEONDISK"):
                self.__sereniypySettings.saveOnDisk = self.__jsonSettings[outer]
            elif (outer.upper() == "CHARGE"):
                self.__sereniypySettings.charge = self.__jsonSettings[outer]
            elif (outer.upper() == "SPIN"):
                self.__sereniypySettings.spin = self.__jsonSettings[outer]
            elif (outer.upper() == "GEOMETRY"):
                self.__sereniypySettings.geometry = self.__jsonSettings[outer]
            elif (outer.upper() == "PATH"):
                self.__sereniypySettings.path = self.__jsonSettings[outer]
            elif (outer.upper() == "SCFMODE"):
                self.__sereniypySettings.scfMode = jr.resolveSCFMode(
                    self.__jsonSettings[outer].upper())
            elif (outer.upper() == "METHOD"):
                self.__sereniypySettings.method = jr.resolveElectronicStructureTheory(
                    self.__jsonSettings[outer].upper())
        # o--------------o
        # | DFT Settings |
        # o--------------o
            elif (outer.upper() == "DFT"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "FUNCTIONAL"):
                        self.__sereniypySettings.dft.functional = jr.resolveFunctional(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "DENSITYFITTING"):
                        self.__sereniypySettings.dft.densityFitting = jr.resolveDensityFitting(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "DISPERSION"):
                        self.__sereniypySettings.dft.dispersion = jr.resolveDispersionCorrection(
                            self.__jsonSettings[outer][innerinner].upper())
        # o--------------o
        # | SCF Settings |
        # o--------------o
            elif (outer.upper() == "SCF"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "INITIALGUESS"):
                        self.__sereniypySettings.scf.initialguess = jr.resolveInitialGuess(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "MAXCYCLES"):
                        self.__sereniypySettings.scf.maxCycles = int(self.__jsonSettings[
                            outer][innerinner])
                    elif (innerinner.upper() == "WRITERESTART"):
                        self.__sereniypySettings.scf.writeRestart = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "ENERGYTHRESHOLD"):
                        self.__sereniypySettings.scf.energyThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "RMSDTHRESHOLD"):
                        self.__sereniypySettings.scf.rmsdThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DAMPING"):
                        self.__sereniypySettings.scf.damping = jr.resolveDamping(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "SERIESDAMPINGSTART"):
                        self.__sereniypySettings.scf.seriesDampingStart = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "SERIESDAMPINGEND"):
                        self.__sereniypySettings.scf.seriesDampingEnd = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "SERIESDAMPINGSTEP"):
                        self.__sereniypySettings.scf.seriesDampingStep = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "SERIESDAMPINGINITIALSTEPS"):
                        self.__sereniypySettings.scf.seriesDampingInitialSteps = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "STATICDAMPINGFACTOR"):
                        self.__sereniypySettings.scf.staticDampingFactor = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "ENDDAMPERR"):
                        self.__sereniypySettings.scf.endDampErr = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "USELEVELSHIFT"):
                        self.__sereniypySettings.scf.useLevelshift = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "USEOFFDIAGLEVELSHIFT"):
                        self.__sereniypySettings.scf.useOffDiagLevelshift = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "MINIMUMLEVELSHIFT"):
                        self.__sereniypySettings.scf.minimumLevelshift = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DIISFLUSH"):
                        self.__sereniypySettings.scf.diisFlush = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DISSSTARTERROR"):
                        self.__sereniypySettings.scf.diisStartError = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DISSMAXSTORE"):
                        self.__sereniypySettings.scf.diisMaxStore = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DIISTHRESHOLD"):
                        self.__sereniypySettings.scf.diisThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "USEADIIS"):
                        self.__sereniypySettings.scf.useADIIS = self.__jsonSettings[outer.upper(
                        ) == "SCF"][innerinner]
            # o----------------o
            # | BASIS Settings |
            # o----------------o
            elif (outer.upper() == "BASIS"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "LABEL"):
                        self.__sereniypySettings.basis.label = self.__jsonSettings[outer][innerinner]
                    elif (innerinner.upper() == "AUXCLABEL"):
                        self.__sereniypySettings.basis.auxCLabel = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "AUXJLABEL"):
                        self.__sereniypySettings.basis.auxJLabel = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "MAKESPHERICALBASIS"):
                        self.__sereniypySettings.basis.makeSphericalBasis = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "INTEGRALTHRESHOLD"):
                        self.__sereniypySettings.basis.integralThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "BASISLIBPATH"):
                        self.__sereniypySettings.basis.basisLibPath = self.__jsonSettings[
                            outer][innerinner]
            # o---------------o
            # | GRID Settings |
            # o---------------o
            elif (outer.upper() == "GRID"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "GRIDTYPE"):
                        self.__sereniypySettings.grid.gridType = jr.resolveGridType(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "RADIALGRIDTYPE"):
                        self.__sereniypySettings.grid.radialGridType = jr.resolveRadialGridType(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "SPHERICALGRIDTYPE"):
                        self.__sereniypySettings.grid.sphericalGridType = jr.resolveSphericalGridType(
                            self.__jsonSettings[outer][innerinner].upper())
                    elif (innerinner.upper() == "BLOCKSIZE"):
                        self.__sereniypySettings.grid.blocksize = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "ACCURACY"):
                        self.__sereniypySettings.grid.accuracy = int(self.__jsonSettings[
                            outer][innerinner])
                    elif (innerinner.upper() == "SMALLGRIDACCURACY"):
                        self.__sereniypySettings.grid.smallGridAccuracy = int(self.__jsonSettings[
                            outer][innerinner])
                    elif (innerinner.upper() == "BLOCKAVETHRESHOLD"):
                        self.__sereniypySettings.grid.blockAveThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "BASFUNCRADIALTHRESHOLD"):
                        self.__sereniypySettings.grid.basFuncRadialThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "WEIGHTTHRESHOLD"):
                        self.__sereniypySettings.grid.weightThreshold = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "SMOOTHING"):
                        self.__sereniypySettings.grid.smoothing = self.__jsonSettings[
                            outer][innerinner]
            # o-----------------o
            # | EFIELD Settings |
            # o-----------------o
            elif (outer.upper() == "EFIELD"):
                for innerinner, _ in inner.items():
                    if (innerinner.upper() == "USE"):
                        self.__sereniypySettings.efield.use = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "ANALYTICAL"):
                        self.__sereniypySettings.efield.analytical = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "POS1"):
                        self.__sereniypySettings.efield.pos1 = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "POS2"):
                        self.__sereniypySettings.efield.pos2 = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "DISTANCE"):
                        self.__sereniypySettings.efield.distance = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "NRINGS"):
                        self.__sereniypySettings.efield.nRings = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "RADIUS"):
                        self.__sereniypySettings.efield.radius = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "FIELDSTRENGTH"):
                        self.__sereniypySettings.efield.fieldStrength = self.__jsonSettings[
                            outer][innerinner]
                    elif (innerinner.upper() == "NAMEOUTPUT"):
                        self.__sereniypySettings.efield.nameOutput = self.__jsonSettings[
                            outer][innerinner]

    ## @brief Provides the settings in JSON format
    #  @return the settings in JSON format
    def getJsonSettings(self):
        return self.__jsonSettings

    ## @brief Provides the serenity settings objects
    #  @return the serenity settings objects
    def getSerenipySettings(self):
        return self.__sereniypySettings

    ## @brief Sets the settings in JSON format
    def setJsonSettings(self, json):
        self.__jsonSettings = json

    ## @brief Sets the serenity settings objects
    def setSerenipySettings(self, serSettings):
        self.__sereniypySettings = serSettings
