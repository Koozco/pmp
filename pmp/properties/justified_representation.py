from numpy import zeros


def has_approvaed_candidate(preference, committee):
    return len(preference.approved & committee) > 0


def justified_representation(profile, committee):
    k = len(committee)
    n = len(profile.preferences)
    m = len(profile.candidates)
    quota = int(n / k)
    justified = True

    appearances = zeros(m + 1, dtype=int)
    voters_without_approved_candidate = [v for v in profile.preferences if not has_approvaed_candidate(v, committee)]

    for v in voters_without_approved_candidate:
        for c in v.approved:
            appearances[c] += 1
            if appearances[c] >= quota:
                justified = False
                break
        if not justified:
            break

    return justified
