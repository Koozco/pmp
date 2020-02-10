class Profile:
    """Profile of voters' preferences"""

    def __init__(self, candidates=None, preferences=None):
        """
        :param candidates: Candidates list
        :type candidates: List(Number)
        :param preferences: Preferences list
        :type preferences: List(Preference)
        """
        if candidates is None:
            candidates = []
        if preferences is None:
            preferences = []
        self.candidates = candidates
        self.num_cand = len(candidates)
        self.preferences = preferences
        self.scores = {}

    def add_preference(self, preference):
        """
        :param preference: Added preference
        :type preference: Preference

        Add single preference to the profile. Works only if preference is valid.
        """
        if preference.is_valid(self.num_cand):
            self.preferences.append(preference)

    def add_preferences(self, preferences):
        """
        :param preferences: Added preferences
        :type preferences: List(Preference)

        Add preferences to the profile. Adds only the valid ones.
        """
        for pref in preferences:
            if not pref.is_valid(self.num_cand):
                return
        self.preferences += preferences

    def clean_scores(self):
        """Clear candidates scores cached in profile"""
        self.scores = {x: 0 for x in range(len(self.candidates))}

    def __str__(self):
        return 'Profile with %d voters and %d candidates: ' % (len(self.preferences), self.num_cand) + ', '.join(
            map(str, self.preferences))
