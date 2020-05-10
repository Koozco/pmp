"""This module contains implementations of many multwinner voting rules. As of now, only rules based on approval preferences (dichotomous preferences) are implemented.

* Reweighted Approval Voting (RAV)

  - with tie-breaking [Gurobi optional]

  - without tie-breaking

* Proportional Approval Voting (PAV)

* Phragmen's rules

  - maxPhragmen without lexicographic tie-breaking [Gurobi req.]
 
  - maxPhragmen without lexicographic tie-breaking, refined [Gurobi req.]
 
  - varPhragmen [Gurobi req.]

  - seqPhragmen

* Approval Chamberlin-Courant

  - the optimization variant [Gurobi optional]
 
  - the sequential (greedy) variant
  
* Monroe [Gurobi req.]

.. moduleauthor:: Martin Lackner

"""

import rules.rule_approval_ilp
import functools
import itertools
import sys
from gmpy2 import mpq


def __enough_approved_candiates(profile, committeesize):
    appr = set()
    for pref in profile.preferences:
        appr.update(pref.approved)
    if len(appr) < committeesize:
        print("committeesize =", committeesize, "is larger than number of approved candidates")
        print(profile)
        exit()


def __get_scorefct(scorefct_str, committeesize):
    if scorefct_str == 'pav':
        return __pav_score_fct
    elif scorefct_str == 'cc':
        return __cc_score_fct
    elif scorefct_str == 'av':
        return __av_score_fct
    elif scorefct_str[:4] == 'geom':
        base = mpq(scorefct_str[4:])
        return functools.partial(__geom_score_fct, base=base)
    elif scorefct_str.startswith('generalizedcc'):
        param = mpq(scorefct_str[13:])
        return functools.partial(__generalizedcc_score_fct, l=param, committeesize=committeesize)
    elif scorefct_str.startswith('lp-av'):
        param = mpq(scorefct_str[5:])
        return functools.partial(__lp_av_score_fct, l=param)
    else:
        print("Error: scoring function", scorefct_str, "does not exist.")
        sys.exit()


def thiele_score(profile, committee, scorefct_str):
    scorefct = __get_scorefct(scorefct_str, len(committee))
    score = 0
    for pref in profile.preferences:
        cand_in_com = 0
        for _ in set(committee) & pref.approved:
            cand_in_com += 1
            score += pref.weight * scorefct(cand_in_com)
    return score


def compute_thiele_methods_branchandbound(profile, committeesize, scorefct_str, tiebreaking=False):
    __enough_approved_candiates(profile, committeesize)
    scorefct = __get_scorefct(scorefct_str, committeesize)

    best_committees = [compute_seq_thiele_methods_with_tiebreaking(profile, committeesize, scorefct_str)[0]]
    best_score = thiele_score(profile, best_committees[0], scorefct_str)
    part_coms = [[]]
    while part_coms:
        part_com = part_coms.pop(0)
        if len(part_com) == committeesize:  # potential committee, check if at least as good as previous best committee
            score = thiele_score(profile, part_com, scorefct_str)
            if score == best_score:
                if not tiebreaking:
                    best_committees.append(part_com)  # we compute ALL optimal committees
            elif score > best_score:
                best_committees = [part_com]
                best_score = score
        else:
            if len(part_com) > 0:
                largest_cand = part_com[-1]
            else:
                largest_cand = -1
            missing_candidates = committeesize - len(part_com)
            marg_util_cand = __additional_thiele_scores(profile, part_com, scorefct)
            upper_bound = sum(sorted(marg_util_cand[largest_cand + 1:])[-missing_candidates:]) + thiele_score(profile,
                                                                                                              part_com,
                                                                                                              scorefct_str)
            if upper_bound >= best_score:
                for c in range(largest_cand + 1, profile.num_cand - missing_candidates + 1):
                    part_coms.insert(0, part_com + [c])
    return sorted(best_committees)


