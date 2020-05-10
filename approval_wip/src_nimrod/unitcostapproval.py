'''
Class for unit-cost approval.
'''


import operator
from util import Util
from budget import Budget
from budgetingmethod import BudgetingMethod


class UnitCostApproval(BudgetingMethod):
    '''
    Assumes approval election.
    Assumes unit-cost items.
    Returns limit-many items with most approvals.
    '''


    def __init__(self):
        '''
        Constructor with a name.
        '''
        super().__init__('Unit-cost Approval')


    def compute(self, election):
        '''
        Returns a budget within limit.
        '''
        Util.check_approval_election(election)
        Util.check_unitcost_election(election)
        approvals = {}
        for item in election.items().items():
            approvals[item.name()] = 0
        for vote in election.votes().votes():
            for item in vote.approvals():
                approvals[item.name()] += 1
        sortedApprovals = sorted(approvals.items(), key=operator.itemgetter(1), reverse=True)
        itemNames = list(map(lambda x : x[0], sortedApprovals[0:election.limit()]))
        budget = Budget()
        for itemName in itemNames:
            for item in election.items().items():
                if item.name() == itemName:
                    budget.add_item(item)
        return budget
