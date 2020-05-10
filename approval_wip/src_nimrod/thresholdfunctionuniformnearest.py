'''
Class for the nearest threshold function where k is random.
'''


import random
import operator


from util import Util
from thresholdfunction import ThresholdFunction


class ThresholdFunctionUniformNearest(ThresholdFunction):
    '''
    A threshold function gets vote and items and fills-in an approval set.
    '''


    def __init__(self, a, b):
        '''
        [a, b] is the uniform range for the number of nearest to be approved.
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


    def approvals(self, position, items):
        '''
        Returns an approval set for the vote in this position wrt. the items.
        '''
        ans = []
        dict = {}
        for item in items.items():
            dict[item] = Util.dist(position, item.position())
        sorteddict = sorted(dict.items(), key=operator.itemgetter(1))
        for i in range(random.randint(self.a(), self.b())):
            ans.append(sorteddict[i][0])
        return ans
