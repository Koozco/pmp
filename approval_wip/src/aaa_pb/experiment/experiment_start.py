from pathlib import Path

import aaa_pb.model.elections_experiment
import aaa_pb.model.elections_experiment_parameters
import aaa_pb.model.euclidean_distribution_descriptor_container
import aaa_pb.model.euclidean_election_datapoints_generator
import aaa_pb.output_file_paths_getter
from aaa_pb.model import ballot_2d2, election_instance_container
from aaa_pb.persistence.election_experiment_results_file_writer import ElectionExperimentResultsFileWriter
from aaa_pb.persistence.json_converters.list_of_election_containers_json_converter import \
    ListOfElectionsContainers_JsonConverter
from aaa_pb.persistence.list_of_elections_containers_persistence import ListOfElectionsContainers_Persistence
from aaa_pb.utils import timed
from aaa_pb.runners.cmd_line_experiment_parameters import CmdLineExperimentParameters
from aaa_pb.registry.approval_rules_enum import ApprovalRulesEnum


class ExperimentStart:

    def main_runner(self, params: CmdLineExperimentParameters) -> None:
        base_dir = Path(params.base_working_dir_name)
        base_work_dir_path = base_dir / params.output_dir_name
        base_work_dir_path.mkdir(parents=True, exist_ok=False)

        number_of_datapoint_distributions = params.number_of_elections

        rules_classes = ApprovalRulesEnum.getByNames(params.rules)
        committee_size = params.committee_size

        # there is one container per each unique (distribution, ballot_calc)
        if params.load_election_instances_path:
            election_instances_containers = ListOfElectionsContainers_JsonConverter \
                .from_json_dict(src_dir=params.load_election_instances_path)
        else:
            election_instances_containers = \
                self.generate_election_instances(
                    number_of_datapoint_distributions=number_of_datapoint_distributions,
                    params=params
                )

        if params.persist_election_instances_path:
            params.persist_election_instances_path.mkdir(parents=True)
            ListOfElectionsContainers_Persistence.persist(
                path=params.persist_election_instances_path / "list_of_election_containers.json",
                elections_containers=election_instances_containers
            )

        for election_instances_container in election_instances_containers:
            self.runExperimentForGivenDatapointsDistribution(base_work_dir_path,
                                                             election_instances_container,
                                                             rules_classes=rules_classes,
                                                             committee_size=committee_size)

    def generate_election_instances(self, number_of_datapoint_distributions, params):
        if params.datapoints_dir_path_src is not None and params.datapoints_dir_path_dst is not None:
            raise Exception
        # Generate  data points
        if params.distributions is not None and params.number_voters_and_candidates is not None:
            if params.datapoints_dir_path_src is not None:
                raise Exception

            distribution_descriptors_container = \
                aaa_pb.model.euclidean_distribution_descriptor_container.EuclideanDistributionDescriptorContainer \
                    .getByNames(
                    names=params.distributions,
                    number_of_datapoint_distributions=number_of_datapoint_distributions,
                    number_of_voters_and_candidates=params.number_voters_and_candidates
                )
        elif params.datapoints_dir_path_src is not None:
            if params.distributions is not None or params.number_voters_and_candidates is not None:
                raise Exception

            distribution_descriptors_container = aaa_pb.model.euclidean_distribution_descriptor_container.EuclideanDistributionDescriptorContainer.fromDir(
                input_dir_path=params.datapoints_dir_path_src
            )
        else:
            raise Exception

        def make_list_of_datapoints(distribution_descriptors_container):
            # type: (new_experiment.EuclideanDistributionDescriptorContainer) -> list((new_experiment.EuclideanDistributionDescriptor, list[new_experiment.EuclideanElectionDatapoints]))
            ret = []
            for distribution_descriptor in distribution_descriptors_container.getDescriptorList():
                datapoints = aaa_pb.model.euclidean_election_datapoints_generator.EuclideanElectionDatapointsGenerator.fromDistributionDescriptor(
                    distribution_descriptor=distribution_descriptor)
                ret.append((distribution_descriptor, datapoints))

            return ret

        list_of_descriptors_and_list_of_datapoints = make_list_of_datapoints(
            distribution_descriptors_container=distribution_descriptors_container)
        if params.datapoints_dir_path_dst is not None:
            aaa_pb.model.euclidean_distribution_descriptor_container.EuclideanDistributionDescriptorContainer.toDir(
                output_dir_path=params.datapoints_dir_path_dst,
                list_of_descriptors_and_list_of_datapoints=list_of_descriptors_and_list_of_datapoints
            )
        # Generate elections
        # TODO run experiment with different ballot calcs
        ballot_calcs = self.buildBallotCalcs(params)
        # max_number_of_candidates = len(list_of_descriptors_and_list_of_datapoints[0][1][0].C)
        # u1 = ballot_2d2.ApprovalBallotCalc_NearestUniform(min=1, max=max_number_of_candidates)
        # u1 = ballot_2d2.ApprovalBallotCalc_NearestUniform(min=committee_size, max=committee_size)
        # ddd = u1.to_dict()
        # u2 = ballot_2d2.ApprovalBallotCalc_NearestUniform.from_dict(ddd)
        # ballot_calcs = [
        #     ballot_2d2.ApprovalBallotCalc.nearest_gauss(mean=20, sigma=5),
        #     ballot_2d2.ApprovalBallotCalc.in_radius_uniform(min=0.5, max=1.5),
        #     ballot_2d2.ApprovalBallotCalc.in_radius_gauss(mean=1, sigma=0.5)
        # ]

        election_instances_containers = self._generateElectionInstanceContainers(
            list_of_descriptors_and_list_of_datapoints=list_of_descriptors_and_list_of_datapoints,
            ballot_calcs=ballot_calcs
        )
        return election_instances_containers

    def buildBallotCalcs(self, params):
        ballot_calcs_params = params.ballot_calcs_params
        ballot_calcs = []
        for ballot_calcs_params in ballot_calcs_params:
            bc = ballot_2d2.ApprovalBallotCalc.fromString(
                name=ballot_calcs_params[0],
                params=ballot_calcs_params[1:])
            ballot_calcs.append(bc)
        return ballot_calcs

    def _generateElectionInstanceContainers(self, ballot_calcs, list_of_descriptors_and_list_of_datapoints):
        ret = []
        for (distribution_descriptor, list_of_datapoints) in list_of_descriptors_and_list_of_datapoints:
            # generate election instances from 2d points according to given distribution and ballot calculator
            election_instances_containers = election_instance_container.ElectionInstancesContainer.fromDistribution(
                distribution_descriptor=distribution_descriptor,
                ballot_calcs=ballot_calcs,
                list_of_datapoints=list_of_datapoints
            )

            for election_instances_container in election_instances_containers:
                ret.append(election_instances_container)
        return ret

    def runExperimentForGivenDatapointsDistribution(self,
                                                    base_work_dir_path,
                                                    election_instances_container,
                                                    rules_classes,
                                                    committee_size):
        # type: (pathlib.Path, new_experiment.ElectionInstancesContainer, list, int) -> None
        elections_experiment_parameters_list = []

        for rule_class in rules_classes:
            elections_experiment_parameters_list.append(
                aaa_pb.model.elections_experiment_parameters.ElectionsExperimentParameters(
                rule_class=rule_class,
                committee_size=committee_size
            ))

        for elections_experiment_parameters in elections_experiment_parameters_list:
            output_file_paths_getter = aaa_pb.output_file_paths_getter.OutputFilePathsGetter(

                base_work_dir_path=base_work_dir_path,
                election_experiment_parameters=elections_experiment_parameters,
                distribution_label=election_instances_container.distribution_descriptor.label,
                ballot_calc_label=election_instances_container.ballot_calc.getShortName()
            )

            #        for election_instance in election_instances_container.election_instances:
            #            avg_number_of_approved_candidates = sum([len(p) for p in election_instance.P])/len(election_instance.P)
            #            print avg_number_of_approved_candidates
            #
            #        exit(1)

            # setup experiment and run
            elections_experiment = aaa_pb.model.elections_experiment.ElectionsExperiment(
                election_instances=election_instances_container,
                elections_experiment_parameters=elections_experiment_parameters
            )
            # TODO return ElectionsExperimentResultsContainer

            print("Running experiment for {0}".format(elections_experiment_parameters.mkString()))

            @timed.timed
            def timedRunExperiment():
                elections_experiment.runExperiment()
                pass

            timedRunExperiment()

            election_experiment_results_file_writer = ElectionExperimentResultsFileWriter(
                elections_experiment=elections_experiment,
                output_file_path_getter=output_file_paths_getter
            )
            election_experiment_results_file_writer \
                .writeHistogram_Image() \
                .writeHistogram_Text() \
                .writeResults_Images() \
                .writeResults_Text()

        pass
