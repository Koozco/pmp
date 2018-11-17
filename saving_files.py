import os


def save_to_file(candidates=None, preferences=None, voters=None, k=0, winners=None):
    m = 0
    n = 0
    if candidates:
        m = len(candidates)
    if voters:
        n = len(voters)
    print(m, n, k)

    if candidates:
        save_candidates(candidates)
    if preferences and voters:
        save_preferences(voters, preferences)
    if winners:
        save_winners(winners, candidates)


def save_candidates(candidates):
    for i in range(len(candidates)):
        print(i, *candidates[i])


def save_preferences(voters, preferences):
    for i in range(len(preferences)):
        preference = ' '.join(map(str, preferences[i].order))
        voter = ' '.join(map(str, voters[i][:-1]))
        print(preference, voter)


def save_winners(winners, candidates):
    for i in range(len(winners)):
        candidate = ' '.join(map(str, candidates[i]))
        print(i, candidate)
