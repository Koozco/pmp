'''
Class for a 2d position.
'''


class Position:
    '''
    A position has x and y.
    '''


    def __init__(self, x, y):
        '''
        Constructor with x and y.
        '''
        self._x = x
        self._y = y


    def __repr__(self):
        '''
        For printing.
        '''
        return '(%.2f, %.2f)'%(self.x(), self.y())


    def x(self):
        '''
        Getter.
        '''
        return self._x


    def y(self):
        '''
        Getter.
        '''
        return self._y
