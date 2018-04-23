class Rule:
    """Scoring rule."""

    def __init__(self, committee_size, candidates, preferences):
        self.k = committee_size
        self.candidates = candidates
        self.preferences = preferences

    def find_committee(self):
        raise NotImplementedError()
