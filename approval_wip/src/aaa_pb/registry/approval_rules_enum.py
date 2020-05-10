from enum import Enum
from typing import List, Type

from aaa_pb.rules.approval.av import AV
from aaa_pb.rules.approval.cc import CC_Banzhaf, CC_ReverseGreedy_Slow, CC_ReverseGreedy, CC_Greedy, CC_Annealing
from aaa_pb.rules.approval.ilp.monroe import Monroe_ILP
from aaa_pb.rules.approval.ilp.owa import PAV_ILP, CC_ILP
from aaa_pb.rules.approval.ilp.pav_sp_tu import PAV_SinglePeaked_ILP
from aaa_pb.rules.approval.ilp.phragmen import PhragmenMax_ILP, PhragmenVar_ILP
from aaa_pb.rules.approval.pav import PAV_Annealing, PAV_ReverseGreedy, PAV_Greedy, PAV_Genetic
from aaa_pb.rules.approval.phragmen import PhragmenMax_Seq, PhragmenVar_Seq
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


class ApprovalRulesEnum(Enum):

    monroe_ilp = Monroe_ILP
    pav_ilp = PAV_ILP
    cc_ilp = CC_ILP
    pav_single_peaked_ilp = PAV_SinglePeaked_ILP

    phragmen_max_ilp = PhragmenMax_ILP
    phragment_var_ilp = PhragmenVar_ILP

    av = AV

    cc_banzhaf = CC_Banzhaf
    cc_reverse_greedy_slow = CC_ReverseGreedy_Slow
    cc_reversy_greedy = CC_ReverseGreedy
    cc_greedy = CC_Greedy
    cc_annealing = CC_Annealing

    pav_annealing = PAV_Annealing
    pav_reverse_greedy = PAV_ReverseGreedy
    pav_greedy = PAV_Greedy
    pav_genetic = PAV_Genetic

    phragmen_max_seq = PhragmenMax_Seq
    phragmen_var_seq = PhragmenVar_Seq


    @classmethod
    def getList(cls) -> List[Type[ApprovalBasedRuleBase]]:
        all_enum_values = list(cls)
        return [x.value for x in all_enum_values]

    @classmethod
    def getByNames(cls, names: List[str]) -> List[Type[ApprovalBasedRuleBase]]:
        # TODO use names of enum values!!
        rules_list = cls.getList()

        def get_rule_by_short_name(name: str) -> Type[ApprovalBasedRuleBase]:
            gen = (rule for rule in rules_list if rule.getShortName() == name)
            ruleOpt = next(gen, None)
            if ruleOpt is None:
                raise Exception("Could not find rule: '{0}'".format(name))
            return ruleOpt

        rules = [get_rule_by_short_name(name) for name in names]
        return rules


