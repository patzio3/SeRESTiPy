#!/usr/bin/env  python3
#@file   JsonResolver.py
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

import serenipy as spy
import numpy as np

def resolveSCFMode(argument):
    switcher = {
        "RESTRICTED": spy.SCF_MODES.RESTRICTED,
        "UNRESTRICTED": spy.SCF_MODES.UNRESTRICTED,
        spy.SCF_MODES.RESTRICTED: "RESTRICTED",
        spy.SCF_MODES.UNRESTRICTED: "UNRESTRICTED"
    }
    return switcher.get(argument, "Invalid SCFMode!")


def resolveElectronicStructureTheory(argument):
    switcher = {
        "HF": spy.HF,
        "DFT": spy.DFT,
        spy.HF : "HF",
        spy.DFT : "DFT"
    }
    return switcher.get(argument, "Invalid electronic structure theory!")


def resolveDispersionCorrection(argument):
    switcher = {
        "NONE": spy.DFT_DISPERSION_CORRECTIONS.NONE,
        "D3": spy.DFT_DISPERSION_CORRECTIONS.D3,
        "D3ABC": spy.DFT_DISPERSION_CORRECTIONS.D3ABC,
        "D3BJ": spy.DFT_DISPERSION_CORRECTIONS.D3BJ,
        "D3BJABC": spy.DFT_DISPERSION_CORRECTIONS.D3BJABC,
        spy.DFT_DISPERSION_CORRECTIONS.NONE : "NONE",
        spy.DFT_DISPERSION_CORRECTIONS.D3 : "D3",
        spy.DFT_DISPERSION_CORRECTIONS.D3ABC : "D3ABC",
        spy.DFT_DISPERSION_CORRECTIONS.D3BJ : "D3BJ",
        spy.DFT_DISPERSION_CORRECTIONS.D3BJABC : "D3BJABC"

    }
    return switcher.get(argument, "Invalid dispersion correction!")


def resolveInitialGuess(argument):
    switcher = {
        "HCORE": spy.INITIAL_GUESSES.H_CORE,
        "H_CORE": spy.INITIAL_GUESSES.H_CORE,
        "EHT": spy.INITIAL_GUESSES.EHT,
        "ATOM_DENS": spy.INITIAL_GUESSES.ATOM_DENS,
        "ATOMDENS": spy.INITIAL_GUESSES.ATOM_DENS,
        "ATOM_SCF": spy.INITIAL_GUESSES.ATOM_SCF,
        "ATOMSCF": spy.INITIAL_GUESSES.ATOM_SCF,
        "ATOM_SCF_INPLACE": spy.INITIAL_GUESSES.ATOM_SCF_INPLACE,
        "SAP": spy.INITIAL_GUESSES.SAP,
        spy.INITIAL_GUESSES.H_CORE : "HCORE",
        spy.INITIAL_GUESSES.H_CORE : "H_CORE",
        spy.INITIAL_GUESSES.EHT : "EHT",
        spy.INITIAL_GUESSES.ATOM_DENS : "ATOM_DENS",
        spy.INITIAL_GUESSES.ATOM_DENS : "ATOMDENS",
        spy.INITIAL_GUESSES.ATOM_SCF : "ATOM_SCF",
        spy.INITIAL_GUESSES.ATOM_SCF : "ATOMSCF",
        spy.INITIAL_GUESSES.ATOM_SCF_INPLACE : "ATOM_SCF_INPLACE",
        spy.INITIAL_GUESSES.SAP : "SAP"
    }
    return switcher.get(argument, "Invalid initial guess!")


