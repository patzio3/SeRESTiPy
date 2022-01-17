import serenipy as spy


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
    }
    return switcher.get(argument, "Invalid electronic structure theory!")


def resolveDispersionCorrection(argument):
    switcher = {
        "NONE": spy.DFT_DISPERSION_CORRECTIONS.NONE,
        "D3": spy.DFT_DISPERSION_CORRECTIONS.D3,
        "D3ABC": spy.DFT_DISPERSION_CORRECTIONS.D3ABC,
        "D3BJ": spy.DFT_DISPERSION_CORRECTIONS.D3BJ,
        "D3BJABC": spy.DFT_DISPERSION_CORRECTIONS.D3BJABC
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
        "SAP": spy.INITIAL_GUESSES.SAP
    }
    return switcher.get(argument, "Invalid initial guess!")


def resolveBasisPurpose(argument):
    switcher = {
        "DEFAULT": spy.BASIS_PURPOSES.DEFAULT,
        "AUX_COULOMB": spy.BASIS_PURPOSES.AUX_COULOMB,
        "MINBAS": spy.BASIS_PURPOSES.MINBAS,
        "HUECKEL": spy.BASIS_PURPOSES.HUECKEL,
        "AUX_CORREL": spy.BASIS_PURPOSES.AUX_CORREL
    }
    return switcher.get(argument, "Invalid BASIS_PURPOSE!")


def resolveRadialGridType(argument):
    switcher = {
        "BECKE": spy.RADIAL_GRID_TYPES.BECKE,
        "HANDY": spy.RADIAL_GRID_TYPES.HANDY,
        "AHLRICHS": spy.RADIAL_GRID_TYPES.AHLRICHS,
        "KNOWLES": spy.RADIAL_GRID_TYPES.KNOWLES,
        "EQUI": spy.RADIAL_GRID_TYPES.EQUI
    }
    return switcher.get(argument, "Invalid RADIAL_GRID_TYPE!")


def resolveSphericalGridType(argument):
    switcher = {
        "LEBEDEV": spy.SPHERICAL_GRID_TYPES.LEBEDEV
    }
    return switcher.get(argument, "Invalid SPHERICAL_GRID_TYPE!")


def resolveGridType(argument):
    switcher = {
        "BECKE": spy.GRID_TYPES.BECKE,
        "VORONOI": spy.GRID_TYPES.VORONOI
    }
    return switcher.get(argument, "Invalid GRID_TYPE!")


def resolveGridPurpose(argument):
    switcher = {
        "DEFAULT": spy.GRID_PURPOSES.DEFAULT,
        "SMALL": spy.GRID_PURPOSES.SMALL,
        "PLOT": spy.GRID_PURPOSES.PLOT
    }
    return switcher.get(argument, "Invalid GRID_PURPOSE!")


def resolveOptimizationAlgorithm(argument):
    switcher = {
        "SD": spy.OPTIMIZATION_ALGORITHMS.SD,
        "BFGS": spy.OPTIMIZATION_ALGORITHMS.BFGS
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
        "NADDFUNC": spy.KIN_EMBEDDING_MODES.NADD_FUNC,
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


def resolveDamping(argument):
    switcher = {
        "NONE": spy.DAMPING_ALGORITHMS.NONE,
        "STATIC": spy.DAMPING_ALGORITHMS.STATIC,
        "SERIES": spy.DAMPING_ALGORITHMS.SERIES,
        "DYNAMIC": spy.DAMPING_ALGORITHMS.DYNAMIC
    }
    return switcher.get(argument, "Invalid DAMPING_ALGORITHM!")


def resolveTask(scfmode, task, act=[], env=[], args=[]):
    if (scfmode.upper() == "RESTRICTED"):
        if (task.upper() in ["SCF", "SCFTASK"]):
            return spy.ScfTask_R(act[0])
        elif (task.upper() in ["FDE", "FDETASK"]):
            return spy.FDETask_R(act[0], env)
        elif (task.upper() in ["CC", "COUPLEDCLUSTERTASK"]):
            return spy.CoupledClusterTask_R(act[0])
        elif (task.upper() in ["DISP", "DISPERSION", "DISPERSIONCORRECTIONTASK"]):
            return spy.DispersionCorrectionTask(act[0])
        elif (task.upper() in ["FAT", "FREEZEANDTHAWTASK"]):
            return spy.FreezeAndThawTask_R(act, env)
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
    elif (scfmode.upper() == "UNRESTRICTED"):
        if (task.upper() in ["SCF", "SCFTASK"]):
            return spy.ScfTask_U(act[0])
        elif (task.upper() in ["FDE", "FDETASK"]):
            return spy.FDETask_U(act[0], env)
        elif (task.upper() in ["CC", "COUPLEDCLUSTERTASK"]):
            return spy.CoupledClusterTask_U(act[0])
        elif (task.upper() in ["DISP", "DISPERSION", "DISPERSIONCORRECTIONTASK"]):
            return spy.DispersionCorrectionTask(act[0])
        elif (task.upper() in ["FAT", "FREEZEANDTHAWTASK"]):
            return spy.FreezeAndThawTask_U(act, env)
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


