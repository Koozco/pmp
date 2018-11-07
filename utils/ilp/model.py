from cplex_wrapper import CplexWrapper
from ilp import Solvers

__wrappers__ = {
    Solvers.CPLEX: CplexWrapper
}


class Model:

    def __init__(self, solver=Solvers.CPLEX):
        self.wrapper = __wrappers__[solver]()

    def solve(self):
        self.wrapper.solve()

    def add_variable(self, name, lb=None, ub=None):
        self.wrapper.add_variable(name, lb, ub)

    def add_variables(self, name, lb=None, ub=None):
        self.wrapper.add_variables(name, lb, ub)

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
