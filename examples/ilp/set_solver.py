from pmp.utils.ilp.model import Model
from pmp.utils.ilp.solvers import Solvers

# List all available solvers:
print('Available solvers:')
for solver in Solvers:
    print(solver)

# Create model with given solver
model = Model(solver=Solvers.CPLEX)
