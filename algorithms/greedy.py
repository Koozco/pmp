from .rule_builder import RuleBuilder


def greedy(rule_class):
    return RuleBuilder().set_algorithm(find_committee).set_rule(rule_class).build()


def find_committee(self, profile, k):
    pass