def resolveBasisPurpose(argument):
    switcher = {
        "DEFAULT": spy.BASIS_PURPOSES.DEFAULT,
        "AUX_COULOMB": spy.BASIS_PURPOSES.AUX_COULOMB,
        "MINBAS": spy.BASIS_PURPOSES.MINBAS,
        "HUECKEL": spy.BASIS_PURPOSES.HUECKEL,
        "AUX_CORREL": spy.BASIS_PURPOSES.AUX_CORREL,
        spy.BASIS_PURPOSES.DEFAULT : "DEFAULT",
        spy.BASIS_PURPOSES.AUX_COULOMB : "AUX_COULOMB",
        spy.BASIS_PURPOSES.MINBAS : "MINBAS",
        spy.BASIS_PURPOSES.HUECKEL : "HUECKEL",
        spy.BASIS_PURPOSES.AUX_CORREL : "AUX_CORREL"
    }
    return switcher.get(argument, "Invalid BASIS_PURPOSE!")


def resolveRadialGridType(argument):
    switcher = {
        "BECKE": spy.RADIAL_GRID_TYPES.BECKE,
        "HANDY": spy.RADIAL_GRID_TYPES.HANDY,
        "AHLRICHS": spy.RADIAL_GRID_TYPES.AHLRICHS,
        "KNOWLES": spy.RADIAL_GRID_TYPES.KNOWLES,
        "EQUI": spy.RADIAL_GRID_TYPES.EQUI,
        spy.RADIAL_GRID_TYPES.BECKE : "BECKE",
        spy.RADIAL_GRID_TYPES.HANDY : "HANDY",
        spy.RADIAL_GRID_TYPES.AHLRICHS : "AHLRICHS",
        spy.RADIAL_GRID_TYPES.KNOWLES : "KNOWLES",
        spy.RADIAL_GRID_TYPES.EQUI : "EQUI"
    }
    return switcher.get(argument, "Invalid RADIAL_GRID_TYPE!")


def resolveSphericalGridType(argument):
    switcher = {
        "LEBEDEV": spy.SPHERICAL_GRID_TYPES.LEBEDEV,
        spy.SPHERICAL_GRID_TYPES.LEBEDEV : "LEBEDEV"
    }
    return switcher.get(argument, "Invalid SPHERICAL_GRID_TYPE!")


def resolveGridType(argument):
    switcher = {
        "BECKE": spy.GRID_TYPES.BECKE,
        "VORONOI": spy.GRID_TYPES.VORONOI,
        spy.GRID_TYPES.BECKE : "BECKE",
        spy.GRID_TYPES.VORONOI : "VORONOI"
    }
    return switcher.get(argument, "Invalid GRID_TYPE!")


def resolveGridPurpose(argument):
    switcher = {
        "DEFAULT": spy.GRID_PURPOSES.DEFAULT,
        "SMALL": spy.GRID_PURPOSES.SMALL,
        "PLOT": spy.GRID_PURPOSES.PLOT,
        spy.GRID_PURPOSES.DEFAULT : "DEFAULT",
        spy.GRID_PURPOSES.SMALL : "SMALL",
        spy.GRID_PURPOSES.PLOT : "PLOT"
    }
    return switcher.get(argument, "Invalid GRID_PURPOSE!")


def resolveOptimizationAlgorithm(argument):
    switcher = {
        "SD": spy.OPTIMIZATION_ALGORITHMS.SD,
        "BFGS": spy.OPTIMIZATION_ALGORITHMS.BFGS,
        spy.OPTIMIZATION_ALGORITHMS.SD : "SD",
        spy.OPTIMIZATION_ALGORITHMS.BFGS : "BFGS"
    }
    return switcher.get(argument, "Invalid OPTIMIZATION_ALGORITHM!")


def resolveGradientType(argument):
    switcher = {
        "NUMERICAL": spy.GRADIENT_TYPES.NUMERICAL,
        "ANALYTICAL": spy.GRADIENT_TYPES.ANALYTICAL
    }
    return switcher.get(argument, "Invalid GRADIENT_TYPE!")


def resolveGeometryOptimizationType(argument):
    switcher = {
        "GROUNDSTATE": spy.GEOMETRY_OPTIMIZATION_TYPES.GROUNDSTATE,
        "TS": spy.GEOMETRY_OPTIMIZATION_TYPES.TS
    }
    return switcher.get(argument, "Invalid GEOMETRY_OPTIMIZATION_TYPE!")


