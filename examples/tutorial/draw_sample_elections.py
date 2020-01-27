import os

from pmp.experiments import process_win_dir
from pmp.experiments import Histogram


# note: redundant parameters voters and preferences has to included
def illustrate_sample_election(candidates, winners, election, voters, preferences):
    # strategy has to pass all not 2nd elections
    election_n = election.split('_')[1]
    if int(election_n) != 2:
        return

    # create histogram object with scale parameters as in paper
    histogram = Histogram(-3, 3, -3, 3, (0.33, 0.33, 0.33), 20)

    # candidates, just like voters are given as tuples of coordinates and string property, party
    candidates_cords = [(x, y) for (x, y, _party) in candidates]
    histogram.accumulate(candidates_cords)

    winners_attributes = [candidates[i] for i in winners]
    # transform winners coordinates from (-3, 3) to (0, 120)
    winners_cords = [((x + 3) * 20, (y + 3) * 20) for (x, y, _party) in winners_attributes]

    histogram.draw_fixed_points(winners_cords, (0, 0, 255), 1)

    dir = 'sample_elections'
    filename = '{}-sample.png'.format(election)
    path = os.path.join(dir, filename)

    histogram.save_image(path)


process_win_dir('paper_generated', illustrate_sample_election)
