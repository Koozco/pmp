from expects import *


def test_inout_files(experiment):
    expect(experiment._Experiment__generate_inout).to(be_false)
    experiment.set_inout_filename('inout_fname')
    expect(experiment._Experiment__generate_inout).to(be_true)
