from typing import Type

from rules.approval_based_rule_base import ApprovalBasedRuleBase


class ElectionsExperimentParameters:

    def __init__(self, rule_class: Type[ApprovalBasedRuleBase], committee_size: int) -> None:
        self.committee_size = committee_size
        self.rule_class = rule_class

    def mkString(self) -> str:
        return "committee_size {0}, rule_name: {1}".format(self.committee_size, self.rule_class.getName())
