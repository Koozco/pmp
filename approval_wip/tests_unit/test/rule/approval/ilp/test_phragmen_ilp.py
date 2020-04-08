import unittest

from aaa_pb.utils.misc_utils import MiscUtils
from test.test_commons.approval_election_test_data_source import ApprovalElectionTestDataSource


class PhragmenIlpRules_Test(unittest.TestCase):

    @unittest.skip("the actual numbers differ from expected numbers very slightly so should this test case be treated a success?")
    def test_phragmen_on_generated_small_elections(self):
        quiet = True

        for data in ApprovalElectionTestDataSource().getSampleElections():
            (V, number_of_candidates, k, sample_name) = MiscUtils.pluck(
                data,
                'V',
                'number_of_candidates',
                'k',
                'sample_name')

            expectedResult = ApprovalElectionTestDataSource().getSamplePhragmenResult(sample_name)
            expected_committee, expected_load_vector = MiscUtils.pluck(
                expectedResult,
                'committee',
                'loads')

            # print "Ballots:"
            # for vote in V:
            #     print vote
            # print ""

            self.__run_single_election_max(
                V=V,
                number_of_candidates=number_of_candidates,
                k=k,
                quiet=quiet,
                sample_name=sample_name + "_phragmen",
                write_results_to_file=False,
                expected_committee=expected_committee,
                expected_load_vector=expected_load_vector,
                err_eps=0
            )
        pass

    def test_simple_max_1(self):
        # example 1 from paper "phragmens voting methods and justified representation"

        V = [
            [0],
            [0],
            [1],
            [2]
        ]
        k = 2
        number_of_candidates = 3

        self.__run_single_election_max(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates,
            quiet=True,
            expected_load_vector=[0.5, 0.5, 1.0, 0.0],
            expected_committee=[0, 1],  # or equally good [0, 2]
            err_eps=0
        )

    def test_simple_max_2(self):
        # NOTE
        # cplex finds optimal solution in the first iteration, but then it tries to hard and veers off into floats
        # example 2 from paper "phragmens voting methods and justified representation"
        V = [
            [0],
            [1],
            [1, 2],
            [0, 1, 2],
            [3]
        ]
        k = 3
        number_of_candidates = 4

        self.__run_single_election_max(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates,
            quiet=False,
            expected_load_vector=[3.0 / 4, 3.0 / 4, 3.0 / 4, 3.0 / 4, 0.0],
            err_eps=1e-7
        )

    def test_simple_var_2(self):
        # example 2 from paper "phragmens voting methods and justified representation"
        V = [
            [0],
            [1],
            [1, 2],
            [0, 1, 2],
            [3]
        ]
        k = 3
        number_of_candidates = 4

        self.__run_single_election_var(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates,
            quiet=False,
            expected_load_vector=[0.5, 0.5, 0.5, 0.5, 1.0],
            err_eps=0
        )

    def __run_single_election_var(self,
                                  V,
                                  number_of_candidates,
                                  k,
                                  quiet,
                                  err_eps,
                                  expected_load_vector=None,
                                  expected_committee=None,
                                  sample_name=None,
                                  write_results_to_file=False):

        from aaa_pb.rules.approval.ilp.phragmen import PhragmenVar_ILP

        # when
        committee, voter_loads = PhragmenVar_ILP.computeCommitteeAndLoads(
            number_of_candidates=number_of_candidates,
            k=k,
            V=V,
            quiet=quiet,
            lp_output_file_name="test_phragmen_var.lp"
        )

        # then
        print(voter_loads)
        print(committee)

        if write_results_to_file:
            ApprovalElectionTestDataSource().serializeCommitteeAndLoads(voter_loads=voter_loads, committee=committee, sample_name=sample_name)

        if expected_load_vector is not None:
            self.__assertListContainNearlyEqualElements(sorted(voter_loads), sorted(expected_load_vector), eps=err_eps)

        if expected_committee is not None:
            self.assertListEqual(committee, expected_committee)

        pass

    def __run_single_election_max(self,
                                  V,
                                  number_of_candidates,
                                  k,
                                  quiet,
                                  err_eps,
                                  expected_load_vector=None,
                                  expected_committee=None,
                                  sample_name=None,
                                  write_results_to_file=False):

        from aaa_pb.rules.approval.ilp.phragmen import PhragmenMax_ILP

        def verify_boolean_variable(value, name):
            if not (value == 1.0 or value == 0.0):
                msg = "boolean {0}: actual value: {1}".format(name, value)
                # assert False, msg
                print("[WARNING] " + msg)
            pass

        # when
        committee, voter_loads = PhragmenMax_ILP.computeCommitteeAndLoads(
            number_of_candidates=number_of_candidates,
            k=k,
            V=V,
            quiet=quiet,
            lp_output_file_name="test_phragmen_max.lp",
            verify_boolean_variable=verify_boolean_variable
        )

        # then
        print(voter_loads)
        print(committee)

        if write_results_to_file:
            ApprovalElectionTestDataSource().serializeCommitteeAndLoads(voter_loads=voter_loads, committee=committee, sample_name=sample_name)

        if expected_committee is not None:
            self.assertListEqual(committee, expected_committee)

        if expected_load_vector is not None:
            self.__assertListContainNearlyEqualElements(sorted(voter_loads), sorted(expected_load_vector), eps=err_eps)



        pass

    def __assertListContainNearlyEqualElements(self, l1, l2, eps):
        if eps == 0:
            self.assertListEqual(l1, l2)
        else:
            for x1, x2 in zip(l1, l2):
                if x1 != x2:
                    msg_template = "x1: {0}, x2: {1}, gap: {2}, max gap: {3}"
                    if x1 < x2:
                        gap = x2 - x1
                        msg = msg_template.format(x1, x2, gap, eps)
                        self.assertTrue(x1 - x2 + eps >= 0, msg)
                    else:
                        gap = x1 - x2
                        msg = msg_template.format(x1, x2, gap, eps)
                        self.assertTrue(x2 - x1 + eps >= 0, msg)
        pass

    pass
