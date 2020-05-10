'''
Class for a budget.
'''


import itertools


class Budget:
    '''
    A budget is a list of items.
    '''


    def __init__(self, items = []):
        '''
        Constructor with a list of items.
        '''
        if items == []:
            self._items = []
        else:
            self._items = items


    def __repr__(self):
        '''
        For printing.
        '''
        ans =  '{'
        for i in range(len(self._items)):
            ans += str(self._items[i])
            if i < len(self._items) - 1:
                ans += ', '
        ans += '}'
        return ans


    def equals(self, other):
        '''
        Equals.
        '''
        if not isinstance(other, self.__class__):
            return False
        for item in self._items:
            in_there = False
            for other_item in other.items():
                if item.equals(other_item):
                    in_there = True
            if not in_there:
                return False
        for item in other._items:
            in_there = False
            for self_item in self.items():
                if item.equals(self_item):
                    in_there = True
            if not in_there:
                return False
        return True


    def items(self):
        '''
        Getter.
        '''
        return self._items


    def add_item(self, item):
        '''
        Add an item.
        '''
        self._items.append(item)


    def add_items(self, items):
        '''
        Add items.
        '''
        self._items += items


    def total_cost(self):
        '''
        The total cost.
        '''
        cost = 0
        for item in self._items:
            cost += item.cost()
        return cost


    def is_within_limit(self, limit):
        '''
        Whether self it within the given limit.
        '''
        return self.total_cost() <= limit
