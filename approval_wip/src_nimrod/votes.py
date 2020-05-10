'''
Class for votes.
'''


class Votes:
    '''
    Votes is a list of votes.
    '''


    def __init__(self, votes = []):
        '''
        Constructor with a list of votes.
        '''
        if votes == []:
            self._votes = []
        else:
            self._votes = votes


    def __repr__(self):
        '''
        For printing.
        '''
        ans =  ''
        for i in range(len(self._votes)):
            ans += str(self._votes[i])
            if i < len(self._votes) - 1:
                ans += '\n'
        return ans


    def print_simple(self):
        '''
        Simple printing.
        '''
        ans = ''
        for vote in self._votes:
            ans += vote.simple_print()
            ans += '\n'
        print(ans)


    def votes(self):
        '''
        Getter.
        '''
        return self._votes


    def number_of_votes(self):
        '''
        Number of votes.
        '''
        return len(self._votes)


    def add_vote(self, vote):
        '''
        Add a vote.
        '''
        self._votes.append(vote)


    def add_votes(self, votes):
        '''
        Add votes.
        '''
        self._votes += votes
