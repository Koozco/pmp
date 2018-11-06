import experiment_config
from rules.borda import Borda
from rules.bloc import Bloc
from helpers import generateUniform

# Experiment as more generic class for running experiments described in config

config = experiment_config.ExperimentConfig()
# config.set_candidates(generateUniform(-3, -3, 3, 3, 100, 'None'))
config.add_candidates(lambda: generateUniform(-3, -3, 3, 3, 100, 'None'))
# add a single candidate
# config.add_candidates([(999.888, 111.222, 'None')])
# config.add_one_candidate((999.88, 11.22, 2.2), 'Be')

config.add_voters(generateUniform(-3, -3, 3, 3, 100, 'None'))
# config.add_one_voter((1000, 11, 2))

# config.impartial(10, 10)

config.run_election(Bloc, 1, "kb10")
config.set_generated_dir_path("gen")

config.run()


