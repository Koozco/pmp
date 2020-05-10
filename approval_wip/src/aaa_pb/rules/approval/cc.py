import collections
import operator
# OK
from typing import List, Tuple, Dict, Set

import gmpy2

from aaa_pb.rules.approval._annealing import Annealing_Meta
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase
# alphaCC is NP-hard
# greedy algorithm by Boutilier 2011
# FPT approximation shceme for alphaCC (parameterized by committee size) Skowron, Faliszewski 2015
# heuristic by clustering, Faliszewski 2016c
from aaa_pb.rules.bruteforcetemplate import BruteForceRule


class CC_BruteForce:

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> Tuple[List[List[int]], float]:
        return BruteForceRule.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            scoreCommitteeFun=CommitteeScore.CC
        )


class CC_Banzhaf(ApprovalBasedRuleBase):
    """ Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al."""

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee_set = set()
        V_sets = [set(v) for v in V]

        def binomial(n, k):
            return gmpy2.comb(n, k)

        def computeRestrictedBanzhafValue(committee_set, c):
            committee_size = len(committee_set)
            number_of_open_seats = k - 1 - committee_size
            value = 0

            for vote in V_sets:
                if c in vote:
                    number_of_alternatives_to_choose_from = number_of_candidates - committee_size - len(vote)
                    if number_of_alternatives_to_choose_from >= number_of_open_seats:
                        value += binomial(n=number_of_alternatives_to_choose_from, k=number_of_open_seats)
            return value

        remaining_candidates = list(range(number_of_candidates))

        for _ in range(k):
            # consider only voters who don't have representatives
            V_sets = [v for v in V_sets if not v.isdisjoint(committee_set)]

            banzfahs = {c: computeRestrictedBanzhafValue(committee_set, c) for c in remaining_candidates}
            next_committee_member = clazz.randomUtils.keyOfMaxValueFromDict(banzfahs)
            committee_set.add(next_committee_member)
            remaining_candidates.remove(next_committee_member)

        return list(committee_set)

    pass


# nah OK
# we don't use it but for tests to compare results with those from the normal (fast) version
class CC_ReverseGreedy_Slow(ApprovalBasedRuleBase):
    """ Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al."""

    excluded = True

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee = list(range(number_of_candidates))

        def computeCommitteeScore(committee):
            score = 0
            committee_set = set(committee)
            for vote in V:
                if not committee_set.isdisjoint(vote):
                    score += 1
            return score

        for committee_size in reversed(range(k + 1, number_of_candidates + 1)):

            best_committees = []
            best_score = -1

            for i in range(committee_size):
                tmp_committee = committee[:i] + committee[i + 1:]
                score = computeCommitteeScore(tmp_committee)

                if score == best_score:
                    best_committees.append(tmp_committee)
                if score > best_score:
                    best_score = score
                    best_committees = [tmp_committee]

            best_tmp_committee = ApprovalBasedRuleBase.randomUtils.chooseOne(best_committees)
            committee = best_tmp_committee

        return committee

    pass


# OK
class CC_ReverseGreedy(ApprovalBasedRuleBase):
    """ Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al."""

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee = list(range(number_of_candidates))
        more_than_the_biggest_score_of_a_candidate = len(V) + 1

        def computeCandidateToVotesWithThatCandidateMap():
            map = collections.defaultdict(list)
            for vote in V:
                for c in vote:
                    map[c].append(vote)
            return map

        candidate_to_votes_with_that_candidate_map = computeCandidateToVotesWithThatCandidateMap()

        # how much removal of c would change the score of the whole committee
        # non-negative value
        def computeCandidateScoreDelta(c):
            delta = 0
            for vote in candidate_to_votes_with_that_candidate_map[c]:
                # check if c is the only representative of the voter in the committee
                if len(vote) == 1:
                    # c is the only representative of the voter
                    # so removing c from the committee
                    # lowers the score of the committee by 1
                    delta += 1
            return delta

        # once a candidate is removed from the committee for good
        # we remove it from the votes
        # keeps the votes containing only candidates who are still in the committee
        def removeCandidateFromVotes(c):
            for vote in candidate_to_votes_with_that_candidate_map[c]:
                vote.remove(c)
            pass

        i = number_of_candidates
        while i > k:
            i -= 1

            worst_candidates = []
            min_score_delta = more_than_the_biggest_score_of_a_candidate

            for c in committee:
                score_delta = computeCandidateScoreDelta(c)

                if score_delta == min_score_delta:
                    worst_candidates.append(c)
                elif score_delta < min_score_delta:
                    min_score_delta = score_delta
                    worst_candidates = [c]

            worst_candidate = ApprovalBasedRuleBase.randomUtils.chooseOne(worst_candidates)
            committee.remove(worst_candidate)
            removeCandidateFromVotes(worst_candidate)

        return committee


# OK
# TODO random tie breaking !
class CC_Greedy(ApprovalBasedRuleBase):
    """
    Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al.
    """

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee = []

        def computeVotersApprovingACandidates() -> Dict[int, Set[int]]:
            result = collections.defaultdict(set)
            for voter, vote in enumerate(V):
                for c in vote:
                    result[c].add(voter)
            return result

        candidate_to_voters_map = computeVotersApprovingACandidates()

        def removeVotersFor(candidate):
            voters_to_remove = candidate_to_voters_map[candidate_with_most_voters]
            del candidate_to_voters_map[candidate]
            for votersSet in candidate_to_voters_map.values():
                votersSet.difference_update(voters_to_remove)
            pass

        for _ in range(k):
            candidate_with_most_voters = clazz.randomUtils.keyOfMaxFromDict(candidate_to_voters_map,
                                                                            max_key=lambda x: len(
                                                                                operator.itemgetter(1)(x)))
            committee.append(candidate_with_most_voters)
            # keep only voters without a representative
            removeVotersFor(candidate=candidate_with_most_voters)

        return committee


# OK, though a bit slow
class CC_Annealing(ApprovalBasedRuleBase):
    """ Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al."""

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        V_set = [set(v) for v in V]

        def computeCommitteeScore(committee: List[int]) -> int:
            score = 0
            for vote in V_set:
                if not vote.isdisjoint(committee):
                    score += 1
            return score

        return Annealing_Meta.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            compute_committee_score_fun=computeCommitteeScore
        )


