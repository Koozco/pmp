from types import MethodType
from rules.rule import Rule


class RuleBuilder:

    def __init__(self):
        self.rule_class = None
        self.algorithm = None

    def build(self):
        if self.rule_class is None:
            raise Exception("Rule is not set.")
        if self.algorithm is None:
            raise Exception("Algorithm is not set.")

        rule = self.rule_class()
        rule.find_committee = MethodType(self.algorithm, rule)
        return rule

    def set_rule(self, rule_class):
        if not issubclass(rule_class, Rule):
            raise Exception("Rule must inherit from Rule class.")

        self.rule_class = rule_class
        return self

    def set_algorithm(self, algorithm_function):
        if not callable(algorithm_function):
            raise Exception("Algorithm must be callable.")

        self.algorithm = algorithm_function
        return self
