import unittest

from aaa_pb.rules.approval.phragmen import PhragmenMax_Seq


class SeqMaxPhragmen_Text(unittest.TestCase):

    def test_SexMaxPhragmen(self):

        # test case from "Phragmen's Voting Methods and Justified Representation" Brill et. al.

        # given
        k = 3
        V = [
            [0],
            [1],
            [1, 2],
            [0, 1, 2],
            [3]
        ]

        # when
        actual_committee = sorted(PhragmenMax_Seq.apply(
            V=V,
            number_of_candidates=4,
            k=k))

        # then
        if actual_committee != [0, 1, 2]:
            self.assertListEqual(actual_committee, [0, 1, 3])
        # [0, 1, 2] != [0, 1, 3]
        pass
