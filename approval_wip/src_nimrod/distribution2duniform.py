'''
Class for uniform 2d distribution.
'''


import random


from position import Position
from distribution2d import Distribution2D


class Distribution2DUniform(Distribution2D):
    '''
    A uniform distribution has bottomleft and upperright (both being positions).
    '''


    def __init__(self, bottomleft, upperright):
        '''
        A uniform distribution has bottomleft and upperright (both being positions).
        '''
        super().__init__()
        self._bottomleft = bottomleft
        self._upperright = upperright


    def bottomleft(self):
        '''
        Getter.
        '''
        return self._bottomleft


    def upperright(self):
        '''
        Getter.
        '''
        return self._upperright


    def sample(self):
        '''
        Press the button.
        '''
        return Position(
            self.bottomleft().x() + random.random() * (self.upperright().x() - self.bottomleft().x()),
            self.bottomleft().y() + random.random() * (self.upperright().y() - self.bottomleft().y()))
