import os

from pmp.experiments import process_win_dir
from pmp.experiments import Histogram


class DistributionHistograms:
    def __init__(self):
        self.histograms = {}

    def __call__(self, candidates, winners, election, voters, preferences):
        election_id = election.split('_')[0]
        histogram = self._get_histogram(election_id)

        winners_attributes = [candidates[i] for i in winners]
        winners_cords = [(x, y) for (x, y, _party) in winners_attributes]
        histogram.accumulate(winners_cords)

    def draw_all_histograms(self):
        dir = 'distributions'

        for election in self.histograms.keys():
            histogram = self._get_histogram(election)

            filename = '{}-distribution.png'.format(election)
            path = os.path.join(dir, filename)

            histogram.save_image(path)

    def _get_histogram(self, election_id):
        # if it's first time election_id is met
        if election_id not in self.histograms.keys():
            self.histograms[election_id] = Histogram(-3, 3, -3, 3, (0, 0, 1), 20)
        return self.histograms[election_id]


histograms = DistributionHistograms()

process_win_dir('paper_generated', histograms)

histograms.draw_all_histograms()
