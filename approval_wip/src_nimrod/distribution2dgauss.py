'''
Class for Gauss 2d distribution.
'''


import random


from position import Position
from distribution2d import Distribution2D


class Distribution2DGauss(Distribution2D):
    '''
    A Gauss distribution has a mean (position) and std (value).
    '''


    def __init__(self, mean, std):
        '''
        A Gauss distribution has a mean (position) and std (value).
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
        return Position(
            random.gauss(self.mean().x(), self.std()),
            random.gauss(self.mean().y(), self.std()))