def resolveHessianType(argument):
    switcher = {
        "NUMERICAL": spy.HESSIAN_TYPES.NUMERICAL,
        "ANALYTICAL": spy.HESSIAN_TYPES.ANALYTICAL
    }
    return switcher.get(argument, "Invalid HESSIAN_TYPE!")


def resolveLocalizationAlgorithm(argument):
    switcher = {
        "PM": spy.ORBITAL_LOCALIZATION_ALGORITHMS.PIPEK_MEZEY,
        "FB": spy.ORBITAL_LOCALIZATION_ALGORITHMS.FOSTER_BOYS,
        "IAO": spy.ORBITAL_LOCALIZATION_ALGORITHMS.IAO,
        "IBO": spy.ORBITAL_LOCALIZATION_ALGORITHMS.IBO,
        "ER": spy.ORBITAL_LOCALIZATION_ALGORITHMS.EDMISTON_RUEDENBERG,
        "NO": spy.ORBITAL_LOCALIZATION_ALGORITHMS.NON_ORTHOGONAL
    }
    return switcher.get(argument, "Invalid ORBITAL_LOCALIZATION_ALGORITHM!")


def resolveKinEmbeddingMode(argument):
    switcher = {
        "NONE": spy.KIN_EMBEDDING_MODES.NONE,
        "NADDFUNC": spy.KIN_EMBEDDING_MODES.NADDFUNC,
        "LEVELSHIFT": spy.KIN_EMBEDDING_MODES.LEVELSHIFT,
        "HUZINAGA": spy.KIN_EMBEDDING_MODES.HUZINAGA,
        "RECONSTRUCTION": spy.KIN_EMBEDDING_MODES.RECONSTRUCTION
    }
    return switcher.get(argument, "Invalid KIN_EMBEDDING_MODE!")


def resolveCCLevel(argument):
    switcher = {
        "CCSD": spy.CC_LEVEL.CCSD,
        "CCSD_T": spy.CC_LEVEL.CCSD_T
    }
    return switcher.get(argument, "Invalid CC_LEVEL!")


def resolveGaugeOrigin(argument):
    switcher = {
        "CENTEROFMASS": spy.GAUGE_ORIGIN.COM,
        "ORIGIN": spy.GAUGE_ORIGIN.ORIGIN
    }
    return switcher.get(argument, "Invalid gauge origin type!")


def resolveDensityFitting(argument):
    switcher = {
        "RI": spy.DENS_FITS.RI,
        "NORI": spy.DENS_FITS.NORI,
        "NONE": spy.DENS_FITS.NONE
    }
    return switcher.get(argument, "Invalid density fitting method!")


def resolveFunctional(argument):
    switcher = {
        "LDA": spy.XCFUNCTIONALS.LDA,
        "PBE": spy.XCFUNCTIONALS.PBE,
        "BP86": spy.XCFUNCTIONALS.BP86,
        "PW91": spy.XCFUNCTIONALS.PW91,
        "BLYP": spy.XCFUNCTIONALS.BLYP,
        "PBE0": spy.XCFUNCTIONALS.PBE0,
        "B3LYP": spy.XCFUNCTIONALS.B3LYP,
        "B2PLYP": spy.XCFUNCTIONALS.B2PLYP
    }
    return switcher.get(argument, "Invalid exchange--correlation functional!")

