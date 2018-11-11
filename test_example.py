import experiment_config
from experiment import Experiment, impartial
from rules.borda import Borda
from rules.bloc import Bloc
from helpers import generate_uniform

# Experiment as more generic class for running experiments described in config

config = experiment_config.ExperimentConfig()
# config.set_candidates(generate_uniform(-3, -3, 3, 3, 100, 'None'))
config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, 10, 'None'))

# add a single candidate
# config.add_candidates([(999.888, 111.222, 'None')])
# config.add_one_candidate((999.88, 11.22, 2.2), 'Be')

config.add_voters(generate_uniform(-3, -3, 3, 3, 10, 'None'))
# config.add_one_voter((1000, 11, 2))

# Impartial
# config.add_candidates([0, 1])
# config.add_voters(lambda c: impartial(len(c), 10))

# config.impartial(10, 10)

experiment = Experiment(config)
experiment.set_election(Bloc, 1)
experiment.set_filename("kb10")
experiment.set_generated_dir_path("gene")

experiment.run(visualization=True)


