'''
Budgeting histograms.
'''


import sys
import time
import calendar
from subprocess import call


from distribution2d import *
from position import Position
from experiment import Experiment
# from maxrule import MaxRule
from electioncreator2d import *
from greedyrule import GreedyRule
# from satisfactionfunction import *
from greedyapproval import GreedyApproval
from unitcostapproval import UnitCostApproval
from costdistributiongauss import CostDistributionGauss
from costdistributionuniform import CostDistributionUniform
from thresholdfunction import *
from thresholdfunctionnearest import *


def create_2d_histograms():
    # Directory
    epoch = calendar.timegm(time.gmtime())
    directoryName = 'plots/' + str(epoch)
    call(['mkdir','-p', directoryName])

    # Items
    itemsCreator = ItemsCreator()
    datas = [
        [Position(0.2, 0.3), 10],
        [Position(0.4, 0.2), 30],
        [Position(0.6, 0.2), 50],
        [Position(0.8, 0.3), 70],
        [Position(0.35, 0.8), 300],
        [Position(0.65, 0.8), 300]
    ]
    for data in datas:
        itemsCreator.add(50,
            Distribution2DGauss(data[0], 0.025),
            CostDistributionGauss(data[1], 1))

    # Votes
    votesCreator = VotesCreator()
    votesCreator.add(100,
        Distribution2DGauss(Position(0.5, 0.5), 0.1),
        ThresholdFunctionNearest(10))
    votesCreator.add(25,
        Distribution2DGauss(Position(0.5, 0.5), 0.5),
        ThresholdFunctionNearest(5))

    # Limit
    budgetLimit = 3000

    # Repetitions
    numberOfRepetitions = 500

    # Budgeting methods
    budgetingMethods = [
        GreedyApproval(),
        # MaxRule(SatisfactionFunctionNumberOfBudgetedItems()),
        # MaxRule(SatisfactionFunctionTotalBudgetedCost()),
        # MaxRule(SatisfactionFunctionOneIfSomethingIsBudgeted())
#        MaxRule(SatisfactionFunctionMostExpensiveBudgetedItem())
    ]

    # Do magic
    for budgetingMethod in budgetingMethods:
        print('Creating for ' + budgetingMethod.name())
        sys.stdout.flush()
        filename = budgetingMethod.name()
        Experiment.create_histogram(
            itemsCreator,
            votesCreator,
            budgetLimit,
            budgetingMethod,
            numberOfRepetitions,
            directoryName,
            filename)

    # Copy main for housekeeping
    call(['cp', 'main.py', directoryName + '/Z_main.py'])


def main():
    print('\nBudgeting histograms\n')
    create_2d_histograms()


if __name__ == '__main__':
    main()