def resolveKinFunctional(argument):
    switcher = {
        "PW91K": spy.KINFUNCTIONALS.PW91K,
        "TF": spy.KINFUNCTIONALS.TF,
        "NONE": spy.KINFUNCTIONALS.NONE,
        "PBE2K": spy.KINFUNCTIONALS.PBE2K,
        "PBE2KS": spy.KINFUNCTIONALS.PBE2KS,
        "PBE3K": spy.KINFUNCTIONALS.PBE3K,
        "PBE4K": spy.KINFUNCTIONALS.PBE4K,
        "LLP91K": spy.KINFUNCTIONALS.LLP91K,
        "LLP91KS": spy.KINFUNCTIONALS.LLP91KS,
        "E2000K": spy.KINFUNCTIONALS.E2000K,
    }
    return switcher.get(argument, "Invalid kinetic functional!")


def resolveDamping(argument):
    switcher = {
        "NONE": spy.DAMPING_ALGORITHMS.NONE,
        "STATIC": spy.DAMPING_ALGORITHMS.STATIC,
        "SERIES": spy.DAMPING_ALGORITHMS.SERIES,
        "DYNAMIC": spy.DAMPING_ALGORITHMS.DYNAMIC
    }
    return switcher.get(argument, "Invalid DAMPING_ALGORITHM!")

def resolveResponseAlgorithm(argument):
    switcher = {
        "SYMMETRIC": spy.RESPONSE_ALGORITHM.SYMMETRIC,
        "SYMMETRIZED": spy.RESPONSE_ALGORITHM.SYMMETRIZED,
        "SYMPLECTIC": spy.RESPONSE_ALGORITHM.SYMPLECTIC
    }
    return switcher.get(argument, "Invalid RESPONSE_ALGORITHM!")

def resolveLRSCFType(argument):
    switcher = {
        "ISOLATED": spy.LRSCF_TYPE.ISOLATED,
        "UNCOUPLED": spy.LRSCF_TYPE.UNCOUPLED,
        "COUPLED": spy.LRSCF_TYPE.COUPLED
    }
    return switcher.get(argument, "Invalid LRSCF_TYPE!")

def resolveGauge(argument):
    switcher = {
        "LENGTH": spy.GAUGE.LENGTH,
        "VELOCITY": spy.GAUGE.VELOCITY
    }
    return switcher.get(argument, "Invalid GAUGE!")

def resolveLRMethod(argument):
    switcher = {
        "TDA": spy.LR_METHOD.TDA,
        "TDDFT": spy.LR_METHOD.TDDFT,
        "CC2": spy.LR_METHOD.CC2,
        "CISDINF": spy.LR_METHOD.CISDINF,
        "CISD": spy.LR_METHOD.CISD,
        "ADC2": spy.LR_METHOD.ADC2
    }
    return switcher.get(argument, "Invalid RESPONSE_ALGORITHM!")

