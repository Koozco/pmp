'''
Class for creating simple elections.
'''


import random
import numpy as np
from item import Item
from vote import Vote, ApprovalVote
from items import Items
from votes import Votes
from election import Election


class ElectionCreatorSimple:
    '''
    Creates simple elections.
    '''


    @staticmethod
    def create_random_election_with_gaussian_costs(n, m, gauss_mean, gauss_std, limit = -1):
        '''
        n votes over c1,...,cm with Gaussian costs.
        '''
        items = []
        for j in range(1, m + 1):
            cost = np.random.normal(gauss_mean, gauss_std, 1)
            if cost < 1:
                cost = [1]
            items.append(Item('c' + str(j), int(cost[0])))
        items = Items()
        for item in items:
            items.add_item(item)
        votes = Votes()
        for i in range(n):
            tempitems = items[:]
            random.shuffle(tempitems)
            vote = Vote()
            for item in tempitems:
                vote.add_component([item])
            votes.add_vote(vote)
        return Election(items, votes, limit)


    @staticmethod
    def create_random_approval_election(n, m, p, limit = -1):
        '''
        n approval votes over c1,...,cm all cost 1
        where independent probability of vote approving some item is p.
        '''
        itemsarray = []
        for j in range(1, m + 1):
            itemsarray.append(Item(str(j), 1))
        items = Items()
        for item in itemsarray:
            items.add_item(item)
        votes = Votes()
        for i in range(n):
            approvalset = []
            for item in itemsarray:
                if (random.random() < p):
                    approvalset.append(item)
            vote = ApprovalVote(approvalset)
            votes.add_vote(vote)
        return Election(items, votes, limit)
