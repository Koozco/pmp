from pathlib import Path

from aaa_pb.model.elections_experiment_parameters import ElectionsExperimentParameters
from aaa_pb.utils.path_validator import PathValidator


class OutputFilePathsGetter:

    def __init__(self,
                 base_work_dir_path: Path,
                 election_experiment_parameters: ElectionsExperimentParameters,
                 distribution_label: str,
                 ballot_calc_label: str) -> None:
        print("11")
        PathValidator(base_work_dir_path, "Election experiment base work dir path") \
            .exists() \
            .is_dir()

        self.base_dir_path = base_work_dir_path
        self.election_experiment_parameters = election_experiment_parameters
        self.distribution_label = distribution_label
        self.ballot_calc_label = ballot_calc_label

        pass

    def pathForSingleElection_Text(self, election_index: int) -> Path:
        return self.__pathForSingleElection(election_index).with_suffix(".txt")

    def pathForSingleElection_Image(self, election_index: int) -> Path:
        return self.__pathForSingleElection(election_index).with_suffix(".png")

    def pathForHistogram_Text(self) -> Path:
        return self.__pathForHistogram(suffix="_hist.txt")

    def pathForHistogram_Image(self) -> Path:
        return self.__pathForHistogram(suffix="_hist.png")

    # PRIVATE

    def __pathForSingleElection(self, election_index: int) -> Path:

        rule_name = self.election_experiment_parameters.rule_class.getName()
        committee_size = self.election_experiment_parameters.committee_size

        election_result_bare_file_name = "{0}_k{1}_{2}".format(rule_name, committee_size, election_index)

        return self.__baseDirPathForSingleElections() / election_result_bare_file_name

    def __pathForHistogram(self, suffix: str) -> Path:
        dir_path = self.base_dir_path / "histogram"
        dir_path.mkdir(parents=False, exist_ok=True)

        return dir_path / (self.__makeElectionName() + suffix)

    def __baseDirPathForSingleElections(self) -> Path:
        dir_path = self.base_dir_path / self.__makeElectionName()
        dir_path.mkdir(parents=False, exist_ok=True)

        return dir_path

    def __makeElectionName(self) -> str:
        distribution_label = self.distribution_label
        ballot_calc_label = self.ballot_calc_label
        rule_name = self.election_experiment_parameters.rule_class.getName()
        committee_size = self.election_experiment_parameters.committee_size
        elections_results_dir_name = "elections_{0}_{1}_{2}_k{3}".format(distribution_label, rule_name,
                                                                         ballot_calc_label, committee_size)
        return elections_results_dir_name

    pass
