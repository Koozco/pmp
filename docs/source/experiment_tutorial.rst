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

    unifrom_config = ExperimentConfig('uniform')
    unifrom_config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, m, 'None'))
    unifrom_config.add_voters(lambda: generate_uniform(-3, -3, 3, 3, n, 'None'))

    gaussian_config = ExperimentConfig('gaussian')
    gaussian_config.add_candidates(lambda: generate_gauss(0.0, 0.0, 1.0, m, 'None'))
    gaussian_config.add_voters(lambda: generate_gauss(0.0, 0.0, 1.0, n, 'None'))

    configs = [unifrom_config, gaussian_config]


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

At first, let's aim to prepare sample election diagrams for each combination of ``distribution x rule``.
We will use :class:`.Histogram`. The simplest case for Callable `strategy` is to provide a function.
Since it has to be a sample, let's decide on which of `.win` files choose. For example, let it be 42th election for each
combination.
::

    import os

    # note: redundant parameters voters and preferences has to included
    def illustrate_sample_election(candidates, winners, election, voters, preferences):
        # strategy has to pass all not 42th elections
        election_id = election.split('_')[1]
        if int(election_id) != 42:
            return

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
