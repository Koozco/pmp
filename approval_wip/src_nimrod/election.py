'''
Class for an election.
'''


import itertools
from budget import Budget


class Election:
    '''
    An election includes items, votes, and limit.
    '''


    def __init__(self, items = [], votes = [], limit = -1):
        '''
        Constructor with items, votes, and limit.
        '''
        if items == []:
            self._items = []
        else:
            self._items = items
        if votes == []:
            self._votes = []
        else:
            self._votes = votes
        self._limit = limit


    def __repr__(self):
        '''
        For printing.
        '''
        ans = 'Election\n'
        ans += 'with items: '
        ans += str(self._items)
        ans += ', \n'
        ans += 'limit: '
        ans += str(self._limit)
        ans += ', \n'
        ans += 'and votes:\n'
        ans += str(self._votes)
        return ans


    def items(self):
        '''
        Getter.
        '''
        return self._items


    def votes(self):
        '''
        Getter.
        '''
        return self._votes


    def limit(self):
        '''
        Getter.
        '''
        return self._limit


    def set_limit(self, limit):
        '''
        Setter.
        '''
        self._limit = limit
