'''
Class for util.
'''


import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    '''
    Visualizer visualizes single elections and creates visual histograms.
    '''


    def __init__(self):
        '''
        Empty constructor.
        '''
        pass


    def visualize_single_election(self, election, budget, filename):
        plt.clf()

        itemsXs = []
        itemsYs = []
        for item in election.items().items():
            itemsXs.append(item.position().x())
            itemsYs.append(item.position().y())
        plt.scatter(itemsXs, itemsYs, c = 'b')

        votesXs = []
        votesYs = []
        for vote in election.votes().votes():
            votesXs.append(vote.position().x())
            votesYs.append(vote.position().y())
        plt.scatter(votesXs, votesYs, c = 'g')

        fundedXs = []
        fundedYs = []
        for funded in budget.items():
            fundedXs.append(funded.position().x())
            fundedYs.append(funded.position().y())
        plt.scatter(fundedXs, fundedYs, c = 'r')

        plt.savefig(filename)
        print('single election is in %s.png'%(filename))


    def create_scatterplot(self, elections, budgets, filename):
        plt.clf()

        fig = plt.gcf()
        fig.set_size_inches(3, 3)

        itemsXs = []
        itemsYs = []
        for election in elections:
            for item in election.items().items():
                itemsXs.append(item.position().x())
                itemsYs.append(item.position().y())
        plt.scatter(itemsXs, itemsYs, c = 'b', alpha = 0.05)

        votesXs = []
        votesYs = []
        for election in elections:
            for vote in election.votes().votes():
                votesXs.append(vote.position().x())
                votesYs.append(vote.position().y())
        plt.scatter(votesXs, votesYs, c = 'g', alpha = 0.05)

        fundedXs = []
        fundedYs = []
        for budget in budgets:
            for funded in budget.items():
                fundedXs.append(funded.position().x())
                fundedYs.append(funded.position().y())
        plt.scatter(fundedXs, fundedYs, c = 'r')

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')

        plt.savefig(filename, figsize=(10, 10))
        print('scatterplot is in %s.png'%(filename))


    def zoom(self, data, x):
        ans = np.zeros([len(data) * x, len(data) * x])
        for i in range(len(data)):
            for j in range(len(data[0])):
                for ii in range(x):
                    for jj in range(x):
                        ans[i * x + ii][j * x + jj] = data[i][j]
        return ans


    def create_histogram(self, elections, budgets, filename):
        plt.clf()

        # resolution and data
        resolution = 50
        data = np.zeros([resolution, resolution])

        # fill in data
        for budget in budgets:
            for funded in budget.items():
                binx = int(funded.position().x() * resolution)
                biny = int(funded.position().y() * resolution)
                data[resolution - binx][biny] += funded.cost()

        # normalize data
        T = np.sum(data)
        for binx in range(resolution):
            for biny in range(resolution):
                if data[binx][biny] > 0:
                    data[binx][biny] = 1 / (np.pi / 2) * np.arctan(data[binx][biny] / (0.0004 * T))
        data = self.zoom(data, 5)
        plt.imsave(filename + '.png', data, format='png', cmap='copper')
        print('histogram is in %s.png'%(filename))
