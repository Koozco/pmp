from typing import List

from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.model.elections_experiment_parameters import ElectionsExperimentParameters
from aaa_pb.model.election_result import ElectionResult
from aaa_pb.legacy_adapters.new_experiment import NewExperiment


class ElectionsExperiment:

    def __init__(self, election_instances: ElectionInstancesContainer, elections_experiment_parameters: ElectionsExperimentParameters) -> None:
        self.election_instances = election_instances.election_instances  # TODO
        self.elections_experiment_parameters = elections_experiment_parameters

        self.election_results = None

        pass

    def getElectionResults(self) -> List[ElectionResult]:
        if self.election_results is None:
            raise Exception("Elections results not available - experiment hasn't been run!")

        return self.election_results

    def runExperiment(self) -> None:

        election_instances = self.election_instances
        rule_class = self.elections_experiment_parameters.rule_class
        committee_size = self.elections_experiment_parameters.committee_size

        election_results = []
        for election_instance in election_instances:
            election_result = NewExperiment.computeElectionResult(
                election_instance=election_instance,
                rule_class=rule_class,
                committee_size=committee_size)
            election_results.append(election_result)

        self.election_results = election_results

        pass

    pass
