'''
Class for gauss cost distribution.
'''


import random


from costdistribution import CostDistribution


class CostDistributionGauss(CostDistribution):
    '''
    A uniform distribution has a and b.
    '''


    def __init__(self, mean, std):
        '''
        Constructor with mean and std.
        '''
        super().__init__()
        self._mean = mean
        self._std = std


    def mean(self):
        '''
        Getter.
        '''
        return self._mean


    def std(self):
        '''
        Getter.
        '''
        return self._std


    def sample(self):
        '''
        Press the button.
        '''
        while True:
            t = int(random.gauss(self.mean(), self.std()))
            if t > 0:
                return t