def resolveTask(scfmode, task, act=[], env=[], args={}):
    #RESTRICTED
    if (scfmode.upper() == "RESTRICTED"):
        if (task.upper() in ["SCF", "SCFTASK"]):
            return spy.ScfTask_R(act[0])
        elif (task.upper() in ["FDE", "FDETASK"]):
            serenityTaskObject = spy.FDETask_R(act[0], env)
            if (args):
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 1000
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject
        elif (task.upper() in ["CC", "COUPLEDCLUSTERTASK"]):
            return spy.CoupledClusterTask_R(act[0])
        elif (task.upper() in ["DISP", "DISPERSION", "DISPERSIONCORRECTIONTASK"]):
            return spy.DispersionCorrectionTask(act[0])
        elif (task.upper() in ["FAT", "FREEZEANDTHAWTASK"]):
            serenityTaskObject = spy.FreezeAndThawTask_R(act, env)
            if (args):
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 1000
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject
        elif (task.upper() in ["GEOMETRYOPTIMIZATIONTASK", "GEOOPT", "OPT"]):
            return spy.GeometryOptimizationTask_R(act, env)
        elif (task.upper() in ["GRADIENTTASK", "GRADIENT", "GRAD"]):
            return spy.GradientTask_R(act, env)
        elif (task.upper() in ["LOCALIZATIONTASK", "LOC", "LOCALIZATION"]):
            return spy.LocalizationTask(act)
        elif (task.upper() in ["MP2TASK", "MP2"]):
            return spy.MP2Task_R(act[0], env)
        elif (task.upper() in ["MULTIPOLEMOMENTTASK", "MULTI"]):
            return spy.MultipoleMomentTask(act)
        elif (task.upper() in ["PLOTTASK", "PLOT", "CUBEFILETASK", "CUBE"]):
            return spy.PlotTask_R(act, env)
        elif (task.upper() in ["LRSCF", "LRSCFTASK"]):
            serenityTaskObject = spy.LRSCFTask_R(act, env)
            if (args):
                serenityTaskObject.settings.nEigen = int(args["NEIGEN"]) if "NEIGEN" in args else 4
                serenityTaskObject.settings.conv = float(args["CONV"]) if "CONV" in args else 1.0e-5
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 50
                serenityTaskObject.settings.maxSubspaceDimension = int(args["MAXSUBSPACEDIMENSION"]) if "MAXSUBSPACEDIMENSION" in args else int(1e+9)
                serenityTaskObject.settings.dominantThresh = float(args["DOMINANTTHRESH"]) if "DOMINANTTHRESH" in args else 0.85
                serenityTaskObject.settings.analysis = str(args["ANALYSIS"]) if "ANALYSIS" in args else True
                serenityTaskObject.settings.besleyAtoms = int(args["BESLEYATOMS"]) if "BESLEYATOMS" in args else 0
                serenityTaskObject.settings.besleyCutoff = np.array(args["BESLEYCUTOFF"]) if "BESLEYCUTOFF" in args else np.array([])
                serenityTaskObject.settings.excludeProjection = str(args["EXCLUDEPROJECTION"]) if "EXCLUDEPROJECTION   " in args else False
                serenityTaskObject.settings.uncoupledSubspace = np.array(args["UNCOUPLEDSUBSPACE"]) if "UNCOUPLEDSUBSPACE" in args else np.array([])
                serenityTaskObject.settings.fullFDEc = str(args["FULLFDEC"]) if "FULLFDEC   " in args else False
                serenityTaskObject.settings.gaugeOrigin = np.array(args["GAUGEORIGIN"]) if "GAUGEORIGIN" in args else np.array([np.Inf, np.Inf, np.Inf])
                serenityTaskObject.settings.frequencies = np.array(args["FREQUENCIES"]) if "FREQUENCIES" in args else np.array([])
                serenityTaskObject.settings.frequencyRange = np.array(args["GREQUENCYRANGE"]) if "GREQUENCYRANGE" in args else np.array([])
                serenityTaskObject.settings.damping = float(args["DAMPING"]) if "DAMPING" in args else 0.0
                serenityTaskObject.settings.couplingPattern = np.array(args["COUPLINGPATTERN"]) if "COUPLINGPATTERN" in args else np.array([])
                serenityTaskObject.settings.saveResponseMatrix = str(args["SAVERESPONSEMATRIX"]) if "SAVERESPONSEMATRIX" in args else False
                serenityTaskObject.settings.diis = str(args["DIIS"]) if "DIIS" in args else True
                serenityTaskObject.settings.diisStore = int(args["DIISSTORE"]) if "DIISSTORE" in args else 50
                serenityTaskObject.settings.preopt = float(args["PREOPT"]) if "PREOPT" in args else 1.0e-3
                serenityTaskObject.settings.ccprops = str(args["CCPROPS"]) if "CCPROPS" in args else False
                serenityTaskObject.settings.sss = float(args["SSS"]) if "SSS" in args else 1.0
                serenityTaskObject.settings.oss = float(args["OSS"]) if "OSS" in args else 1.0
                serenityTaskObject.settings.nafThresh = float(args["NAFTHRESH"]) if "NAFTHRESH" in args else 0.0
                serenityTaskObject.settings.samedensity = np.array(args["SAMEDENSITY"]) if "SAMEDENSITY" in args else np.array([])
                serenityTaskObject.settings.subsystemgrid = np.array([int(args["SUBSYSTEMGRID"])]) if "SUBSYSTEMGRID" in args else np.array([])
                serenityTaskObject.settings.rpaScreening = str(args["RPASCREENING"]) if "RPASCREENING" in args else False
                serenityTaskObject.settings.transitionCharges = True #bool(args["TRANISITIONCHARGES"]) if "TRANISITIONCHARGES" in args else False
                serenityTaskObject.settings.partialResponseConstruction = str(args["PARTIALRESPONSECONSTRUCTION"]) if "PARTIALRESPONSECONSTRUCTION" in args else False
                serenityTaskObject.settings.grimme = str(args["GRIMME"]) if "GRIMME" in args else False
                serenityTaskObject.settings.adaptivePrescreening = str(args["ADAPTIVESCREENING"]) if "ADAPTIVESCREENING" in args else True
                serenityTaskObject.settings.algorithm = resolveResponseAlgorithm(args["ALGORITHM"]) if "ALGORITHM" in args else spy.RESPONSE_ALGORITHM.SYMMETRIC
                serenityTaskObject.settings.func = resolveFunctional(args["FUNC"]) if "FUNC" in args else spy.XCFUNCTIONALS.NONE
                serenityTaskObject.settings.loadType = resolveLRSCFType(args["LOADTYPE"]) if "LOADTYPE" in args else spy.LRSCF_TYPE.UNCOUPLED
                serenityTaskObject.settings.gauge = resolveGauge(args["GAUGE"]) if "GAUGE" in args else spy.GAUGE.LENGTH
                serenityTaskObject.settings.method = resolveLRMethod(args["METHOD"]) if "METHOD" in args else spy.LR_METHOD.TDDFT
                serenityTaskObject.settings.densFitJ = resolveDensityFitting(args["DENSFITJ"]) if "DENSFITJ" in args else spy.DENS_FITS.RI
                serenityTaskObject.settings.densFitK = resolveDensityFitting(args["DENSFITK"]) if "DENSFITK" in args else spy.DENS_FITS.NONE
                serenityTaskObject.settings.densFitLRK = resolveDensityFitting(args["DENSFITLRK"]) if "DENSFITLRK" in args else spy.DENS_FITS.NONE
                serenityTaskObject.settings.densFitCache = resolveDensityFitting(args["DENSFITCACHE"]) if "DENSFITCACHE" in args else spy.DENS_FITS.RI
                #Look for proper grid settings passing
                serenityTaskObject.settings.grid.smallGridAccuracy = int(args["SMALLGRIDACCURACY"]) if "SMALLGRIDACCURACY" in args else 4
                serenityTaskObject.settings.grid.accuracy = int(args["ACCURACY"]) if "ACCURACY" in args else 4
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject
    #UNRESTRICTED
    elif (scfmode.upper() == "UNRESTRICTED"):
        if (task.upper() in ["SCF", "SCFTASK"]):
            return spy.ScfTask_U(act[0])
        elif (task.upper() in ["FDE", "FDETASK"]):
            serenityTaskObject = spy.FDETask_U(act[0], env)
            if (args):
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 1000
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject
        elif (task.upper() in ["CC", "COUPLEDCLUSTERTASK"]):
            return spy.CoupledClusterTask_U(act[0])
        elif (task.upper() in ["DISP", "DISPERSION", "DISPERSIONCORRECTIONTASK"]):
            return spy.DispersionCorrectionTask(act[0])
        elif (task.upper() in ["FAT", "FREEZEANDTHAWTASK"]):
            serenityTaskObject = spy.FreezeAndThawTask_U(act, env)
            if (args):
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 1000
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject
        elif (task.upper() in ["GEOMETRYOPTIMIZATIONTASK", "GEOOPT", "OPT"]):
            return spy.GeometryOptimizationTask_U(act, env)
        elif (task.upper() in ["GRADIENTTASK", "GRADIENT", "GRAD"]):
            return spy.GradientTask_U(act, env)
        elif (task.upper() in ["LOCALIZATIONTASK", "LOC", "LOCALIZATION"]):
            return spy.LocalizationTask(act)
        elif (task.upper() in ["MP2TASK", "MP2"]):
            return spy.MP2Task_U(act[0], env)
        elif (task.upper() in ["MULTIPOLEMOMENTTASK", "MULTI"]):
            return spy.MultipoleMomentTask(act)
        elif (task.upper() in ["PLOTTASK", "PLOT", "CUBEFILETASK", "CUBE"]):
            return spy.PlotTask_U(act, env)
        elif (task.upper() in ["LRSCF", "LRSCFTASK"]):
            serenityTaskObject = spy.LRSCFTask_U(act, env)
            if (args):
                serenityTaskObject.settings.nEigen = int(args["NEIGEN"]) if "NEIGEN" in args else 4
                serenityTaskObject.settings.conv = float(args["CONV"]) if "CONV" in args else 1.0e-5
                serenityTaskObject.settings.maxCycles = int(args["MAXCYCLES"]) if "MAXCYCLES" in args else 50
                serenityTaskObject.settings.maxSubspaceDimension = int(args["MAXSUBSPACEDIMENSION"]) if "MAXSUBSPACEDIMENSION" in args else int(1e+9)
                serenityTaskObject.settings.dominantThresh = float(args["DOMINANTTHRESH"]) if "DOMINANTTHRESH" in args else 0.85
                serenityTaskObject.settings.analysis = str(args["ANALYSIS"]) if "ANALYSIS" in args else True
                serenityTaskObject.settings.besleyAtoms = int(args["BESLEYATOMS"]) if "BESLEYATOMS" in args else 0
                serenityTaskObject.settings.besleyCutoff = np.array(args["BESLEYCUTOFF"]) if "BESLEYCUTOFF" in args else np.array([])
                serenityTaskObject.settings.excludeProjection = str(args["EXCLUDEPROJECTION"]) if "EXCLUDEPROJECTION   " in args else False
                serenityTaskObject.settings.uncoupledSubspace = np.array(args["UNCOUPLEDSUBSPACE"]) if "UNCOUPLEDSUBSPACE" in args else np.array([])
                serenityTaskObject.settings.fullFDEc = str(args["FULLFDEC"]) if "FULLFDEC   " in args else False
                serenityTaskObject.settings.gaugeOrigin = np.array(args["GAUGEORIGIN"]) if "GAUGEORIGIN" in args else np.array([np.Inf, np.Inf, np.Inf])
                serenityTaskObject.settings.frequencies = np.array(args["FREQUENCIES"]) if "FREQUENCIES" in args else np.array([])
                serenityTaskObject.settings.frequencyRange = np.array(args["GREQUENCYRANGE"]) if "GREQUENCYRANGE" in args else np.array([])
                serenityTaskObject.settings.damping = float(args["DAMPING"]) if "DAMPING" in args else 0.0
                serenityTaskObject.settings.couplingPattern = np.array(args["COUPLINGPATTERN"]) if "COUPLINGPATTERN" in args else np.array([])
                serenityTaskObject.settings.saveResponseMatrix = str(args["SAVERESPONSEMATRIX"]) if "SAVERESPONSEMATRIX" in args else False
                serenityTaskObject.settings.diis = str(args["DIIS"]) if "DIIS" in args else True
                serenityTaskObject.settings.diisStore = int(args["DIISSTORE"]) if "DIISSTORE" in args else 50
                serenityTaskObject.settings.preopt = float(args["PREOPT"]) if "PREOPT" in args else 1.0e-3
                serenityTaskObject.settings.ccprops = str(args["CCPROPS"]) if "CCPROPS" in args else False
                serenityTaskObject.settings.sss = float(args["SSS"]) if "SSS" in args else 1.0
                serenityTaskObject.settings.oss = float(args["OSS"]) if "OSS" in args else 1.0
                serenityTaskObject.settings.nafThresh = float(args["NAFTHRESH"]) if "NAFTHRESH" in args else 0.0
                serenityTaskObject.settings.samedensity = np.array(args["SAMEDENSITY"]) if "SAMEDENSITY" in args else np.array([])
                serenityTaskObject.settings.subsystemgrid = np.array([int(args["SUBSYSTEMGRID"])]) if "SUBSYSTEMGRID" in args else np.array([])
                serenityTaskObject.settings.rpaScreening = str(args["RPASCREENING"]) if "RPASCREENING" in args else False
                serenityTaskObject.settings.transitionCharges = str(args["TRANISITIONCHARGES"]) if "TRANISITIONCHARGES" in args else False
                serenityTaskObject.settings.partialResponseConstruction = str(args["PARTIALRESPONSECONSTRUCTION"]) if "PARTIALRESPONSECONSTRUCTION" in args else False
                serenityTaskObject.settings.grimme = str(args["GRIMME"]) if "GRIMME" in args else False
                serenityTaskObject.settings.adaptivePrescreening = str(args["ADAPTIVESCREENING"]) if "ADAPTIVESCREENING" in args else True
                serenityTaskObject.settings.algorithm = resolveResponseAlgorithm(args["ALGORITHM"]) if "ALGORITHM" in args else spy.RESPONSE_ALGORITHM.SYMMETRIC
                serenityTaskObject.settings.func = resolveFunctional(args["FUNC"]) if "FUNC" in args else spy.XCFUNCTIONALS.NONE
                serenityTaskObject.settings.loadType = resolveLRSCFType(args["LOADTYPE"]) if "LOADTYPE" in args else spy.LRSCF_TYPE.UNCOUPLED
                serenityTaskObject.settings.gauge = resolveGauge(args["GAUGE"]) if "GAUGE" in args else spy.GAUGE.LENGTH
                serenityTaskObject.settings.method = resolveLRMethod(args["METHOD"]) if "METHOD" in args else spy.LR_METHOD.TDDFT
                serenityTaskObject.settings.densFitJ = resolveDensityFitting(args["DENSFITJ"]) if "DENSFITJ" in args else spy.DENS_FITS.RI
                serenityTaskObject.settings.densFitK = resolveDensityFitting(args["DENSFITK"]) if "DENSFITK" in args else spy.DENS_FITS.NONE
                serenityTaskObject.settings.densFitLRK = resolveDensityFitting(args["DENSFITLRK"]) if "DENSFITLRK" in args else spy.DENS_FITS.NONE
                serenityTaskObject.settings.densFitCache = resolveDensityFitting(args["DENSFITCACHE"]) if "DENSFITCACHE" in args else spy.DENS_FITS.RI
                #Look for proper grid settings passing
                serenityTaskObject.settings.grid.smallGridAccuracy = int(args["SMALLGRIDACCURACY"]) if "SMALLGRIDACCURACY" in args else 4
                serenityTaskObject.settings.grid.accuracy = int(args["ACCURACY"]) if "ACCURACY" in args else 4
                serenityTaskObject.settings.embedding.embeddingMode = resolveKinEmbeddingMode(args["EMB"]["EMBEDDINGMODE"]) if "EMBEDDINGMODE" in args["EMB"] else spy.KIN_EMBEDDING_MODES.NADDFUNC
                serenityTaskObject.settings.embedding.naddXCFunc = resolveFunctional(args["EMB"]["NADDXCFUNC"]) if "NADDXCFUNC" in args["EMB"] else spy.XCFUNCTIONALS.PW91
                serenityTaskObject.settings.embedding.naddKinFunc = resolveKinFunctional(args["EMB"]["NADDKINFUNC"]) if "NADDKINFUNC" in args["EMB"] else spy.KINFUNCTIONALS.PW91K
            return serenityTaskObject


