from enum import Enum


class Sense(Enum):
    eq = 'E'
    lt = 'L'
    gt = 'G'


class Objective(Enum):
    minimize = 0
    maximize = 1


class VariableTypes(Enum):
    int = 1
    continuous = 2
