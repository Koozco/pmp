class SolverWrapper:

    def solve(self):
        raise NotImplementedError()

    def add_variable(self, name, lb, ub, vtype):
        raise NotImplementedError()

    def add_variables(self, name, lb, ub, vtype):
        raise NotImplementedError()

    def add_constraint(self, var, coeff, sense, rs):
        raise NotImplementedError()

    def add_constraints(self, var, coeff, sense, rs):
        raise NotImplementedError()

    def set_objective_sense(self, sense):
        raise NotImplementedError()

    def set_objective(self, var, coeff):
        raise NotImplementedError()

    def write_to_file(self, name):
        raise NotImplementedError()

    def get_solution_status(self):
        raise NotImplementedError()

    def get_objective_value(self):
        raise NotImplementedError()

    def get_solution(self):
        raise NotImplementedError()
