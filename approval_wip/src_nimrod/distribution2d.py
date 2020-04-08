'''
Class for 2d distribution.
'''


import random


from position import Position


class Distribution2D:
    '''
    A distribution has a button.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        pass


    def sample(self):
        '''
        Press the button.
        '''
        pass


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


class Distribution2DDisc(Distribution2D):
    '''
    A disc distribution has a center (position) and radius (value).
    '''


    def __init__(self, center, radius):
        '''
        A disc distribution has a center (position) and radius (value).
        '''
        super().__init__()
        self._center = center
        self._radius = radius


    def center(self):
        '''
        Getter.
        '''
        return self._center


    def radius(self):
        '''
        Getter.
        '''
        return self._radius


    def sample(self):
        '''
        Press the button.
        '''
        r = self.radius()
        while True:
            (px, py) = (random.random() * (2 * r) - r, random.random() * (2 * r) - r)
            if (px**2 + py**2 <= r**2):
                return Position(self.center().x() + px, self.center().y() + py)


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
        x = -7
        y = -7
        while not (0 < x < 1 and 0 < y < 1):
            x = random.gauss(self.mean().x(), self.std())
            y = random.gauss(self.mean().y(), self.std())
        return Position(x, y)
