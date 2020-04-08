'''
Class for a vote.
'''


from item import Item


class Vote:
    '''
    A vote is a list of sets which are its components.
    '''


    def __init__(self, components = []):
        '''
        Constructor with a list of components.
        '''
        if components == []:
            self._components = []
        else:
            self._components = components


    def __repr__(self):
        '''
        For printing.
        '''
        ans =  'vote: '
        for i in range(len(self._components)):
            ans += str(self._components[i])
            if i < len(self._components) - 1:
                ans += ' > '
        return ans


    def simple_print(self):
        '''
        Simple printing.
        '''
        ans = ''
        for i in range(len(self._components)):
            for item in self._components[i]:
                ans += '%3s'%(item.name())
            if i < len(self._components) - 1:
                ans += ' > '
        return ans


    def components(self):
        '''
        Getter.
        '''
        return self._components


    def add_component(self, component):
        '''
        Add a component.
        '''
        self._components.append(component)


    def add_components(self, components):
        '''
        Add components.
        '''
        self._components += components


class ApprovalVote(Vote):
    '''
    An approval vote is a dichotomous vote.
    '''


    def __init__(self, approval_set):
        '''
        Constructor with a list of components.
        '''
        Vote.__init__(self, [approval_set])


    def __repr__(self):
        '''
        For printing.
        '''
        ans = 'approval vote: '
        ans += self.get_approvals()
        return ans


    def as_array(self):
        ans = []
        for item in self.approvals():
            ans.append(int(item.name()))
        return ans


    def approvals(self):
        return self.components()[0]


class ApprovalVote2D(ApprovalVote):
    '''
    A 2d approval vote is a dichotomous vote with a position.
    '''


    def __init__(self, position, approval_set):
        '''
        Constructor with a list of components.
        '''
        Vote.__init__(self, [approval_set])
        self._position = position


    def __repr__(self):
        '''
        For printing.
        '''
        ans =  'approval vote 2d: '
        ans += '('
        ans += str(self.approvals())
        ans += ', '
        ans += str(self.position())
        ans += ')'
        return ans


    def position(self):
        '''
        Getter.
        '''
        return self._position
