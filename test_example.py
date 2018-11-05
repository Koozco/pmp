import experiment_config
from experiment import Experiment
from rules.borda import Borda
from helpers import generateUniform

# Experiment as more generic class for running experiments described in config

# Q: what to do with saving data? Do we need it?
# Q: Replace compute_winners with run_election?


config = experiment_config.ExperimentConfig()
# config.set_candidates(generateUniform(-3, -3, 3, 3, 100, 'None'))
config.add_candidates(lambda: generateUniform(-3, -3, 3, 3, 100, 'None'))
# add a single candidate
# config.add_candidates([(999.888, 111.222, 'None')])
# config.add_candidate((999.88, 11.22, 2.2), 'Be')
config.add_voters(generateUniform(-3, -3, 3, 3, 100, 'None'))
config.compute_winners(Borda, 10, "kb10")

config.run()



