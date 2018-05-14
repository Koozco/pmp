class Profile:
    """Profile of voters' preferences"""

    def __init__(self, candidates):
        self.candidates = candidates
        self.num_cand = len(candidates)
        self.preferences = []

    def add_preference(self, preference):
        preference.is_valid(self.num_cand)
        self.preferences.append(preference)

    def add_preferences(self, preferences):
        for pref in preferences:
            pref.is_valid(self.num_cand)
        self.preferences += preferences

    def __str__(self):
        return 'Profile with %d votes and %d candidates: ' % (len(self.preferences), self.num_cand) + ', '.join(
            map(str, self.preferences))

