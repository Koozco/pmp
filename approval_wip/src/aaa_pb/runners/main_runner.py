import argparse
import random
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

from aaa_pb.runners.sample_input_cli_args import SampleInputCliArgs
from aaa_pb.test_utils.record_elections_data_for_tests import RecordElectionsDataForTests
from aaa_pb.utils.timed import timed
from aaa_pb.runners.cmd_line_experiment_parameters import CmdLineExperimentParameters
from aaa_pb.experiment.experiment_start import ExperimentStart


class MainRunner:

    @classmethod
    def run_with_hardcoded_args(cls, data_time_str: str, data_for_tests_dst_dir: Optional[Path] = None) -> None:
        sample_cli_args = SampleInputCliArgs(time_name=data_time_str)

        RecordElectionsDataForTests.TEST_UTIL_HOOK.base_output_dir = data_for_tests_dst_dir

        all_args = sample_cli_args.args_2019_01()
        print("\n".join(all_args))
        cls.run(argv=all_args)


    @classmethod
    @timed
    def run(cls, argv: List[str]) -> None:
        random.seed(1)
        # numpy.random.seed(1)

        #    import rules.approval._base
        #
        #    for r in rules.approval._base.ApprovalBasedRules.getList():
        #        print '"' + str(r).split('.')[-1] + '",'
        #
        #    exit(1)
        namespace = cls.get_cli_argument_parser().parse_args(argv)
        params = CmdLineExperimentParameters(namespace=namespace)
        ExperimentStart().main_runner(params=params)

    @classmethod
    def get_cli_argument_parser(cls) -> ArgumentParser:
        parser = argparse.ArgumentParser(description='Runs series of experiments')
        parser.add_argument('--rules',
                            required=True,
                            type=str,
                            metavar="RULE",
                            nargs='+',
                            help='Voting rule names')
        parser.add_argument('--distributions',
                            required=False,
                            type=str,
                            metavar="NAME",
                            nargs='+',
                            help='Distribution schemes names')
        parser.add_argument('--ballot-calc-params',
                            required=True,
                            type=str,
                            metavar=("NAME", "ARG1", "ARG2"),
                            nargs=3,
                            help='Parameters to instantiate ballot calc',
                            action='append'
                            )
        parser.add_argument('--committee-size',
                            required=True,
                            type=int,
                            metavar='SIZE',
                            help='Committee size')
        parser.add_argument('--output-dir-name',
                            required=True,
                            type=str,
                            metavar='NAME',
                            help='Output dir name')
        parser.add_argument('--base-working-dir-name',
                            required=True,
                            type=str,
                            metavar='NAME',
                            help='Base dir for all output')
        parser.add_argument('--number-of-elections',
                            required=False,
                            type=int,
                            metavar='NAME',
                            help='Number of elections')
        parser.add_argument('--number-voters-and-candidates',
                            required=False,
                            type=int,
                            metavar='NUM',
                            help='Number candidates and number of voters (they are equal)')
        parser.add_argument('--datapoints-dir-path-src',
                            required=False,
                            type=str,
                            metavar='PATH',
                            help='File path pointing to dir with file holding datapoints for 2D elections that we read from')
        parser.add_argument('--datapoints-dir-path-dst',
                            required=False,
                            type=str,
                            metavar='PATH',
                            help='File path pointing to dir with file holding datapoints for 2D elections that we write to')

        parser.add_argument('--load-election-instances-path',
                            required=False,
                            type=str,
                            metavar='PATH',
                            help='File path pointing to source dir with file holding election instances')

        parser.add_argument('--persist-election-instances-path',
                            required=False,
                            type=str,
                            metavar='PATH',
                            help='File path pointing to destination dir for files holding election instances')
        return parser
