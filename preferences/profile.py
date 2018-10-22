class Profile:
    """Profile of voters' preferences"""

    def __init__(self, candidates=None, preferences=None):
        if candidates is None:
            candidates = []
        if preferences is None:
            preferences = []
        self.candidates = candidates
        self.num_cand = len(candidates)
        self.preferences = preferences
        self.scores = {}

    def add_preference(self, preference):
        preference.is_valid(self.num_cand)
        self.preferences.append(preference)

    def add_preferences(self, preferences):
        for pref in preferences:
            pref.is_valid(self.num_cand)
        self.preferences += preferences

    def clean_scores(self):
        self.scores = {x: 0 for x in self.candidates}

    def __str__(self):
        return 'Profile with %d votes and %d candidates: ' % (len(self.preferences), self.num_cand) + ', '.join(
            map(str, self.preferences))
