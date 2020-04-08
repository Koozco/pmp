import random
from typing import List, Tuple

## TODO revise all implementation to use random tie-breaking
from aaa_pb.rules.approval._annealing import Annealing_Meta
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase
from aaa_pb.rules.bruteforcetemplate import BruteForceRule


class PAV_BruteForce:

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> Tuple[List[List[int]], float]:

        return BruteForceRule.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            scoreCommitteeFun=CommitteeScore.PAV
        )


# OK, though a bit slow
class PAV_Annealing(ApprovalBasedRuleBase):
    """ Based on "Effective Heuristics for Committee Scoring Rules", Faliszewski et. al."""

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        V_set = [set(v) for v in V]

        number_of_representatives_to_score_map = clazz.getScoreMapForCommitteeSize(k)

        def computeCommitteeScore(committee: List[int]) -> int:
            score = 0
            for vote in V_set:
                number_of_representatives = len(vote.intersection(committee))
                score += number_of_representatives_to_score_map[number_of_representatives]
            return score

        return Annealing_Meta.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            compute_committee_score_fun=computeCommitteeScore
        )

    cache = {}

    @classmethod
    def getScoreMapForCommitteeSize(clazz, k: int) -> List[float]:
        if k not in clazz.cache:
            harmonic_series = [1.0 / p for p in range(1, k + 1)]
            number_of_representatives_to_score_map = [1.0]
            for i in range(1, k):
                number_of_representatives_to_score_map.append(
                    harmonic_series[i] + number_of_representatives_to_score_map[i - 1]
                )
            clazz.cache[k] = [0.0] + number_of_representatives_to_score_map

        return clazz.cache[k]

    pass


class PAV_ReverseGreedy(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        """
        based on description from "Proportional Justified Representation", Sanchez-Fernandez et. al.
        """

        committee = list(range(number_of_candidates))
        more_than_the_biggest_score_of_a_candidate = len(V) + 1

        # when a candidate is dropped from the committee
        # she/he is also removed from the votes,
        # so votes contain candidates that belong to the winning committee
        V = [set(vote) for vote in V]

        def computeApprovalWeight(c, V):
            weight = 0.0
            for vote in V:
                if c in vote:
                    vote_length = len(vote)
                    weight += 1.0 / vote_length
            return weight

        def removeCandidateFromVotes(c, V):
            V2 = []
            for vote in V:
                if c in vote:
                    if len(vote) == 1:
                        continue
                    else:
                        vote.remove(c)
                V2.append(vote)
            return V2

        currentCommitteeSize = number_of_candidates

        while currentCommitteeSize > k:

            worstCandidates = []
            smallestScore = more_than_the_biggest_score_of_a_candidate

            for c in committee:
                score = computeApprovalWeight(
                    c=c,
                    V=V)
                if score == smallestScore:
                    worstCandidates.append(c)
                elif score < smallestScore:
                    worstCandidates = [c]
                    smallestScore = score

            theWorstCandidate = ApprovalBasedRuleBase.randomUtils.chooseOne(worstCandidates)
            committee.remove(theWorstCandidate)
            V = removeCandidateFromVotes(
                c=theWorstCandidate,
                V=V
            )

            currentCommitteeSize -= 1

        return committee


# OK
class PAV_Greedy(ApprovalBasedRuleBase):
    """
    Based on description from "Proportional Justified Representation", Sanchez-Fernandez et. al.
    """

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        # print(V)
        committee_set = set()
        remaining_candidates = list(range(number_of_candidates))

        V_sets = [set(v) for v in V]

        def computeApprovalScore(c):
            result = 0.0
            for vote in V_sets:
                if c in vote:
                    number_of_representatives_so_far = len(committee_set.intersection(vote))
                    result += 1.0 / (1 + number_of_representatives_so_far)
            return result

        for _ in range(k):

            best_score = -1.0
            best_candidates = []

            for c in remaining_candidates:

                score = computeApprovalScore(c)

                if score == best_score:
                    best_candidates.append(c)
                if score > best_score:
                    best_score = score
                    best_candidates = [c]

            best_candidate = clazz.randomUtils.chooseOne(best_candidates)
            remaining_candidates.remove(best_candidate)
            committee_set.add(best_candidate)

        return list(committee_set)


class PAV_Genetic(ApprovalBasedRuleBase):
    """
    Based on description from "Proportional Justified Representation", Sanchez-Fernandez et. al.
    """

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        def gen_initial_population(size):
            population = []
            candidates = list(range(number_of_candidates))
            for _ in range(size):
                random.shuffle(candidates)
                population.append(sorted(candidates[:k]))
            return population

        def sort_from_best(population):
            population = sorted(population, key=lambda p: CommitteeScore.PAV(V=V, committee=p), reverse=True)
            return population

        def check_is_valid_committee(committee):
            assert len(committee) == k
            assert len(set(committee)) == k
            assert sorted(committee) == committee
            pass

        candidates_set = set(range(number_of_candidates))

        def mutate(p):
            set_p = set(p)
            possibilities = [x for x in candidates_set if x not in set_p]
            if len(possibilities) == 0:
                return []
            choice = random.choice(possibilities)
            idx = random.randint(0, k - 1)
            p[idx] = choice
            p = sorted(p)
            check_is_valid_committee(p)
            return [p]

        def crossover(p1, p2):
            p12 = list(set(p1 + p2))
            random.shuffle(p12)
            p3 = sorted(p12[:k])
            check_is_valid_committee(p3)
            return [p3]

        population_size = 100
        number_of_generations = 1000
        mutation_probability = 0.02
        crossover_probability = 0.02

        population = gen_initial_population(population_size)

        population = sort_from_best(population)

        for _ in range(number_of_generations):
            assert population_size == len(population), "expected: {0} vs. actual: {1}".format(population_size,
                                                                                              len(population))
            for p in list(population):
                if random.random() < mutation_probability:
                    population.extend(mutate(p))

            p1 = None
            for p in list(population):
                if random.random() < crossover_probability:
                    if p1 is None:
                        p1 = p
                    else:
                        population.extend(crossover(p1, p))

            population = sort_from_best(population)[:population_size]

        return sorted(population[0])
