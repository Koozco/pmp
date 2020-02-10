from pmp.experiments import ExperimentConfig, generate_uniform, Experiment, generate_gauss
from pmp.rules import Bloc, Borda

experiments_num = 100
n = 200
m = 200
k = 20

uniform_config = ExperimentConfig('uniform')
uniform_config.add_candidates(lambda: generate_uniform(-3, -3, 3, 3, m, 'None'))
uniform_config.add_voters(lambda: generate_uniform(-3, -3, 3, 3, n, 'None'))

gaussian_config = ExperimentConfig('gaussian')
gaussian_config.add_candidates(lambda: generate_gauss(0.0, 0.0, 1.0, m, 'None'))
gaussian_config.add_voters(lambda: generate_gauss(0.0, 0.0, 1.0, n, 'None'))

configs = [uniform_config, gaussian_config]

rules = [Bloc, Borda]

for config in configs:
    experiment = Experiment(config)
    experiment.set_generated_dir_path('paper_generated')

    for rule in rules:
        election_name = "{}-{}".format(config.id, rule.__name__)
        experiment.add_election(rule, k, election_name)

    experiment.run(n=experiments_num, save_win=True, log_on=False)
