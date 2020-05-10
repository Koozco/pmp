import collections
from typing import List, Set

from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


# TODO
class PhragmenMax_Seq(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        return _seqPhragmen(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates,
            isMax=True
        )


# TODO
class PhragmenVar_Seq(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        """ Based on "Phragmen's Voting Methods and Justified Representation" Brill et. al. """
        return _seqPhragmen(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates,
            isVar=True
        )

# TODO
def _seqPhragmen(V: List[List[int]], k: int, number_of_candidates: int, isMax: bool=False, isVar: bool=False) -> List[int]:

    # TODO use from fractions import Fraction ?
    # TODO use rational numbers rather than floats ?

    assert (isMax is True and isVar is False) or (isMax is False and isVar is True)

    committee = []
    voter_loads = [0.0] * len(V)
    remaining_candidates = set(range(number_of_candidates))
    more_than_maximal_load = k + 1

    def computeBackersForEachCandidate() -> List[Set[int]]:
        backers = [set() for _ in range(number_of_candidates)]
        for voter, vote in enumerate(V):
            for c in vote:
                backers[c].add(voter)
        return backers

    candidate_to_voters_map = computeBackersForEachCandidate()

    def updateVotersLoads(selected_candidate, new_load):  # TODO this looks fishy!
        backers = candidate_to_voters_map[selected_candidate]
        for v in backers:
            voter_loads[v] = new_load
        pass

    # Maximum load optimization variant
    def maxLoadIfWeSelect(candidate):
        backers = candidate_to_voters_map[candidate]
        if len(backers) == 0:
            return more_than_maximal_load
        backers_loads_total = 0.0
        for voter in backers:
            backers_loads_total += voter_loads[voter]
        # add 1 unit of load and distribute it evenly among the backers
        max_load = (1.0 + backers_loads_total) / len(backers)
        return max_load

    # TODO not sure at all if it's correct
    # Maximal variance optimization variant
    def sumOfSquaresOfVoterLoadsIfWeSelect(candidate):
        backers = candidate_to_voters_map[candidate]
        if len(backers) == 0:
            # return sys.maxint
            python2_sys_maxint = 9223372036854775807
            return python2_sys_maxint

        backers_loads = [voter_loads[v] for v in backers]
        max_loads = (1.0 + sum(backers_loads)) / len(backers)
        nonBackersSumOfSquaresOfLoads = sum([voter_loads[x] ** 2 for x in range(0, len(V)) if x not in backers])
        return (max_loads ** 2) * len(backers) + nonBackersSumOfSquaresOfLoads

    if isMax:
        optimizationCriterionIfWeSelectCandidateFun = maxLoadIfWeSelect
    elif isVar:
        optimizationCriterionIfWeSelectCandidateFun = sumOfSquaresOfVoterLoadsIfWeSelect
    else:
        raise Exception

    votes_per_candidate = collections.defaultdict(int)  # TODO maybe use a list to be faster

    for v in V:
        for c in v:
            votes_per_candidate[c] += 1

    candidate_with_most_votes = ApprovalBasedRuleBase.randomUtils.keyOfMaxValueFromDict(votes_per_candidate)

    committee.append(candidate_with_most_votes)
    remaining_candidates.remove(candidate_with_most_votes)
    updateVotersLoads(
        selected_candidate=candidate_with_most_votes,
        new_load=1.0 / votes_per_candidate[candidate_with_most_votes]
    )

    for _ in range(1, k):
        candidate_to_max_load = {c: optimizationCriterionIfWeSelectCandidateFun(c) for c in remaining_candidates}

        candidate_inducing_smallest_load = ApprovalBasedRuleBase.randomUtils.keyOfMinValueFromDict(
            candidate_to_max_load)

        committee.append(candidate_inducing_smallest_load)
        remaining_candidates.remove(candidate_inducing_smallest_load)

        smallest_max_load = candidate_to_max_load[candidate_inducing_smallest_load]
        updateVotersLoads(
            selected_candidate=candidate_inducing_smallest_load,
            new_load=smallest_max_load
        )

    return committee
