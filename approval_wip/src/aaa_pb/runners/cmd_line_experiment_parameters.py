import argparse
from pathlib import Path


class CmdLineExperimentParameters():

    def __init__(self, namespace: argparse.Namespace) -> None:
        self.persist_election_instances_path = Path(namespace.persist_election_instances_path) if namespace.persist_election_instances_path is not None else None

        self.load_election_instances_path = Path(namespace.load_election_instances_path) if namespace.load_election_instances_path is not None else None

        self.distributions = namespace.distributions
        self.ballot_calcs_params = namespace.ballot_calc_params
        self.committee_size = namespace.committee_size
        self.rules = namespace.rules
        self.output_dir_name = namespace.output_dir_name
        self.base_working_dir_name = namespace.base_working_dir_name
        self.number_of_elections = namespace.number_of_elections
        self.number_voters_and_candidates = namespace.number_voters_and_candidates
        self.datapoints_dir_path_src = Path(namespace.datapoints_dir_path_src) if namespace.datapoints_dir_path_src is not None else None
        self.datapoints_dir_path_dst = Path(namespace.datapoints_dir_path_dst) if namespace.datapoints_dir_path_dst is not None else None
