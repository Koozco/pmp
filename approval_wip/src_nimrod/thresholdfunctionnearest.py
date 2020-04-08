'''
Class for the nearest threshold function.
'''


import operator


from util import Util
from thresholdfunction import ThresholdFunction


class ThresholdFunctionNearest(ThresholdFunction):
    '''
    A threshold function gets vote and items and fills-in an approval set.
    '''


    def __init__(self, k):
        '''
        k is the number of nearest to be approved.
        '''
        super().__init__()
        self._k = k


    def k(self):
        '''
        Getter.
        '''
        return self._k


    def approvals(self, position, items):
        '''
        Returns an approval set for the vote in this position wrt. the items.
        '''
        ans = []
        dict = {}
        for item in items.items():
            dict[item] = Util.dist(position, item.position())
        sorteddict = sorted(dict.items(), key=operator.itemgetter(1))
        for i in range(self.k()):
            ans.append(sorteddict[i][0])
        return ans
