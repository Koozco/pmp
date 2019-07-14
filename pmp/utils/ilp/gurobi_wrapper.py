from gurobipy import GRB, Model, LinExpr
from .ilp import Objective, VariableTypes, Sense
from .solver_wrapper import SolverWrapper


class GurobiWrapper(SolverWrapper):

    def __init__(self):
        self.model = Model()

    def solve(self):
        self.model.optimize()

    def add_variable(self, name, lb, ub, vtype):
        args = {'name': name}
        if ub is not None:
            args['ub'] = ub
        if lb is not None:
            args['lb'] = lb
        if vtype is not None:
            args['vtype'] = self._var_types_mapping(vtype)

        self.model.addVar(**args)

    def add_variables(self, name, lb, ub, vtype):
        args = {'name': name}
        if ub is not None:
            args['ub'] = ub
        if lb is not None:
            args['lb'] = lb
        if vtype is not None:
            args['vtype'] = [self._var_types_mapping(t) for t in vtype]

        self.model.addVars(len(name), **args)

    def add_constraint(self, var, coeff, sense, rs):
        args = {
            'lhs': LinExpr(coeff, self._gurobi_variables(var)),
            'sense': self._sense_mapping(sense),
            'rhs': rs
        }
        self.model.addConstr(**args)

    def add_constraints(self, var, coeff, sense, rs):
        for constr in zip(var, coeff, sense, rs):
            self.add_constraint(*constr)

    def set_objective_sense(self, sense):
        mapping = {
            Objective.maximize: GRB.MAXIMIZE,
            Objective.minimize: GRB.MINIMIZE
        }
        self.model.ModelSense = mapping[sense]

    def set_objective(self, var, coeff):
        lin_expr = LinExpr(coeff, self._gurobi_variables(var))
        self.model.setObjective(lin_expr)

    def write_to_file(self, name):
        self.model.write(name)

    def get_solution_status(self):
        status = self.model.Status
        return status, self._solution_strings()[status]

    def get_objective_value(self):
        return self.model.ObjVal

    def get_solution(self):
        return {var.VarName: var.X for var in self.model.getVars()}

    def _gurobi_variable(self, name):
        return self.model.getVarByName(name)

    def _gurobi_variables(self, names):
        return [self._gurobi_variable(n) for n in names]

    @staticmethod
    def _sense_mapping(sense):
        mapping = {
            Sense.lt: GRB.LESS_EQUAL,
            Sense.gt: GRB.GREATER_EQUAL,
            Sense.eq: GRB.EQUAL
        }
        return mapping[sense]

    @staticmethod
    def _var_types_mapping(vtype):
        mapping = {
            VariableTypes.int: GRB.INTEGER,
            VariableTypes.continuous: GRB.CONTINUOUS
        }
        return mapping[vtype]

    @staticmethod
    def _solution_strings():
        return {
            1: 'LOADED',
            2: 'OPTIMAL',
            3: 'INFEASIBLE',
            4: 'INF_OR_UNBD',
            5: 'UNBOUNDED',
            6: 'CUTOFF',
            7: 'ITERATION_LIMIT',
            8: 'NODE_LIMIT',
            9: 'TIME_LIMIT',
            10: 'SOLUTION_LIMIT',
            11: 'INTERRUPTED',
            12: 'NUMERIC',
            13: 'SUBOPTIMAL',
            14: 'INPROGRESS',
            15: 'USER_OBJ_LIMIT'
        }


wrapper_class = GurobiWrapper
