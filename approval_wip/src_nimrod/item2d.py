'''
Class for a 2d budget item.
'''


from item import Item


class Item2D(Item):
    '''
    A 2d item has a name, a cost, and position.
    '''


    def __init__(self, name, cost, position):
        '''
        Constructor with a name, a cost, and position.
        '''
        super().__init__(name, cost)
        self._position = position


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
            return '(%s, $%d, %s)'%(self.name(), self.cost(), self.position())


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


    def position(self):
        '''
        Getter.
        '''
        return self._position
