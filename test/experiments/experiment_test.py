import pytest

from expects import *
from os import walk

from pmp.experiments import Experiment, ExperimentConfig
from pmp.experiments.election_config import ElectionConfig
from pmp.rules import Bloc


@pytest.fixture
def experiment_config(approval_profile):
    config = ExperimentConfig()
    config.add_candidates(approval_profile.candidates)
    config.add_voters(approval_profile.preferences)
    return config


@pytest.fixture
def experiment(experiment_config):
    experiment = Experiment(experiment_config)
    return experiment


def generated_files(path):
    """Helper returning files generated by an experiment"""
    for _, dirs, files in walk(path):
        if len(dirs) > 0:
            return []
        return files


def test_run_experiment_set_election_precedence(experiment, tmpdir):
    experiment.set_generated_dir_path(tmpdir)
    experiment.set_election(Bloc, 2)
    experiment.set_result_filename('bloc')
    experiment.run(n=1, log_on=False, save_win=True, split_dirs=False)

    files = generated_files(tmpdir)
    expect(len(files)).to(equal(1))
    election_id = files[0].split('_')[0]
    expect(election_id).to(equal('bloc'))


def test_run_experiment_add_election_precedence(experiment, tmpdir):
    experiment.set_generated_dir_path(tmpdir)
    experiment.set_election(Bloc, 2)
    experiment.set_result_filename('bloc')
    experiment.add_election(Bloc, 1, 'other')
    experiment.run(n=1, log_on=False, save_win=True, split_dirs=False)

    files = generated_files(tmpdir)
    expect(len(files)).to(equal(1))
    election_id = files[0].split('_')[0]
    expect(election_id).to(equal('other'))


def test_run_experiment_elect_configs_precedence(experiment, tmpdir):
    experiment.set_generated_dir_path(tmpdir)
    experiment.set_election(Bloc, 2)
    experiment.set_result_filename('bloc')
    experiment.add_election(Bloc, 1, 'other')
    election_configs = [ElectionConfig(Bloc, 1, 'moreOther')]
    experiment.run(n=1, log_on=False, save_win=True, elect_configs=election_configs, split_dirs=False)

    files = generated_files(tmpdir)
    expect(len(files)).to(equal(1))
    election_id = files[0].split('_')[0]
    expect(election_id).to(equal('moreOther'))


def test_inout_files(experiment):
    expect(experiment._Experiment__generate_inout).to(be_false)
    experiment.set_inout_filename('inout_fname')
    expect(experiment._Experiment__generate_inout).to(be_true)