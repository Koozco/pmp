from .rule_builder import RuleBuilder


def greedy(rule_class, k):
    return RuleBuilder().set_algorithm(find_committee).set_rule(rule_class).set_k(k).build()


def find_committee(self, profile):
    profile.clean_scores()
    for candidate in profile.candidates:
        profile.scores[candidate] = self.compute_score(candidate, profile)

    winners = sorted(profile.candidates, key=lambda x: profile.scores[x], reverse=True)
    return [w for w in winners[:self.k]]
