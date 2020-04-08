from collections import OrderedDict
from typing import List, TypeVar, Any


class Utils:

    @classmethod
    def get_all_subsets(cls, elements: List[Any], size: int) -> List[List[Any]]:

        def iter(remaining: List[Any], small_subsets: List[List[Any]], full_subsets: List[List[Any]]) -> List[List[Any]]:
            if len(remaining) == 0:
                return full_subsets
            else:
                head = remaining[0]
                new_full_subsets = [[head] + list(x) for x in small_subsets if len(x) == size - 1]
                new_small_subsets = [[head] + list(x) for x in small_subsets if len(x) < size - 1]
                return iter(
                    remaining=remaining[1:],
                    small_subsets=small_subsets + new_small_subsets,
                    full_subsets=full_subsets + new_full_subsets
                )

        ret = iter(
            remaining=elements,
            small_subsets=[[]],
            full_subsets=[]
        )
        return ret

class ElectionInstance():

    def __init__(self, votes: List[List[int]], candidates: List[int]) -> None:
        self.votes = votes
        self.candidates = candidates

    def number_of_votes(self) -> int:
        return len(self.votes)

    def number_of_candidates(self) -> int:
        return len(self.candidates)

    def candidate_approval(self, candidate: int) -> int:
        score = 0
        for vote in self.votes:
            if candidate in vote:
                score += 1
        return score




class WinningCommittee:

    def __init__(self, candidates: List[int]) -> None:
        self.candidates = candidates

    def size(self):
        return len(self.candidates)

    def __str__(self):
        return str(self.candidates)


class FirstMajority:

    @classmethod
    def find_winning_committees(cls, election: ElectionInstance) -> List[WinningCommittee]:
        candidates_scores_dict = {c: election.candidate_approval(c) for c in election.candidates}
        ordered_candidates_scores_dict = OrderedDict(sorted(candidates_scores_dict.items(), key=lambda x: -x[1]))
        ordered_scores = list(ordered_candidates_scores_dict.values())
        ordered_candidates = list(ordered_candidates_scores_dict.keys())

        total_score = sum(ordered_scores)
        committee_score = 0
        number_of_winning_candidates = 0

        def is_committee_score_more_than_losers_score():
            return committee_score > total_score - committee_score

        while not is_committee_score_more_than_losers_score():
            committee_score += ordered_scores[number_of_winning_candidates]
            number_of_winning_candidates += 1

        prototype_committee = ordered_candidates[:number_of_winning_candidates]

        score_of_last_winner = ordered_scores[number_of_winning_candidates - 1]
        if number_of_winning_candidates < election.number_of_candidates():
            score_of_first_loser = ordered_scores[number_of_winning_candidates]
            if score_of_last_winner == score_of_first_loser:
                # multiple winning committees
                tied_candidates = [c for c, score in ordered_candidates_scores_dict.items() if score == score_of_last_winner]
                number_of_tied_candidates_in_prototype_committee = len(set(tied_candidates) & set(prototype_committee))
                base_committee = prototype_committee[:-number_of_tied_candidates_in_prototype_committee]
                all_tie_breakers = Utils.get_all_subsets(elements=list(tied_candidates),
                                                        size=number_of_tied_candidates_in_prototype_committee)
                all_tied_committees = [WinningCommittee(base_committee + tie_breaker) for tie_breaker in all_tie_breakers]
                return all_tied_committees
            else:
                # unique winning committee
                return [WinningCommittee(candidates=prototype_committee)]



class EnlarageCommitteeByAddingVoters:

    def __init__(self, election: ElectionInstance, spoiler_votes: List[List[int]], spoilers_to_add_limit: int):
        self.election = election
        self.spoiler_votes = spoiler_votes
        self.spoilers_to_add_limit = spoilers_to_add_limit

    def solve_brute_force(self) -> List[List[int]]:
        size_of_original_winning_committee = FirstMajority.find_winning_committees(election=self.election)[0].size()
        viable_spoiler_votes = []

        for number_of_spoilers_to_add in range(1, self.spoilers_to_add_limit + 1):
            for selected_spoiler_votes in Utils.get_all_subsets(elements=self.spoiler_votes, size=number_of_spoilers_to_add):
                spoiled_election = ElectionInstance(
                    candidates=self.election.candidates,
                    votes=self.election.votes + selected_spoiler_votes
                )
                new_committee_size = FirstMajority.find_winning_committees(election=spoiled_election)[0].size()
                if new_committee_size > size_of_original_winning_committee:
                    viable_spoiler_votes.append(selected_spoiler_votes)

        return viable_spoiler_votes

    def solve_greedy(self) -> List[List[int]]:
        pass




def main():
    print("Hello!")

    election = ElectionInstance(
        votes=[
            [0, 1, 2, 3, 5],
            [0, 5],
            [1, 3, 5],
            [3, 4],
            [3, 0, 4],
            [3, 1, 4]
        ],
        candidates=[0, 1, 2, 3, 4, 5]
    )

    winners = FirstMajority.find_winning_committees(election=election)

    for w in winners:
        print(w)


    en = EnlarageCommitteeByAddingVoters(
        election=ElectionInstance(
            votes = [
                [0],
                [0],
                [0],
                [1],
                [2],
            ],
            candidates=[0, 1, 2]
        ),
        spoiler_votes=[
            [2],
            [1],
            [2],
            [0]
        ],
        spoilers_to_add_limit=2
    )

    good_spoilers = en.solve_brute_force()
    for g in good_spoilers:
        print(g)



if __name__ == '__main__':
    main()
