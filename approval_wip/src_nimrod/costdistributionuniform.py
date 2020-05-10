'''
Class for uniform cost distribution.
'''


import random


from costdistribution import CostDistribution


class CostDistributionUniform(CostDistribution):
    '''
    A uniform distribution has a and b.
    '''


    def __init__(self, a, b):
        '''
        Empty constructor.
        '''
        super().__init__()
        self._a = a
        self._b = b


    def a(self):
        '''
        Getter.
        '''
        return self._a


    def b(self):
        '''
        Getter.
        '''
        return self._b


    def sample(self):
        '''
        Press the button.
        '''
        return int(random.randint(self.a(), self.b()))
