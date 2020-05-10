from typing import List

from aaa_pb.directory_structure import DirectoryStructure


class SampleInputCliArgs:

    def __init__(self, time_name: str) -> None:
        self.time_name = time_name

    def my_args(self) -> List[str]:
        time_name = self.time_name
        argv = [
            # "--rules", "PhragmenMax_Seq",
            "--rules",
            # "PhragmenMax_ILP",
            # "PhragmenVar_ILP",
            # "Monroe_ILP",
            # "PAV_ILP",
            # "CC_ILP",
            # "PAV_SinglePeaked_ILP",
            # "PAV_ILP_ordinal",
            # "CC_Banzhaf",
            # "CC_ReverseGreedy_Slow",
            # "CC_ReverseGreedy",
            # "CC_Greedy",
            # "CC_Annealing",
            # "PAV_Annealing",
            "PAV_ReverseGreedy",
            "PAV_Greedy",
            # "PAV_Genetic",
            # "PhragmenMax_Seq",
            # "PhragmenVar_Seq",

            # "--rules", "PhragmenMax_ILP",
            # "PhragmenMax_ILP_2", # "PAV_Annealing", # "PhragmenMax_ILP", # "CC_ILP", "PAV_ILP", # "PhragmenMax_ILP"
            "--committee-size", "10",
            "--output-dir-name", "new_exp_2_" + time_name + "_py_PAV_ReverseGreedy",
            "--base-working-dir-name", str(DirectoryStructure.LOCAL_EXPERIMENT_OUTPUT_DIR / "experiments"),

            # single gauss distribution, 12 voters and candidates

            # "--datapoints-dir-path-src",
            # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_20181015-195053_py_phragmen",

            "--number-of-elections", "1000",
            "--distributions", "unidisc",  # "gauss1",  # , "unisqua", "gauss4",
            "--number-voters-and-candidates", "100",
            # "--datapoints-dir-path-dst", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_cv100_k10_x10__" + time_name,
            # "--datapoints-dir-path-dst", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/ordinal_cv4__" + time_name,

            "--ballot-calc-params", "ApprovalBallotCalc_NearestUniform", "10.0", "10.0",
            # "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "1.05", "1.05"
        ]
        for arg in argv:
            print(arg)

        return argv


    def my_args_bigMaxPhragmen(self) -> List[str]:
        time_name = self.time_name
        argv = [
            "--rules", "PhragmenMax_ILP",

            "--committee-size", "10",
            "--output-dir-name", "new_exp_2_" + time_name + "_py_bigMaxPhragmen",
            "--base-working-dir-name", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-experiments",

            # "--datapoints-dir-path-src",
            # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_py_bigMaxPhragmen",

            "--number-of-elections", "1000",
            "--distributions", "unidisc",  # "gauss1",  # , "unisqua", "gauss4",
            "--number-voters-and-candidates", "100",

            # "--datapoints-dir-path-dst",
            # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_py_bigMaxPhragmen",

            # "--ballot-calc-params", "ApprovalBallotCalc_NearestUniform", "1", "10"
            "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "1.05", "1.05"
        ]
        return argv


    def args_2019_01(self) -> List[str]:
        time_name_str = self.time_name
        exact_rules = [
            "AV",
            "CC_ILP",
            "PAV_ILP"
        ]
        # TODO (1, 0, .., 0) -> (1, 1, .., 0)-OWA (~ t-approval) rules

        # TODO: important: genetic algorithm
        # TODO: maybe: Banzhaf (Piotr has some derivation on Banzhaf for some rules)
        heuristic_based_rules = [
            # "CC_Annealing",
            # "CC_Greedy",
            # "CC_ReverseGreedy",
            # "PAV_Annealing",
            # "PAV_ReverseGreedy",
            # "PAV_Greedy"
        ]

        # TODO Impartial Culture (different approval probabilities)
        distribution_params = ["--distributions", "unidisc", "unisqua"]

        all_rules_params = ["--rules"] + exact_rules + heuristic_based_rules

        election_params = [
            "--committee-size", "3",
            "--number-voters-and-candidates", "8",
            "--number-of-elections", "10",  # goal: run x1000, x5000
        ]

        ballot_calc_params = [
            "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "0.0", "3.0",
            # TODO should take about k candidates, smallest around k/2, biggest about 2k
            "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "0.5", "2.5",
            "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "1.5", "1.5",
        ]

        return all_rules_params + \
               distribution_params + \
               election_params + \
               ballot_calc_params + \
               [
                   "--output-dir-name", "exp_2020_04_" + time_name_str + "",
                   "--base-working-dir-name", str(DirectoryStructure.LOCAL_EXPERIMENT_OUTPUT_DIR / "experiments"),
               ] + [
                   #     "--load-election-instances-path", str(LOCAL_OUTPUT_DIR / "saved-elections" / "1"),
                   "--persist-election-instances-path", str(DirectoryStructure.LOCAL_EXPERIMENT_OUTPUT_DIR / "saved-elections" / time_name_str)
               ]
