from .preference import Preference

class Approval(Preference):
    """Approval preference profile."""

    def __init__(self, approved):
        Preference.__init__(self, list(approved))
        self.approved = set(approved)
