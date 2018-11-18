try:
    from pmp.experiments import experiment_config
    from pmp.experiments import Experiment
    from pmp.experiments import generate_uniform, impartial
    from pmp.rules.bloc import Bloc
    from pmp.rules.borda import Borda
    from pmp.experiments import FileType
except (ImportError, NameError) as e:
    print("Cannot import pmp. Check whether pmp is installed.\n" + str(e))
    exit()

# Generating voters and candidates using functions and lambdas
config = experiment_config.ExperimentConfig()
config.set_candidates(generate_uniform(-3, -3, 3, 3, 100, 'None'))
config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, 10, 'None'))
config.add_voters(generate_uniform(-3, -3, 3, 3, 10, 'None'))

experiment = Experiment(config)
experiment.set_election(Bloc, 3)
experiment.set_filename("bloc3")
experiment.set_generated_dir_path("bloc_example")
experiment.run(visualization=True, n=2, save_win=True)

# Adding one voter and one candidate
config = experiment_config.ExperimentConfig()
config.add_one_candidate((999.88, 11.22, 2.2), 'Be')
config.add_one_voter((1000, 11, 2))

experiment = Experiment(config)
experiment.set_election(Borda, 1)
experiment.run(n=5, save_out=True)

# Impartial
config = experiment_config.ExperimentConfig()
config.impartial(4, 10)
config.add_voters(lambda c: impartial(len(c), 10))

experiment = Experiment(config)
experiment.set_election(Borda, 2)
experiment.set_filename("impartial")
experiment.run(n=3, save_in=True)

