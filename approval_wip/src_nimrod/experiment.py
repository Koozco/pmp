'''
Performs experiments.
'''


import sys
import pickle
import numpy as np


from vote import Vote
from item import Item
from items import Items
from votes import Votes
from budget import Budget
from distribution2d import *
from election import Election
from position import Position
from visualizer import Visualizer
from electioncreatorsimple import ElectionCreatorSimple
from unitcostapproval import UnitCostApproval
from costdistributionuniform import CostDistributionUniform


class Experiment:
    '''
    Performs experiments.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        pass

    @staticmethod
    def simple_experiment():
        Election = ElectionCreatorSimple.create_random_approval_election(4, 5, 0.5, 3)
        print(Election)
        budgetingMethod = UnitCostApproval()
        budget = budgetingMethod.compute(Election)
        print(budgetingMethod.name(),'returns:',budget)


    @staticmethod
    def simple_2d_experiment():
        election = ElectionCreator2D.create_random_approval_election(
            5000, Distribution2DUniform(Position(0, 0), Position(1, 1)),
            CostDistributionUniform(1, 1),
            50, Distribution2DUniform(Position(0, 0), Position(1, 1)),
            ThresholdFunctionNearest(1),
            5)
        budgetingMethod = UnitCostApproval()
        budget = budgetingMethod.compute(election)
        print(budgetingMethod.name(), 'returns:', budget)
        visualizer = Visualizer()
        visualizer.visualize_single_election(election, budget)


    @staticmethod
    def create_histogram_simple_creator(
        numberOfItems,
        distributionOfItems,
        distributionOfCosts,
        numberOfVotes,
        distributionOfVotes,
        thresholdFunction,
        budgetLimit,
        budgetingMethod,
        numberOfRepetitions,
        filename):
        elections = []
        budgets = []
        for rep in range(numberOfRepetitions):
            if rep % 10 == 0:
                print('repetition %d (%d)'%(rep, numberOfRepetitions))
                sys.stdout.flush()
            election = ElectionCreator2D.create_random_approval_election(
                numberOfItems,
                distributionOfItems,
                distributionOfCosts,
                numberOfVotes,
                distributionOfVotes,
                thresholdFunction,
                budgetLimit)
            elections.append(election)
            budget = budgetingMethod.compute(election)
            budgets.append(budget)
        visualizer = Visualizer()
        visualizer.create_histogram(
            elections,
            budgets,
            'HIST_' + filename)
        visualizer.create_scatterplot(
            elections,
            budgets,
            'SCATTER_' + filename)


    @staticmethod
    def create_histogram(
        itemsCreator,
        votesCreator,
        budgetLimit,
        budgetingMethod,
        numberOfRepetitions,
        directoryName,
        filename):
        elections = []
        budgets = []
        for rep in range(numberOfRepetitions):
            if rep % 10 == 0:
                print('repetition %d (%d)'%(rep, numberOfRepetitions))
                sys.stdout.flush()
            items = itemsCreator.create()
            votes = votesCreator.create(items)
            election = Election(items, votes, budgetLimit)
            elections.append(election)
            budget = budgetingMethod.compute(election)
            budgets.append(budget)
        visualizer = Visualizer()
        visualizer.create_histogram(
            elections,
            budgets,
            directoryName + '/HIST_' + filename)
        visualizer.create_scatterplot(
            elections,
            budgets,
            directoryName + '/SCATTER_' + filename)
