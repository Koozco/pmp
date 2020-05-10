'''
Class for a budget item.
'''


class Item:
    '''
    An item has a name and a cost.
    '''


    def __init__(self, name, cost):
        '''
        Constructor with a name and a cost.
        '''
        self._name = name
        self._cost = cost


    def equals(self, other):
        '''
        Equals.
        '''
        if not isinstance(other, self.__class__):
            return False
        return self._name == other.name()


    def __repr__(self):
        '''
        For printing.
        '''
        if self._cost == 1:
            return self._name
        else:
            return '(%s, %d)'%(self.name(), self.cost())


    def name(self):
        '''
        Getter.
        '''
        return self._name


    def cost(self):
        '''
        Getter.
        '''
        return self._cost
