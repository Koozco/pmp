Experiment Tutorial
===================

This tutorial shows how to use main utility of pmp called experiment
and should help you get familiar with :class:`.Experiment` class.

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
        experiment.set_generated_dir_path('paper')

        for rule in rules:
            election_name = "{}-{}".format(config.id, rule.__name__)
            experiment.add_election(rule, k, election_name)

        experiment.run(n=experiments_num, save_win=True, log_on=False)

Processing experiment output
----------------------------

[TBD]