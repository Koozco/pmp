from enum import Enum


class Solvers(Enum):
    CPLEX = 1


class Sense(Enum):
    eq = 'E'
    lt = 'L'
    gt = 'G'


class Objective(Enum):
    minimize = 0
    maximize = 1
