from .rule_builder import RuleBuilder


def greedy(rule_class):
    return RuleBuilder().set_algorithm(find_committee).set_rule(rule_class).build()


# dobieranie kandydata który najbardziej powieksza wynik komitetu
def find_committee(self, k, profile):
    profile.clean_scores()
    for candidate in profile.candidates:
        profile.scores[candidate] = self.compute_score(candidate, k, profile)

    winners = sorted(profile.candidates, key=lambda x: profile.scores[x], reverse=True)
    return [w for w in winners[:k]]
