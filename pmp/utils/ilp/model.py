import numpy as np
from .solvers import Solvers, init_solver
from .ilp import VariableTypes

_default_vtype = VariableTypes.int


class Model:

    def __init__(self, solver=Solvers.CPLEX, log_errors=True):
        self._s_module = init_solver(solver)
        self.wrapper = self._s_module.wrapper_class(log_errors=log_errors)

    def solve(self):
        self.wrapper.solve()

    def add_variable(self, name, lb=None, ub=None, vtype=None):
        if vtype is None:
            vtype = _default_vtype
        self.wrapper.add_variable(name, lb, ub, vtype)

    def add_variables(self, name, lb=None, ub=None, vtype=None):
        if vtype is None:
            vtype = np.full(len(name), _default_vtype)
        self.wrapper.add_variables(name, lb, ub, vtype)

    def add_constraint(self, var, coeff, sense, rs):
        self.wrapper.add_constraint(var, coeff, sense, rs)

    def add_constraints(self, var, coeff, sense, rs):
        self.wrapper.add_constraints(var, coeff, sense, rs)

    def set_objective_sense(self, sense):
        self.wrapper.set_objective_sense(sense)

    def set_objective(self, var, coeff):
        self.wrapper.set_objective(var, coeff)

    def write_to_file(self, name):
        self.wrapper.write_to_file(name)

    def get_solution_status(self):
        return self.wrapper.get_solution_status()

    def get_objective_value(self):
        return self.wrapper.get_objective_value()

    def get_solution(self):
        return self.wrapper.get_solution()
