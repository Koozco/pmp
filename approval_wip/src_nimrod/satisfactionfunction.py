'''
Class for satisfaction functions.
'''


import gurobipy as grb


from items import Items
from budget import Budget


class SatisfactionFunction(object):
    '''
    A satisfaction functions takes A_v and B and returns a value.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        self._name = 'EMPTY'


    def name(self):
        return self._name


    def compute(self, A_v, B):
        '''
        Returns a budget within limit.
        '''
        print('computing in satisfaction function empty')
        print('A_v:',A_v)
        print('B:',B)
        return 5


    def ilp_hook(self, m, x, f, i, vote):
        '''
        Shall make sure that f[i] <= vote satisfaction according to function.
        '''
        print('ilp_hook')
        print('i:',i)
        print('vote:',vote)


    @staticmethod
    def B_v(A_v, B):
        '''
        Returns B_v = A_v \cap B
        '''
        B_v = Items()
        for itemB in B:
            for itemA_v in A_v:
                if itemB.equals(itemA_v):
                    B_v.add_item(itemB)
        return B_v.items()


class SatisfactionFunctionNumberOfBudgetedItems(SatisfactionFunction):
    '''
    Satisfaction function $f(A_v, B) = |B_v|$.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        super().__init__()
        self._name = 'NumberOfBudgetedItems'


    def compute(self, A_v, B):
        '''
        Return |B_v|.
        '''
        B_v = self.B_v(A_v, B)
        return len(B_v)


    def ilp_hook(self, m, x, f, i, vote):
        '''
        Shall make sure that f[i] <= vote satisfaction according to function.
        '''
        m.addConstr(f[i] <= (grb.quicksum(x[i] for i in vote.as_array())), 'vote_%s_constraint'%(str(i)))


class SatisfactionFunctionOneIfSomethingIsBudgeted(SatisfactionFunction):
    '''
    Satisfaction function $f(A_v, B) = 1_{|B_v| > 0}$.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        super().__init__()
        self._name = 'OneIfSomethingIsBudgeted'


    def compute(self, A_v, B):
        '''
        Return |B_v|.
        '''
        B_v = self.B_v(A_v, B)
        return int(len(B_v) > 0)


    def ilp_hook(self, m, x, f, i, vote):
        '''
        Shall make sure that f[i] <= vote satisfaction according to function.
        '''
        ftemp = {}
        ftemp[i] = m.addVar(vtype=grb.GRB.BINARY, name='ftemp[%s]'%(str(i)))
        m.addConstr(ftemp[i] <= (grb.quicksum(x[i] for i in vote.as_array())), 'vote_%s_tempconstraint'%(str(i)))
        m.addConstr(f[i] <= ftemp[i], 'vote_%s_constraint'%(str(i)))


class SatisfactionFunctionMostExpensiveBudgetedItem(SatisfactionFunction):
    '''
    Satisfaction function $f(A_v, B) = max({c(a) : a \in B_v})$.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        super().__init__()
        self._name = 'MostExpenstiveBudgetedItem'


    def compute(self, A_v, B):
        '''
        Return |B_v|.
        '''
        B_v = self.B_v(A_v, B)
        maxCost = 0
        for item in B_v:
            if item.cost() > maxCost:
                maxCost = item.cost()
        return maxCost


    def ilp_hook(self, m, x, f, i, vote):
        '''
        Shall make sure that f[i] <= vote satisfaction according to function.
        '''
        M = max(map(lambda item : item.cost(), vote.approvals()))
        number = len(vote.approvals())

        # m's and b's
        ms = {}
        bs = {}
        for j in range(1, 1 + number):
            ms[i, j] = m.addVar(vtype=grb.GRB.CONTINUOUS, name='m[%s,%s]'%(i, j))
            bs[i, j] = m.addVar(vtype=grb.GRB.BINARY, name='b[%s,%s]'%(i, j))

        # max trick
        for j in range(1, 1 + number):
            item = vote.approvals()[j - 1]
            if j == 1:
                m.addConstr(ms[i, j] >= 0, 'm%s%sa'%(i, j))
                m.addConstr(ms[i, j] >= item.cost() * x[int(item.name())], 'm%s%sb'%(i, j))
                m.addConstr(ms[i, j] <= 0 + M * bs[i, j], 'm%s%sc'%(i, j))
                m.addConstr(ms[i, j] <= item.cost() * x[int(item.name())] + M * (1 - bs[i,j]), 'm%s%sd'%(i, j))
            else:
                m.addConstr(ms[i, j] >= ms[i, j - 1], 'm%s%sa'%(i, j))
                m.addConstr(ms[i, j] >= item.cost() * x[int(item.name())], 'm%s%sb'%(i, j))
                m.addConstr(ms[i, j] <= ms[i, j - 1] + M * bs[i, j], 'm%s%sc'%(i, j))
                m.addConstr(ms[i, j] <= item.cost() * x[int(item.name())]+ M * (1 - bs[i,j]), 'm%s%sd'%(i, j))

        # f[i] gets the max
        m.addConstr(f[i] == ms[i, len(vote.approvals())])


class SatisfactionFunctionTotalBudgetedCost(SatisfactionFunction):
    '''
    Satisfaction function $f(A_v, B) = sum_{a \in B_v} c(a)$.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        super().__init__()
        self._name = 'TotalBudgetedCost'


    def compute(self, A_v, B):
        '''
        Return |B_v|.
        '''
        B_v = self.B_v(A_v, B)
        totalCost = 0
        for item in B_v:
            totalCost += item.cost()
        return totalCost


    def ilp_hook(self, m, x, f, i, vote):
        '''
        Shall make sure that f[i] <= vote satisfaction according to function.
        '''
        m.addConstr(f[i] <= (grb.quicksum(x[int(item.name())] * item.cost() for item in vote.approvals())), 'vote_%s_constraint'%(str(i)))
