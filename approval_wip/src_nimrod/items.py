'''
Class for items.
'''


from item import Item
from budget import Budget
import itertools


class Items:
    '''
    Items is a set of items.
    '''


    def __init__(self, items = []):
        '''
        Constructor with items.
        '''
        self._items = items[:]


    def __repr__(self):
        '''
        For printing.
        '''
        ans = '['
        for i in range(len(self._items)):
            ans += str(self._items[i])
            if i < len(self._items) - 1:
                ans += ','
        ans += ']'
        return ans


    def items(self):
        '''
        Getter.
        '''
        return self._items


    def add_item(self, item):
        '''
        Adds and item.
        '''
        self._items.append(item)


    def add_items(self, items):
        '''
        Adds a list of items.
        '''
        self._items += items


    def all_budgets_within_limit(self, limit):
        '''
        A list of all budgets within limit.
        '''
        ans = []
        for size in range(len(self._items) + 1):
            for items in itertools.combinations(self._items, size):
                budget = Budget(items)
                if budget.is_within_limit(limit):
                    ans.append(budget)
        return ans


    def as_arrays(self):
        ans = []
        for item in self.items():
            ans.append([int(item.name()), item.cost(), item])
        return ans
