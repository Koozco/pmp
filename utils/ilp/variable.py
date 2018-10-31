from enum import Enum


class ILP(Enum):
    BINARY = 1
    INTEGER = 2


class VarError(Exception):

    def __init__(self, msg, variable):
        self.variable = variable
        self.msg = msg


class Variable:

    def __init__(self, name, vtype, lower_bound=None, upper_bound=None):
        self.name = name
        self.vtype = vtype
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        for check in Variable.checks():
            check(self)

    #TODO ovverride to str

    @classmethod
    def checks(cls):
        return [cls.binary_check, cls.bounds_check]

    @classmethod
    def binary_check(cls, var):
        if var.vtype == ILP.BINARY and (var.lower_bound is not None or var.upper_bound is not None):
            raise VarError("Binary var should't have bounds.", var)

    @classmethod
    def bounds_check(cls, var):
        if var.lower_bound is not None and var.upper_bound is not None and var.lower_bound > var.upper_bound:
            raise VarError("Upper bound can't be higher than lower bound.", var)

    # def __mul__(self, other):
    #     print(self, other)
    #     return self
    #
    # def __rmul__(self, other):
    #     print(self, other)
    #     return self