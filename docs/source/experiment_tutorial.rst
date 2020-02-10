Experiment Tutorial
===================

This tutorial shows how to use main utility of pmp called experiment
and should help you get familiar with :class:`.Experiment` class.

**Tutorial goal: Compute election results for some set of scoring rules and visually compare their characteristics.
Aggregate results of large number of elections on 2-dimensional histogram. Repeat this task for different points distributions.**


Running experiment
------------------

We will try to lead you through your first experiment run with pmp based on use case of paper
`What do multiwinner voting rules do? An experiment over the two-dimensional euclidean domain.
[E. Elkind, P. Faliszewski, J.-F. Laslier, P. Skowron, A. Slinko, and N. Talmon.] <https://arxiv.org/abs/1901.09217>`_

We will focus on running elections in order to generate histograms like on 8th page of the paper.
Please get familiar with mentioned plots.

Let's recreate setup of the experiment. Our setup will be reduced version of the one presented in paper.
::

    # 10k is a lot, let's start with 100, so we can save some time
    experiments_num = 100
    n = 200
    m = 200
    k = 20

Provide experiment configs. (see :class:`.ExperimentConfig`)
One configuration corresponds to a column in the final plot.
::

    from pmp.experiments import ExperimentConfig, generate_uniform, generate_gauss

    uniform_config = ExperimentConfig('uniform')
    uniform_config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, m, 'None'))
    uniform_config.add_voters(lambda: generate_uniform(-3, -3, 3, 3, n, 'None'))

    gaussian_config = ExperimentConfig('gaussian')
    gaussian_config.add_candidates(lambda: generate_gauss(0.0, 0.0, 1.0, m, 'None'))
    gaussian_config.add_voters(lambda: generate_gauss(0.0, 0.0, 1.0, n, 'None'))

    configs = [uniform_config, gaussian_config]


Choose scoring rules. One rule corresponds to a row in the final plot.
::

    from pmp.rules import SNTV, Borda

    rules = [SNTV, Borda]

Last step is to run the experiment itself. Please notice how looks structure of generated directory.
::

    for config in configs:
        experiment = Experiment(config)
        experiment.set_generated_dir_path('paper_generated')

        for rule in rules:
            election_name = "{}-{}".format(config.id, rule.__name__)
            experiment.add_election(rule, k, election_name)

        experiment.run(n=experiments_num, save_win=True, log_on=False)

Since we've run our experiment and store all necessary information in *.win* files, we can proceed to next part - processing results.

Processing experiment results
-----------------------------

With all necessary files generated we can move forward. For this purpose we will use helper
:func:`process_win_dir <pmp.experiments.helpers.process_win_dir>`. It accepts argument ``strategy``, which allows you to
do anything-your-use-case require to do with computed results.
It should look like:
::

    def illustrate_sample_election(candidates, winners, election, voters, preferences):
        pass

    process_win_dir('paper_generated', illustrate_sample_election)

1. Function Strategy
^^^^^^^^^^^^^^^^^^^^

At first, let's aim to prepare sample election diagrams for each combination of ``distribution x rule``.
The simplest case for Callable `strategy` is to provide a function.
Since it has to be a sample election, let's decide on which of `.win` files choose. For example, let it be 2nd election for each
combination.
::

    import os # we will use this later
    from pmp.experiments import Histogram

    # note: redundant parameters voters and preferences has to included
    def illustrate_sample_election(candidates, winners, election, voters, preferences):
        # strategy has to pass all not 2nd elections
        election_n = election.split('_')[1]
        if int(election_n) != 2:
            return

We will use :class:`.Histogram`, although it is not exactly it's destination.
::

        # create histogram object with scale parameters as in paper
        histogram = Histogram(-3, 3, -3, 3, (0.33, 0.33, 0.33), 20)

Candidates are represented as list of their attributes. Accumulate them, just in case of high density, although drawing them
as simple points should be enough.
::

        # candidates, just like voters are given as tuples of coordinates and string property, party
        candidates_cords = [(x, y) for (x, y, _party) in candidates]
        histogram.accumulate(candidates_cords)

Winners contains list of candidate ids. Retrieve their coordinates and transform them to histogram bucket resolution.
::

        winners_attributes = [candidates[i] for i in winners]
        # transform winners coordinates from (-3, 3) to (0, 120)
        winners_cords = [((x+3)*20, (y+3)*20) for (x, y, _party) in winners_attributes]

        histogram.draw_fixed_points(winners_cords, (0, 0, 255), 1)

Create file in some pre-created directory.
::

        dir = 'sample_elections'
        filename = '{}-sample.png'.format(election)
        path = os.path.join(dir, filename)

        histogram.save_image(path)

Final implementation:
::

    import os # we will use this later
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
        winners_cords = [((x+3)*20, (y+3)*20) for (x, y, _party) in winners_attributes]

        histogram.draw_fixed_points(winners_cords, (0, 0, 255), 1)

        dir = 'sample_elections'
        filename = '{}-sample.png'.format(election)
        path = os.path.join(dir, filename)

        histogram.save_image(path)

    process_win_dir('paper_generated', illustrate_sample_election)


2. Callable Object Strategy
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Second goal is to generate the histograms themselves. We can not use as simple function as above. All files referring
one experiment and election configuration need to be aggregated to one histogram.
Naive solution is to create object collecting :class:`.Histogram` object per each configuration (in simplest case, e.g. dict)
and inject it's reference in function we provide as a strategy (for example, using higher-order function or decorator) and in the
strategy function itself conditionally access right histogram depending on election id.

To achieve this goal and keep code clean we will conclude above logic in a class.
::

    class DistributionHistograms:
        def __call__(self, candidates, winners, election, voters, preferences):
            pass

    process_win_dir('paper_generated', illustrate_sample_election)

Let's sum up all logic required to handle single `.win` file:

* identify histogram where to add points

* retrieve winners coordinates

* accumulate points


After finish of processing:

* draw all histograms

Without breaking down into details, below class satisfy all above requirements while keeping histograms in instances state.
::

    import os
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

And everything that should be called presents:
::

    from pmp.experiments import process_win_dir


    histograms = DistributionHistograms()

    process_win_dir('paper', histograms)

    histograms.draw_all_histograms()


**Last step is to use `pmp` worthily with your use case :)**