def compute_seqpav(profile, committeesize, tiebreaking=False):
    """This function computes the *Reweighted Approval Voting* rule

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

       tiebreaking (bool): Whether or not tiebreaking is used. If tiebreaking is true, then only one committee is returned. The computation is faster if tiebreaking is true.

    Returns:
       A list containing all winning committees if tiebreaking is false. If tiebreaking is true, a list containing a single committee is returned.
    """
    if tiebreaking:
        return compute_seq_thiele_methods_with_tiebreaking(profile, committeesize, 'pav')
    else:
        return compute_seq_thiele_methods(profile, committeesize, 'pav')


def compute_seqcc(profile, committeesize, tiebreaking=False):
    """This function computes the *Greedy Chamberlin-Courant* rule

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

       tiebreaking (bool): Whether or not tiebreaking is used. If tiebreaking is true, then only one committee is returned. The computation is faster if tiebreaking is true.

    Returns:
       A list containing all winning committees if tiebreaking is false. If tiebreaking is true, a list containing a single committee is returned.
    """
    if tiebreaking:
        return compute_seq_thiele_methods_with_tiebreaking(profile, committeesize, 'cc')
    else:
        return compute_seq_thiele_methods(profile, committeesize, 'cc')


# SATISFACTION APPROVAL VOTING (without tie breaking)
def compute_sav(profile, committeesize):
    """This function computes the *Satisfaction Approval Voting* rule

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    __enough_approved_candiates(profile, committeesize)

    sav_scores = [0] * profile.num_cand
    for pref in profile.preferences:
        for cand in pref.approved:
            sav_scores[cand] += mpq(pref.weight, len(pref.approved))
    cutoff = sorted(sav_scores)[-committeesize]  # smallest score to be in the committee
    certain_cand = [c for c in range(profile.num_cand) if sav_scores[c] > cutoff]
    possible_cand = [c for c in range(profile.num_cand) if sav_scores[c] == cutoff]
    if len(certain_cand) >= committeesize:
        return [sorted(list(selection)) for selection in itertools.combinations(certain_cand, committeesize)]
    else:
        return [sorted(certain_cand + list(selection)) for selection in
                itertools.combinations(possible_cand, committeesize - len(certain_cand))]


def __generalizedcc_score_fct(i, l, committeesize):
    # corresponds to (1,1,1,..,1,0,..0) of length *committeesize* with *l* zeros
    # l=committeesize-1 ... Chamberlin-Courant
    # l=0 ... Approval Voting
    if i > committeesize - l:
        return 0
    if i > 0:
        return 1
    else:
        return 0


def __lp_av_score_fct(i, l):
    # l-th root of i
    # l=1 ... Approval Voting
    # l=\infty ... Chamberlin-Courant
    if i == 1:
        return 1
    else:
        return i ** mpq(1, l) - (i - 1) ** mpq(1, l)


def __geom_score_fct(i, base):
    if i == 0:
        return 0
    else:
        return mpq(1, base ** i)


def __pav_score_fct(i):
    if i == 0:
        return 0
    else:
        return mpq(1, i)


def __av_score_fct(i):
    if i >= 1:
        return 1
    else:
        return 0


def __cc_score_fct(i):
    if i == 1:
        return 1
    else:
        return 0


def __cumulative_score_fct(scorefct, cand_in_com):
    return sum(scorefct(i + 1) for i in range(cand_in_com))


# returns a list of length num_cand
# the i-th entry contains the marginal score increase gained by adding candidate i  
def __additional_thiele_scores(profile, committee, scorefct):
    marg = [0] * profile.num_cand
    for pref in profile.preferences:
        for c in pref.approved:
            if pref.approved & set(committee):
                marg[c] += pref.weight * scorefct(len(pref.approved & set(committee)) + 1)
            else:
                marg[c] += pref.weight * scorefct(1)
    for c in committee:
        marg[c] = -1
    return marg


# APPROVAL VOTING
def compute_av(profile, committeesize, tiebreaking=False):
    """Computes the *Approval Voting* rule

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    __enough_approved_candiates(profile, committeesize)

    appr_scores = [0] * profile.num_cand
    for pref in profile.preferences:
        for cand in pref.approved:
            appr_scores[cand] += pref.weight
    cutoff = sorted(appr_scores)[-committeesize]  # smallest score to be in the committee
    certain_cand = [c for c in range(profile.num_cand) if appr_scores[c] > cutoff]
    possible_cand = [c for c in range(profile.num_cand) if appr_scores[c] == cutoff]
    if tiebreaking:
        return [sorted(certain_cand + possible_cand[:committeesize - len(certain_cand)])]
    else:
        return [sorted(certain_cand + list(selection)) for selection in
                itertools.combinations(possible_cand, committeesize - len(certain_cand))]


