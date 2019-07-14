from enum import Enum
from importlib import import_module


class Solvers(Enum):
    CPLEX = 1
    GUROBI = 2


class MissingSolver(Exception):
    pass


def init_solver(solver):
    try:
        module = import_module(__solver_module_names[solver], __package__)
        return module
    except (ImportError, NameError) as e:
        raise MissingSolver("Couldn't initialize ilp solver. Please check required dependencies.\n" + str(e))


__solver_module_names = {
    Solvers.CPLEX: '.cplex_wrapper',
    Solvers.GUROBI: '.gurobi_wrapper'
}
