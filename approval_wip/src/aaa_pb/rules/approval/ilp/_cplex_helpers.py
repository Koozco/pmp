from typing import Callable, List

import cplex


def print_all_variables(problem):
    # type: (cplex.Cplex) -> None
    x = problem.solution.get_values()
    for j in range(problem.variables.get_num()):
        print("{0} = {1}".format(problem.variables.get_names(j), x[j]))
    print("--------------------")
    print("")
    pass


def add_boolean_variable(problem: cplex.Cplex, name: str, obj: float) -> None:
    problem.variables.add(
        obj=[obj],
        lb=[0.0],
        ub=[1.0],
        names=[name],
        types=[problem.variables.type.integer]
    )
    pass


def get_committee_from_boolean_variable_names(
        problem: cplex.Cplex,
        number_of_candidates: int,
        candidate_to_var_name_fun: Callable,
        var_name_to_candidate_fun: Callable) -> List[int]:
    var_names = [candidate_to_var_name_fun(c=c) for c in range(number_of_candidates)]
    var_values = problem.solution.get_values(var_names)
    committee = []
    for name, value in zip(var_names, var_values):
        if value > 0.0:
            committee.append(var_name_to_candidate_fun(name))
    return committee


# TODO remove
def setObjectiveFunction(problem: cplex.Cplex, variables_names: List[str], variables_coefficients: List[float],
                         maximize: bool) -> None:
    problem.objective.set_name("objective123")

    # zero out objective function
    number_of_variables_in_default_objective = len(problem.objective.get_linear())
    problem.objective.set_linear([(idx, 0.0) for idx in range(number_of_variables_in_default_objective)])

    # set objective to epsilon
    problem.objective.set_linear(zip(variables_names, variables_coefficients))

    sense = problem.objective.sense.maximize if maximize else problem.objective.sense.minimize
    problem.objective.set_sense(sense)

    pass


def write(c: cplex.Cplex, file_name: str) -> None:
    import pathlib
    # pathlib.Path("/home/pbatko/src/code-misc/python/voting-rules/piotr/lp-files/").mkdir(parents=False, exist_ok=True)
    # c.write("/home/pbatko/src/code-misc/python/voting-rules/piotr/lp-files/" + file_name)
    # exit(1)
    pass


def suppress_output(
        problem: cplex.Cplex,
        log: bool = True,
        results: bool = True,
        warning: bool = False,
        error: bool = False) -> None:
    problem.set_log_stream(None) if log else None
    problem.set_results_stream(None) if results else None
    problem.set_warning_stream(None) if warning else None
    problem.set_error_stream(None) if error else None
