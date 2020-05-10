'''
Class for greedy approval.
'''


import operator
from util import Util
from budget import Budget
from budgetingmethod import BudgetingMethod


class GreedyApproval(BudgetingMethod):
    '''
    Assumes approval election.
    Order items by decreasing number of approvals;
    then goes over and select projects while respecting the budget limit
    (jumping over items which do not fit when considered).
    '''


    def __init__(self):
        '''
        Constructor with a name.
        '''
        super().__init__('GreedyApproval')


    def compute(self, election):
        '''
        Returns a budget within limit.
        '''
        Util.check_approval_election(election)
        approvals = {}
        for item in election.items().items():
            approvals[item] = 0
        for vote in election.votes().votes():
            for item in vote.approvals():
                approvals[item] += 1
        sortedApprovals = sorted(approvals.items(), key=operator.itemgetter(1), reverse=True)
        orderedItems = list(map(lambda x : x[0], sortedApprovals))
        budget = Budget()
        for item in orderedItems:
            if budget.total_cost() + item.cost() <= election.limit():
                budget.add_item(item)
        return budget
