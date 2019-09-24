from .preference import Preference


class Approval(Preference):
    """Approval preference profile."""

    def __init__(self, approved):
        Preference.__init__(self, list(approved))
        self.approved = set(approved)

    def is_valid(self, num_cand):
        return len(self.approved) <= num_cand
