'''
Class for max rules.
'''


import time
# import gurobipy as grb


import operator
from util import Util
from budget import Budget
from budgetingmethod import BudgetingMethod


class MaxRule(BudgetingMethod):
    '''
    A max rule on top of some given satisfaction function;
    that is, implements $\mathcal{R}^m_f$ for a given $f$.
    '''


    def __init__(self, satisfactionFunction):
        '''
        Constructor with a name.
        '''
        super().__init__('MaxRule' + satisfactionFunction.name())
        self._satisfaction_function = satisfactionFunction


    def satisfaction_function(self):
        return self._satisfaction_function


    def compute(self, election):
        '''
        Returns a budget within limit.
        '''
        budget = Budget()
        itemsArray = election.items().as_arrays()

        varNameToItem = {}

        # Create a new model
        m = grb.Model('maxRuleModel')

        # Create variables
        x = {}
        for itemArray in itemsArray:
            name = itemArray[0]
            cost = itemArray[1]
            x[name] = m.addVar(vtype=grb.GRB.BINARY, name='x[%s]'%(name))
            varNameToItem['x[%s]'%(name)] = itemArray[2]
        f = {}
        for i in range(len(election.votes().votes())):
            f[i] = m.addVar(vtype=grb.GRB.CONTINUOUS, name='f[%s]'%(str(i)))

        # Add budget constraint
        m.addConstr(grb.quicksum([x[itemArray[0]] * itemArray[1] for itemArray in itemsArray]) <= election.limit(), 'budget_constraint')

        # Add satisfaction constraints
        for i in range(len(election.votes().votes())):
            self.satisfaction_function().ilp_hook(m, x, f, i, election.votes().votes()[i])

        # Set objective
        m.setObjective(
            grb.quicksum(f[i] for i in range(len(election.votes().votes()))),
            grb.GRB.MAXIMIZE
        )

        # Optimize
        # m.write('tmp.lp')
        m.setParam(grb.GRB.Param.LogToConsole, 0)
        m.optimize()

        for itemArray in itemsArray:
            v = m.getVarByName('x[%s]'%(itemArray[0]))
            if v.x > 0.5:
                budget.add_item(varNameToItem[v.varName])

        return budget
