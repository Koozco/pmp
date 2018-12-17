from .rule import Rule
from .tie_breaking import random_winner
from itertools import combinations


class WeaklySeparable(Rule):
    """ Weakly Separable scoring rule """

    def __init__(self, weights=None, tie_break=random_winner):
        Rule.__init__(self, tie_break)
        self.weights = weights

    def compute_candidate_scores(self, k, profile):
        profile.clean_scores()
        for pref in profile.preferences:
            for n in range(len(pref.order)):
                candidate = pref.order[n]
                weight = self.weights[n] if n < len(self.weights) else 0
                if candidate in profile.scores:
                    profile.scores[candidate] += weight
                else:
                    profile.scores[candidate] = weight

    def compute_score(self, candidate, _, profile):
        score = 0
        for pref in profile.preferences:
            i = pref.order.index(candidate)
            weight = self.weights[i] if i < len(self.weights) else 0
            score += weight
        return score

    def committee_score(self, committee, profile):
        score = 0
        for cand in committee:
            score += self.compute_score(cand, len(committee), profile)
        return score

    def get_committees(self, k, candidates_with_score):
        all_scores = candidates_with_score.keys()
        decreasing_scores = sorted(all_scores, reverse=True)
        committees = []

        score_index = 0
        committee = []
        committee_size = 0
        while committee_size < k:
            score = decreasing_scores[score_index]
            if committee_size + len(candidates_with_score[score]) <= k:
                committee += candidates_with_score[score]
                committee_size += len(candidates_with_score[score])
            else:
                complement_size = k - committee_size
                complements = list(combinations(candidates_with_score[score], complement_size))

                for complement in complements:
                    committees.append(committee + list(complement))
                committee_size += complement_size

            score_index += 1

        if len(committees) == 0:
            committees.append(committee)
        return committees

    def find_committee(self, k, profile):
        if self.weights is None:
            raise Exception("Weights not set.")
        profile.clean_scores()
        self.compute_candidate_scores(k, profile)

        profile.candidates_with_score = {}
        for cand_id in range(len(profile.candidates)):
            score = profile.scores[cand_id]
            if profile.candidates_with_score.get(score) is None:
                profile.candidates_with_score[score] = []
            profile.candidates_with_score[score].append(cand_id)

        committees = self.get_committees(k, profile.candidates_with_score)
        committee = self.tie_break(committees)

        return committee
