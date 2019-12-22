from .tie_breaking import random_winner
from .._common import default_methods_registry


class Rule:
    """Scoring rule class."""

    methods = default_methods_registry()

    def __init__(self, tie_break=random_winner):
        self.tie_break = tie_break

    def find_committee(self, k, profile):
        """
        :param k: size of committee to find
        :type k: String
        :param profile: preferences profile object
        :type profile: Profile
        :return: committee winning under given rule
        """
        raise NotImplementedError()

    def compute_candidate_scores(self, k, profile):
        """
        :param k: size of committee to find
        :type k: String
        :param profile: preferences profile object
        :type profile: Profile

        If it is possible, fill profile.scores member dictionary with scores of all committees
        """
        raise NotImplementedError()

    def compute_committee_score(self, committee, k, profile):
        """
        :param committee: list of candidates
        :type committee: List
        :param k: size of committee to find
        :type k: String
        :param profile: preferences profile object
        :type profile: Profile

        Find score assigned to given committee
        """
        raise NotImplementedError()
