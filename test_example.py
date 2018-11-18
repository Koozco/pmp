try:
    from pmp.experiments import experiment_config
    from pmp.experiments import Experiment
    from pmp.experiments import generate_uniform, impartial
    from pmp.rules.bloc import Bloc
    from pmp.experiments import FileType
except (ImportError, NameError) as e:
    print("Cannot import pmp. Check whether pmp is installed.\n" + str(e))
    exit()

# Experiment as more generic class for running experiments described in config

config = experiment_config.ExperimentConfig()
config.set_candidates(generate_uniform(-3, -3, 3, 3, 100, 'None'))
# config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, 10, 'None'))

# add a single candidate
# config.add_candidates([(999.888, 111.222, 'None')])
# config.add_one_candidate((999.88, 11.22, 2.2), 'Be')

config.add_voters(generate_uniform(-3, -3, 3, 3, 10, 'None'))
# config.add_one_voter((1000, 11, 2))

# Impartial
# config.impartial(4, 10)
# config.add_candidates([0, 1, 2, 3])
# config.add_voters(lambda c: impartial(len(c), 10))

# config.impartial(10, 10)

experiment = Experiment(config)
experiment.set_election(Bloc, 3)
# experiment.set_filename("kb10")
experiment.set_generated_dir_path("gene")

experiment.run(n=2, save_win=True, save_in=True)