# Thiele methods
def compute_seq_thiele_methods(profile, committeesize, scorefct_str):
    """Computes the *seq-Phragmen* rule

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    __enough_approved_candiates(profile, committeesize)
    scorefct = __get_scorefct(scorefct_str, committeesize)

    com_scores = {(): 0}

    for _ in range(0, committeesize):  # size of partial committees currently under consideration
        com_scores_next = {}
        for committee, score in com_scores.iteritems():
            additional_score_cand = __additional_thiele_scores(profile, committee, scorefct)
            # marginal utility gained by adding candidate to the committee
            for c in range(profile.num_cand):
                if additional_score_cand[c] >= max(additional_score_cand):
                    com_scores_next[tuple(sorted(committee + (c,)))] = com_scores[committee] + additional_score_cand[c]
        # remove suboptimal committees, leave only the best branching_factor many (subject to ties)
        com_scores = {}
        cutoff = max(com_scores_next.values())
        for com, score in com_scores_next.iteritems():
            if score >= cutoff:
                com_scores[com] = score
    return [set(comm) for comm in com_scores.keys()]


def compute_seq_thiele_methods_with_tiebreaking(profile, committeesize, scorefct_str):
    __enough_approved_candiates(profile, committeesize)
    scorefct = __get_scorefct(scorefct_str, committeesize)

    committee = set()

    for _ in range(0, committeesize):  # size of partial committees currently under consideration
        additional_score_cand = __additional_thiele_scores(profile, committee, scorefct)
        committee.add(additional_score_cand.index(max(additional_score_cand)))
    return [committee]


def compute_seqphragmen(profile, committeesize):
    __enough_approved_candiates(profile, committeesize)

    load = {v: 0 for v in profile.preferences}
    com_loads = {(): load}

    approvers_weight = {}
    for c in range(profile.num_cand):
        approvers_weight[c] = sum(v.weight for v in profile.preferences if c in v.approved)

    for _ in range(0, committeesize):  # size of partial committees currently under consideration
        com_loads_next = {}
        for committee, load in com_loads.iteritems():
            approvers_load = {}
            for c in range(profile.num_cand):
                approvers_load[c] = sum(v.weight * load[v] for v in profile.preferences if c in v.approved)
            new_maxload = [
                mpq(approvers_load[c] + 1, approvers_weight[c]) if approvers_weight[c] > 0 else committeesize + 1 for c
                in range(profile.num_cand)]
            for c in range(profile.num_cand):
                if c in committee:
                    new_maxload[c] = sys.maxint
            for c in range(profile.num_cand):
                if new_maxload[c] <= min(new_maxload):
                    new_load = {}
                    for v in profile.preferences:
                        if c in v.approved:
                            new_load[v] = new_maxload[c]
                        else:
                            new_load[v] = load[v]
                    com_loads_next[tuple(sorted(committee + (c,)))] = new_load
        # remove suboptimal committees
        com_loads = {}
        cutoff = min([max(load) for load in com_loads_next.values()])
        for com, load in com_loads_next.iteritems():
            if max(load) <= cutoff:
                com_loads[com] = load
    return [set(comm) for comm in com_loads.keys()]


def compute_pav(profile, committeesize, ilp=True, tiebreaking=False):
    """Computes the *Proportional Approval Voting (PAV)* rule
    Uses an Integer Linear Programming (ILP) implemention and
    requires Gurobi 7.0+.

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    if ilp:
        return rule_approval_ilp.compute_thiele_methods_ilp(profile, committeesize, 'pav', tiebreaking)
    else:
        return compute_thiele_methods_branchandbound(profile, committeesize, 'pav', tiebreaking)


