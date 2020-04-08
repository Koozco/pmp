from functools import reduce


class Profile(object):
    def __init__(self, num_cand, cand_names=None):
        self.num_cand = num_cand
        self.preferences = []
        self.cand_names = cand_names if cand_names else {}

    def add_preference(self, preference):
        preference.is_valid(self.num_cand)
        self.preferences.append(preference)

    def add_preferences(self, preferences):
        for pref in preferences:
            pref.is_valid(self.num_cand)
        self.preferences += preferences

    def voters_num(self):
        return reduce(lambda acc, prof: acc + prof.weight, self.preferences, 0)

    def raw_voters(self):
        return [pref.order for pref in self.preferences]

    def remove_candidate(self, cand):
        new_prefs = map(lambda pref: pref.remove_candidate(cand), self)
        new_prof = Profile(self.num_cand - 1)
        new_prof.add_preferences(new_prefs)
        return new_prof

    def remove_voters(self, voters):
        set_voters = set(voters)
        new_prefs = [elem for (_, elem) in
                     filter(lambda tup: tup[0] not in set_voters, enumerate(list(self)))]
        new_prof = Profile(self.num_cand)
        new_prof.add_preferences(new_prefs)
        return new_prof

    def __iter__(self):
        return iter(self.preferences)

    def __str__(self):
        return 'Profile with %d votes and %d candidates: ' % (len(self.preferences), self.num_cand) + ', '.join(
            map(str, self.preferences))
