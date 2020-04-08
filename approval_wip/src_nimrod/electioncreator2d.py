'''
Class for creating 2d elections.
'''


import random
import numpy as np
from item import Item
from item2d import Item2D
from position import Position
from vote import Vote, ApprovalVote, ApprovalVote2D
from items import Items
from votes import Votes
from election import Election


class ItemsCreator:
    '''
    Creates items.
    '''


    def __init__(self):
        '''
        Empty constructor.
        Each datapoint in data is a tuple (numberOfItems, itemsDistribution, costDistribution).
        '''
        self._data = []


    def data(self):
        return self._data


    def add(self, numberOfItems, itemsDistribution, costDistribution):
        self.data().append([numberOfItems, itemsDistribution, costDistribution])


    def create(self):
        items = Items()
        index = 1
        for datapoint in self.data():
            numberOfItems = datapoint[0]
            itemsDistribution = datapoint[1]
            costDistribution = datapoint[2]
            for j in range(1, numberOfItems + 1):
                item = Item2D(str(index), costDistribution.sample(), itemsDistribution.sample())
                items.add_item(item)
                index += 1
        return items


class VotesCreator:
    '''
    Creates votes.
    '''


    def __init__(self):
        '''
        Empty constructor.
        Each datapoint in data is a tuple (numberOfVotes, votesDistribution, thresholdFunction).
        '''
        self._data = []


    def data(self):
        return self._data


    def add(self, numberOfVotes, votesDistribution, thresholdFunction):
        self.data().append([numberOfVotes, votesDistribution, thresholdFunction])


    def create(self, items):
        votes = Votes()
        for datapoint in self.data():
            numberOfVotes = datapoint[0]
            votesDistribution = datapoint[1]
            thresholdFunction = datapoint[2]
            for i in range(1, numberOfVotes + 1):
                position = votesDistribution.sample()
                approvals = thresholdFunction.approvals(position, items)
                votes.add_vote(ApprovalVote2D(position, approvals))
        return votes
