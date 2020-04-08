'''
Class for budgeting methods.
'''


from budget import Budget


class BudgetingMethod(object):
    '''
    A budgeting method has a name and,
    given an election, returns a budget within limit.
    '''


    def __init__(self, name):
        '''
        Constructor with a name.
        '''
        self._name = name


    def name(self):
        '''
        Getter.
        '''
        return self._name


    def compute(self, election):
        '''
        Returns a budget within limit.
        '''
        return Budget()
