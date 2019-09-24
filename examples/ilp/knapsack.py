"""
Use pmp.utils.ilp to model problem.
Widely used to compute elections results.

In this case simple example of using ilp interface to optimize knapsack problem.
"""

from pmp.utils.ilp.model import Model
from pmp.utils.ilp import Objective, Sense

# (WEIGHT, VALUE)
items = [
    (4, 5),
    (1, 8),
    (2, 4),
    (3, 0),
    (2, 4),
    (2, 3),
    (2, 5),
    (1, 1)
]

# knapsack capacity
c = 10

n = len(items)

weights = [items[i][0] for i in range(n)]
values = [items[i][1] for i in range(n)]


# Modeling starts here:
def knapsack_model():
    # default uses cplex wrapper
    # see set_solver.py to learn more
    model = Model()

    # x_i - ith item is placed in knapsack
    names = ['x{}'.format(i) for i in range(n)]

    # x's are binary variables, so:
    # lower bounds
    lb = [0] * n

    # upper bounds
    ub = [1] * n

    model.add_variables(names, lb, ub)

    # Now we want to maximize sum of v_i * x_i - sumed values of chosen items
    # Specify if objective function should be MAXIMIZED or MINIMIZED
    model.set_objective_sense(Objective.maximize)

    # set linear objective function:
    # list of variables:
    vars = names

    # list of their coefficients
    coefficients = values

    model.set_objective(vars, coefficients)

    # The only missing thing is to ensure we won't exceed knapsack capacity, let's add a proper constraint!
    # variables
    vars = names

    # their coefficients
    coefficients = weights

    # sense ( eq / lt / gt )
    sense = Sense.lt

    # right side - in our case capacity
    rs = c

    model.add_constraint(vars, coefficients, sense, rs)

    # That's all, problem modeled
    return model


if __name__ == '__main__':
    # Check out results

    model = knapsack_model()
    model.solve()

    solution_type, additional_data = model.get_solution_status()
    print('Solution type: ' + str(solution_type))
    print('Solution status: ' + additional_data['status_str'])

    max_val = model.get_objective_value()
    print('Maximal value: ' + str(max_val))

    # More detailed solution: ( values of all variables )
    print(model.get_solution())
