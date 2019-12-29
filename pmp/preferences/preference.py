class Preference:
    """Single voter preference."""

    def __init__(self, order=[], weights=None):
        """
        :param order: List of candidates
        :type order: List(Number)
        :param weights: Optional weights corresponding to candidates from order
        :type weights: List(Number)
        """
        self.order = list(order)
        self.weights = list(weights) if weights is not None else weights
        self.candidates_num = len(self.order)

    def is_valid(self, num_cand):
        """
        :param num_cand: Number of candidates
        :type num_cand: Number
        :return: Boolean

        Check if Preference is valid under profile with given candidates number
        """
        raise NotImplementedError()
