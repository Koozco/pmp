'''
Class for greedy rules.
'''


import operator
from util import Util
from budget import Budget
from budgetingmethod import BudgetingMethod


class GreedyRule(BudgetingMethod):
    '''
    A greedy rule on top of some given satisfaction function;
    that is, implements $\mathcal{R}^g_f$ for a given $f$.
    '''


    def __init__(self, satisfactionFunction):
        '''
        Constructor with a name.
        '''
        super().__init__('GreedyRule' + satisfactionFunction.name())
        self._satisfaction_function = satisfactionFunction


    def satisfaction_function(self):
        return self._satisfaction_function


    def compute(self, election):
        '''
        Returns a budget within limit.
        '''
        budget = Budget()
        while True:
            bestItem = 0
            bestValue = 0
            for item in election.items().items():
                if item.cost() + budget.total_cost() > election.limit():
                    continue
                value = 0
                # create a temp budget
                tempBudget = Budget()
                for itemm in budget.items():
                    tempBudget.add_item(itemm)
                tempBudget.add_item(item)
                # compute total satisfaction from adding the item
                tempValue = 0
                for vote in election.votes().votes():
                    tempValue += self.satisfaction_function().compute(vote.approvals(), tempBudget.items())
                # update if the best so far
                if tempValue > value:
                    bestValue = tempValue
                    bestItem = item
            # if found something, then add; otherwise return
            if bestValue > 0:
                budget.add_item(bestItem)
            else:
                return budget
