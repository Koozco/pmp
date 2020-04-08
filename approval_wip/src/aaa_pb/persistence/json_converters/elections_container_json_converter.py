from typing import Dict, Any

from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.persistence.json_converters.ballot_calc_file_writer import ApprovalBallotCalc_JsonConverter
from aaa_pb.persistence.json_converters.distribution_descriptor_json_converter import \
    DistributionDescriptor_JsonConverter
from aaa_pb.persistence.json_converters.election_instance_json_converter import ElectionInstance_JsonConverter


class ElectionsContainer_JsonConverter:

    @classmethod
    def to_json_dict(self, elections_container: ElectionInstancesContainer) -> Dict[str, Any]:
        distributions_description_data = DistributionDescriptor_JsonConverter.to_json_dict(
            descriptor=elections_container.distribution_descriptor)
        approval_ballot_calc_data = ApprovalBallotCalc_JsonConverter.persist(calc=elections_container.ballot_calc)

        election_instance_data_list = []
        for i, election in enumerate(elections_container.election_instances):
            election_instance_data = ElectionInstance_JsonConverter.to_json_dict(election=election)
            election_instance_data_list.append(election_instance_data)

        data = {
            "distributions_description_data": distributions_description_data,
            "approval_ballot_calc": approval_ballot_calc_data,
            "number_of_elections": len(elections_container.election_instances),
            "election_instance_data_list": election_instance_data_list
        }
        return data

    @classmethod
    def from_json_dict(self, data: Dict[str, Any]) -> ElectionInstancesContainer:

        distributions_description_data = data["distributions_description_data"]
        approval_ballot_calc_data = data["approval_ballot_calc"]
        election_instance_data_list = data["election_instance_data_list"]

        distribution_descriptor = DistributionDescriptor_JsonConverter.from_json_dict(
            data=distributions_description_data
        )
        ballot_calc = ApprovalBallotCalc_JsonConverter.load(
            data=approval_ballot_calc_data
        )

        elections_list = []

        for election_instance_data in election_instance_data_list:
            election = ElectionInstance_JsonConverter.from_json_dict(
                data=election_instance_data
            )
            elections_list.append(election)

        return ElectionInstancesContainer(
            election_instances=elections_list,
            ballot_calc=ballot_calc,
            distribution_descriptor=distribution_descriptor
        )
