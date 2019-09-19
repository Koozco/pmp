import cplex
from .ilp import Objective, VariableTypes, SolutionType
from .solver_wrapper import SolverWrapper


class CplexWrapper(SolverWrapper):

    def __init__(self):
        self.model = cplex.Cplex()

    def solve(self):
        self.model.solve()

    def add_variable(self, name, lb, ub, vtype):
        args = {'names': [name]}
        if ub is not None:
            args['ub'] = [ub]
        if lb is not None:
            args['lb'] = [lb]
        if vtype is not None:
            args['types'] = [self._var_types_mapping(vtype)]
        self.model.variables.add(**args)

    def add_variables(self, name, lb, ub, vtype):
        args = {'names': name}
        if ub is not None:
            args['ub'] = ub
        if lb is not None:
            args['lb'] = lb
        if vtype is not None:
            args['types'] = [self._var_types_mapping(t) for t in vtype]
        self.model.variables.add(**args)

    def add_constraint(self, var, coeff, sense, rs):
        args = {
            'lin_expr': [[var, coeff]],
            'senses': sense.value,
            'rhs': [rs]
        }
        self.model.linear_constraints.add(**args)

    def add_constraints(self, var, coeff, sense, rs):
        senses = map(lambda s: s.value, sense)
        senses_str = ''.join(senses)
        args = {
            'lin_expr': list(zip(var, coeff)),
            'senses': senses_str,
            'rhs': rs
        }
        self.model.linear_constraints.add(**args)

    def set_objective_sense(self, sense):
        mapping = {
            Objective.maximize: self.model.objective.sense.maximize,
            Objective.minimize: self.model.objective.sense.minimize
        }
        self.model.objective.set_sense(mapping[sense])

    def set_objective(self, var, coeff):
        self.model.objective.set_linear(list(zip(var, coeff)))

    def write_to_file(self, name):
        self.model.write(name)

    def get_solution_status(self):
        """
        cplex SolutionType:
        https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.3/ilog.odms.cplex.help/refpythoncplex/html/frames.html
        :type solution_type: SolutionType
        :type additional_data: Dict[{'status', 'status_str'}]
        :return solution_type, additional_data:
        """
        cplex_solution_type = self.model.solution.get_solution_type()
        solution_type = SolutionType.feasible if cplex_solution_type != 0 else SolutionType.infeasible

        additional_data = {
            'status': self.model.solution.get_status(),
            'status_str': self.model.solution.status[self.model.solution.get_status()]
        }

        return solution_type, additional_data

    def get_objective_value(self):
        return self.model.solution.get_objective_value()

    def get_solution(self):
        numcols = self.model.variables.get_num()
        names = self.model.variables.get_names()
        vals = self.model.solution.get_values()
        return {names[i]: vals[i] for i in range(numcols)}

    def _var_types_mapping(self, vtype):
        mapping = {
            VariableTypes.int: self.model.variables.type.integer,
            VariableTypes.continuous: self.model.variables.type.continuous
        }
        return mapping[vtype]


wrapper_class = CplexWrapper
