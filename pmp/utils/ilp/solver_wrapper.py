class SolverWrapper:

    def solve(self):
        """
        Solve model. Call this after providing a proper setup of the problem.
        """
        raise NotImplementedError()

    def add_variable(self, name, lb, ub, vtype):
        """
        Add single variable to the model
        :param name: name of added variable
        :type name: String
        :param lb: lower bound of added variable
        :type lb: Number
        :param ub: upper bound of added variable
        :type ub: Number
        :param vtype: type of added variable
        :type vtype: VariableTypes
        """
        raise NotImplementedError()

    def add_variables(self, name, lb, ub, vtype):
        """
        Add many variables to the model
        :param name: array of names of added variables
        :type name: Array[String]
        :param lb: array of lower bounds of added variables
        :type lb: Array[Number]
        :param ub: array of upper bounds of added variables
        :type ub: Array[Number]
        :param vtype: array of types of added variables
        :type vtype: Array[VariableTypes]
        """
        raise NotImplementedError()

    def add_constraint(self, var, coeff, sense, rs):
        """
        Add single constraint to the model
        :param var: array of variable names (occurring in the left side of the constraint)
        :type var: Array[String]
        :param coeff: array of coefficients corresponding to the variables
        :type coeff: Array[Number]
        :param sense: constraint kind, ie. less than, equal
        :type sense: Sense
        :param rs: right side of the constraint
        :type rs: Number
        """
        raise NotImplementedError()

    def add_constraints(self, var, coeff, sense, rs):
        """
        Add multiple constraints to the model
        :param var: array of arrays of variable names (occurring in the left side of the constraints)
        :type var: Array[Array[String]]
        :param coeff: array of arrays of coefficients corresponding to the variables
        :type coeff: Array[Array[Number]
        :param sense: array of constraint kinds, ie. less than, equal
        :type sense: Array[Sense]
        :param rs: array of right sides of the constraints
        :type rs: Array[Number]
        """
        raise NotImplementedError()

    def set_objective_sense(self, sense):
        """
        Set sense of the objective function - maximize/minimize
        :param sense: strategy for the objective function
        :type sense: Objective
        """
        raise NotImplementedError()

    def set_objective(self, var, coeff):
        """
        Set objective function
        :param var: variable names of the variables forming linear combination in objective function
        :type var: Array[String]
        :param coeff: array of coefficients corresponding to the variables
        :type coeff: Array[Number]
        :return:
        """
        raise NotImplementedError()

    def write_to_file(self, name):
        """
        Write provided problem setup to the .lp file.
        :param name: name (path) of the file
        :type name: String
        """
        raise NotImplementedError()

    def get_solution_status(self):
        """
        Get status of the solution. Status is available only after solving a model.
        Can provide different additional_data, depending on chosen solver.
        :type solution_type: SolutionType
        :type additional_data: Dict
        :return solution_type, additional_data:
        """
        raise NotImplementedError()

    def get_objective_value(self):
        """
        Get value of the optimized objective function.
        """
        raise NotImplementedError()

    def get_solution(self):
        """
        Get solution of optimized model.
        Solution has a form of dictionary with variable names as keys and variable values.
        :type solution_dict: Dict[String, Number]
        :return solution_dict:
        """
        raise NotImplementedError()