def compute_cc(profile, committeesize, ilp=True, tiebreaking=False):
    """Computes the *Approval-Based Chamberlin-Courant* rule
    Uses an Integer Linear Programming (ILP) implemention and
    requires Gurobi 7.0+.

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    if ilp:
        return rule_approval_ilp.compute_thiele_methods_ilp(profile, committeesize, 'cc', tiebreaking)
    else:
        return compute_thiele_methods_branchandbound(profile, committeesize, 'cc', tiebreaking)


def compute_varphragmen(profile, committeesize):
    """Computes the *var-Phragmen* rule.
    Uses a Mixed Integer Quadratic Programming (MIQP) implemention and
    requires Gurobi 7.0+.
    This function returns one optimal committees (this is a limitation with the  MIQP solver of Gurobi).

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing one winning committees
    """
    return rule_approval_ilp.compute_optphragmen_ilp(profile, committeesize, "varphrag")


def compute_maxphragmen_unrefined(profile, committeesize):
    """Computes the *unrefined max-Phragmen* rule, i.e., it minimizes only
    the largest voter load and not also lexicographically smaller loads.
    Uses a Mixed Integer Linear Programming (MILP) implemention and
    requires Gurobi 7.0+.
    This function returns some but not necessarily all optimal
    committees (this is a limitation with the  MIQP solver of Gurobi)

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    return rule_approval_ilp.compute_optphragmen_ilp(profile, committeesize, "maxphrag-unrefined")


def compute_maxphragmen_refined(profile, committeesize):
    return rule_approval_ilp.compute_optphragmen_ilp(profile, committeesize, "maxphrag-refined")


def compute_monroe(profile, committeesize):
    """Computes the Monroe rule.
    Uses an Integer Linear Programming (ILP) implemention and
    requires Gurobi 7.0+.

    Args:
       profile (dichProfile):  A dichotomous preference profile

       committeesize (int): Size of the desired output committee

    Returns:
       A list containing all winning committees
    """
    return rule_approval_ilp.compute_monroe_ilp(profile, committeesize)


def compute_cc_extended(profile, committeesize):
    return rule_approval_ilp.compute_cc_extended_ilp(profile, committeesize)


# TODO: implement seq-Monroe

def print_committees(committees, print_max=10):
    if committees is None:
        print("Error: no committees returned")
        return
    if len(committees) == 1:
        print(" 1 committee")
    else:
        if len(committees) > print_max:
            print(" ", len(committees), "committees, printing ", print_max, "of them")
        else:
            print(" ", len(committees), "committees")
    for com in sorted(map(tuple, committees[:print_max])):
        print("    {", ", ".join(map(str, com)), "}")
    print()


def allrules(profile, committeesize, sav=True, without_ilp=True, ejr=False, av=True, rav=True, pav=True, phrag=True,
             cc=True, monroe=True):
    if rav:
        print("RAV (tie-breaking):")
        com = compute_seqpav(profile, committeesize, tiebreaking=True)
        print_committees(com)

        print("RAV:")
        com = compute_seqpav(profile, committeesize)
        print_committees(com)

    if av:
        print("AV:")
        com = compute_av(profile, committeesize)
        print_committees(com)

    if sav:
        print("SAV:")
        com = compute_sav(profile, committeesize)
        print_committees(com)

    if pav:
        print("PAV (all solutions):")
        com = compute_pav(profile, committeesize)
        print_committees(com)

        if without_ilp:
            print("PAV (branch+bound):")
            com = compute_pav(profile, committeesize, ilp=False)
            print_committees(com)

    if phrag:
        print("max-Phragmen without refinement:")
        com = compute_maxphragmen_unrefined(profile, committeesize)
        print_committees(com)

        print("max-Phragmen with refinement:")
        com = compute_maxphragmen_refined(profile, committeesize)
        print_committees(com)

        print("var-Phragmen (one solution):")
        com = compute_varphragmen(profile, committeesize)
        print_committees(com)

        print("seq-Phragmen:")
        com = compute_seqphragmen(profile, committeesize)
        print_committees(com)

    if cc:
        print("Chamberlin-Courant:")
        com = compute_cc(profile, committeesize)
        print_committees(com)

        if without_ilp:
            print("Chamberlin-Courant (branch+bound):")
            com = compute_cc(profile, committeesize, ilp=False)
            print_committees(com)

    if monroe:
        print("Monroe:")
        com = compute_monroe(profile, committeesize)
        print_committees(com)
