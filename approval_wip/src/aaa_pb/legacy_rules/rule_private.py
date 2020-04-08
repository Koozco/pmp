# private implementations for ongoing research

from core import *
from random import *
from sys import *
from itertools import *
from math import *
from copy import copy
from random import choice
from random import sample
from sets import Set

from rule_proportional import *

#######################################################################

######                                                   #####   #####
#     #    ##    #    #  ######  #    #    ##    ###### #     # #     #
#     #   #  #   ##   #      #   #    #   #  #   #      #       #
######   #    #  # #  #     #    ######  #    #  #####  #       #
#     #  ######  #  # #    #     #    #  ######  #      #       #
#     #  #    #  #   ##   #      #    #  #    #  #      #     # #     #
######   #    #  #    #  ######  #    #  #    #  #       #####   #####


BINOMIALS = {}


def binomial(x, y):
    try:
        #        debug( "BBB %d %d" %(x,y) )
        if (x in BINOMIALS):
            if (y in BINOMIALS[x]):
                return BINOMIALS[x][y]
        else:
            BINOMIALS[x] = {}

        binom = factorial(x) // factorial(y) // factorial(x - y)
        BINOMIALS[x][y] = binom
    except ValueError:
        binom = 1
    return binom


# Banzhaf-CC score for an election where we have
#   m   - number of candidates
#   i   - position of our guy in the vote
#   j   - position of the best committee member fixed in the vote
#   t   - number of committee members already chosen
#   k   - committee size
def BanzhafScorePerVote(m, i, j, t, k):
    if (j < i):
        return 0

    score = 0

    # we want to compute the loop below, but faster

    #  for ell in range(i+1,j):
    #    if( m-(ell+1)-t-1 >= k-1-t-1 ):
    #      score += (ell-i) * binomial(m-(ell+1)-t-1, k-1-t-1)

    ## CASE 1
    ## consider the possibility that among the randomly selected
    ## members of the committee, the best one will be after i but before j
    ## (this should handle all the cases in the first iteration of BanzhafCC)

    # if we can still put two guys in the committee (our new guy, on position i, and
    #  the guy who is supposed to be between position i and position j
    if (k >= t + 2):
        # try all positions (ell) of the guy between positions i and j
        for ell in range(i + 1, j):
            # check if it is possible to have someone on position ell
            #       m-(ell+1)   = number of positions behind position ell
            #   A = m-(ell+1)-t = number of positions behind position ell that are free to be taken
            #   B = k-t-2       = number of committee members that still have to be placed
            #
            #   if A >= B then we can place a committee member on position i, then on position ell, and
            #             then place the remaining k-t-2 guys on the positions behind
            if (m - (ell + 1) - t >= k - t - 2):
                score += (ell - i) * binomial(m - (ell + 1) - t, k - t - 2)

    # B = binomial(m-(j+1)-t-1, k-1-t-1)
    # for ell in range(j-1,i,-1):
    #   if( m-(ell+1)-t-1 > k-1-t-1 ):
    #     B = B * (m-(ell+1)-t-1) / (m-(ell+1)-k+1)
    #     score += (ell-i) * B
    #   elif( m-(ell+1)-t-1 == k-1-t-1 ):
    #     score += (ell-i)

    ## CASE 2
    ## Consider the possibility that all the additional randomly chosen
    ## committee members are ranked behind j (this never happens when j=m,
    ## because then there is no "j" to be ranked behind)

    # if the j'th position is real (and not j = m, which is a placeholder for 'not selected anyone yet')
    if (j < m):
        #  m-(j+1)             = number of positions behind j
        #  A = m-(j+1) - (t-1) = number of positions behind j, not taken by already
        #                        selected guy (we subtract t-1 because position j
        #                        already is taken by a selected committee member)
        #  B =k-t-1            = number of committee members to be still placed
        #                        (not counting our guy from position i)
        #  if A >= B then we can place committee members behind j, but
        #  we get points only if position i is ahead of j
        if (m - (j + 1) - (t - 1) >= k - 1 - t):
            if (i < j):
                score += (j - i) * binomial(m - (j + 1) - (t - 1), k - 1 - t)
    # if there is no other committee member yet placed, but k=1
    # then the candidate simply bets Borda score (for k>=2 and j=m, CASE 1 takes
    # care of the score)
    elif (k == 1):
        score = m - i - 1

    return score


def BanzhafCC(V, k):
    debug("BanzhafCC")

    m = len(V[0])
    n = len(V)
    C = range(m)
    S = convertProfile(V)
    N = [0] * n
    B = [m] * n
    W = []

    # compute each additional member of the committee
    print >> sys.stderr, "BanzhafCC computing"
    for i in range(k):
        debug("Banzhaf CC " + str(i))
        best_score = -1
        best_candidate_set = []
        for c in C:
            score = 0
            sss = str(c) + " : "
            for voter in range(n):
                d = BanzhafScorePerVote(m, S[voter][c], B[voter], i, k)
                score += d
            #      debug( str(c) + " -> score " + str(score) )

            if (score > best_score):
                best_score = score
                best_candidate_set = [c]
            elif (score == best_score):
                best_candidate_set += [c]

        best_candidate = choice(best_candidate_set)
        print >> sys.stderr, best_candidate_set

        W += [best_candidate]
        C.remove(best_candidate)
        B = [min(S[i][best_candidate], B[i]) for i in range(n)]
    #    debug( "B = " + str(B) )
    return W


#######################################################################

                                                  ####### #     #    #
#   ####   #####   ######  ######  #####    #   # #     # #  #  #   # #
#  #    #  #    #  #       #       #    #    # #  #     # #  #  #  #   #
#  #       #    #  #####   #####   #    #     #   #     # #  #  # #     #
#  #  ###  #####   #       #       #    #     #   #     # #  #  # #######
#  #    #  #   #   #       #       #    #     #   #     # #  #  # #     #
#   ####   #    #  ######  ######  #####      #   #######  ## ##  #     #


# comput the score of committee S under OWA x score
def owaScore(S, pos_per_cand_in_vote, OWA, score):
    s = 0.0
    t = 0
    pos = sorted([pos_per_cand_in_vote[c] for c in S])
    for p in pos:
        s += score[p] * OWA[t]
        t += 1
    return s


def owaScoreProfile(S, pos_per_cand, OWA, score):
    return sum([owaScore(S, pos_per_cand_in_vote, OWA, score) for pos_per_cand_in_vote in pos_per_cand])


def posPerCandVote(v):
    m = len(v)
    res = range(m)
    for i in range(m):
        res[v[i]] = i
    return res


def posPerCand(V):
    return [posPerCandVote(v) for v in V]


def greedyOWA(V, k, OWA, score):
    debug("greedyOWA")

    m = len(V[0])
    n = len(V)
    C = range(m)
    W = []
    pos_per_cand = posPerCand(V)

    # compute each additional member of the committee
    print >> sys.stderr, "OWA computing"
    print >> sys.stderr, "OWA =", OWA
    for i in range(k):
        print >> sys.stderr, "Greedy OWA ", i
        best_score = -1
        best_candidate_set = []
        for i in C:
            s = owaScoreProfile(W + [i], pos_per_cand, OWA, score)
            #      debug( str(i)+" --> "+str(s) )
            if (s > best_score):
                best_score = s
                best_candidate_set = [i]
            elif (s == best_score):
                best_candidate_set += [i]

        best_candidate = choice(best_candidate_set)

        W += [best_candidate]
        C.remove(best_candidate)
    return W


def reverseGreedyOWA(V, k, OWA, score):
    debug("greedyOWA")

    m = len(V[0])
    n = len(V)
    W = range(m)
    pos_per_cand = posPerCand(V)

    # compute each additional member of the committee
    debug("reverseGreedyOWA computing")
    debug("OWA =" + str(OWA))
    for i in range(m - k):
        print >> sys.stderr, "reverseGreedy OWA ", i
        best_score = -1
        best_remove_set = []
        testOWA = OWA + [0] * (len(W) - k - 1)

        for i in range(len(W)):
            testW = W[:i] + W[i + 1:]
            s = owaScoreProfile(testW, pos_per_cand, testOWA, score)
            if (s > best_score):
                best_score = s
                best_remove_set = [W[i]]
            elif (s == best_score):
                best_remove_set += [W[i]]

        best_remove = choice(best_remove_set)

        W.remove(best_remove)
    return W


def owaPropExtension(OWA, size):
    # extend OWA operator to be of length size by
    # repeating entries sufficiently many times
    newOWA = []
    for i in range(len(OWA)):
        add = size / (len(OWA) - i)
        newOWA += [OWA[i]] * add
        size -= add
    return newOWA


def reverseGreedyOWA_ext(V, k, OWA, score, owa_ext_function):
    debug("greedyOWA")

    m = len(V[0])
    n = len(V)
    W = range(m)
    pos_per_cand = posPerCand(V)

    # compute each additional member of the committee
    debug("reverseGreedyOWA computing")
    debug("OWA =" + str(OWA))
    for i in range(m - k):
        best_score = -1
        best_remove_set = []
        testOWA = owa_ext_function(OWA, len(W))
        debug("reverseGreedy OWA " + str(i))
        debug(testOWA)

        for i in range(len(W)):
            testW = W[:i] + W[i + 1:]
            s = owaScoreProfile(testW, pos_per_cand, testOWA, score)
            if (s > best_score):
                best_score = s
                best_remove_set = [W[i]]
            elif (s == best_score):
                best_remove_set += [W[i]]

        best_remove = choice(best_remove_set)

        W.remove(best_remove)
    return W


def greedyOWA_take_two(V, k, OWA, score):
    debug("greedyOWA")

    m = len(V[0])
    n = len(V)
    C = range(m)
    W = []
    pos_per_cand = posPerCand(V)

    debug("greedyOWA-take-two")
    if (k % 2 != 0):
        debug("Odd committee size---switching to regular greedyOWA")
        return greedyOWA(V, k, OWA, score)

    # compute each additional member of the committee
    print >> sys.stderr, "OWA computing"
    print >> sys.stderr, "OWA =", OWA
    for i in range(k / 2):
        print >> sys.stderr, "Greedy OWA ", i
        best_score = -1
        best_candidate_set = []
        for ci in range(len(C)):
            for cj in range(ci + 1, len(C)):
                i = C[ci]
                j = C[cj]
                #    for i in C:
                #     for j in C:
                #      if( i >= j ):
                #        continue
                s = owaScoreProfile(W + [i, j], pos_per_cand, OWA, score)
                #      debug( str(i)+" --> "+str(s) )
                if (s > best_score):
                    best_score = s
                    best_candidate_set = [(i, j)]
                elif (s == best_score):
                    best_candidate_set += [(i, j)]

        (best_1, best_2) = choice(best_candidate_set)

        W += [best_1, best_2]
        C.remove(best_1)
        C.remove(best_2)
    return W


def greedyOWA_borda(V, k, OWA):
    m = len(V[0])
    return greedyOWA(V, k, OWA, [m - i - 1 for i in range(m)])


def reverseGreedyOWA_borda(V, k, OWA):
    m = len(V[0])
    return reverseGreedyOWA(V, k, OWA, [m - i - 1 for i in range(m)])


def reverseGreedyOWA_borda_prop(V, k, OWA):
    m = len(V[0])
    return reverseGreedyOWA_ext(V, k, OWA, [m - i - 1 for i in range(m)], owaPropExtension)


def greedyOWA_kborda(V, k):
    m = len(V[0])
    return greedyOWA(V, k, [1] * k, [m - i - 1 for i in range(m)])


def greedyOWA_cc(V, k):
    m = len(V[0])
    return greedyOWA(V, k, [1] + [0] * (k - 1), [m - i - 1 for i in range(m)])


def greedyOWA_topkcc(V, k):
    m = len(V[0])
    return greedyOWA(V, k, [1] + [0] * (k - 1), ([1] * k) + ([0] * (m - k)))


def greedyOWA_cc_take_two(V, k):
    m = len(V[0])
    return greedyOWA_take_two(V, k, [1] + [0] * (k - 1), [m - i - 1 for i in range(m)])


def greedyOWA_topkPAV_take_two(V, k):
    m = len(V[0])
    return greedyOWA_take_two(V, k, [1.0 / (i + 1) for i in range(k)], ([1] * k) + ([0] * (m - k)))


def greedyOWA_bordaPAV(V, k):
    m = len(V[0])
    #  return greedyOWA( V, k, [1.0/(i+1) for i in range(k)], [m-i-1 for i in range(m)] )
    return greedyOWA(V, k, [1.0 / (i + 1) for i in range(k)], [m - i - 1 for i in range(m)])


def greedyOWA_topkPAV(V, k):
    m = len(V[0])
    return greedyOWA(V, k, [1.0 / (i + 1) for i in range(k)], ([1] * k) + ([0] * (m - k)))


##################################################################################
#########     METHODS WITH RUNOFFS         #######################################
##################################################################################

def kBordaCCRunnof(V, k, k1):
    m = len(V[0])
    S = kborda(V, (m * k1) / 100)
    ind = dict(zip(S, range(len(S))))
    V_new = [[ind[c] for c in v if ind.has_key(c)] for v in V]
    S2 = greedyCC(V, k)
    return [k for (k, v) in ind.iteritems() if v in S2]


for t in range(10, 100, 10):
    text = "kBorda_%d_CCRunnof = lambda x,y: kBordaCCRunnof( x, y, %d )" % (t, t)
    exec (text)


##################################################################################

######                                                  ####### #     #    #
#     #    ##    #    #  ######  #    #    ##    ###### #     # #  #  #   # #
#     #   #  #   ##   #      #   #    #   #  #   #      #     # #  #  #  #   #
######   #    #  # #  #     #    ######  #    #  #####  #     # #  #  # #     #
#     #  ######  #  # #    #     #    #  ######  #      #     # #  #  # #######
#     #  #    #  #   ##   #      #    #  #    #  #      #     # #  #  # #     #
######   #    #  #    #  ######  #    #  #    #  #      #######  ## ##  #     #


# compute the banzhaf value of c (assuming S is already in, k is the committee size)
def BanzhafOWAScore(k, c, S, v, pos, OWA, score):
    m = len(v)
    f = len(S)  # number of candidates fixed in the committee
    #  pos = {}   # position of the candidate
    Worse = []  # set of candidates on positions worse or equal to c

    DELTA = 0  # marginal contribution of c

    # compute fixed committee members ranked below c (also including c)
    for s in S:
        if pos[s] > pos[c]:
            Worse += [s]
    Worse += [c]

    #  debug( "--------------------")
    #  debug( "VOTE = " + str(v) )
    #  debug( "S = " + str(S) )
    #  debug( "WORSE("+str(c)+") = " + str(Worse) )

    # consider each candidate ranked below c
    for i in range(pos[c], m):
        s = v[i]
        before = sum(
            [int(pos[x] < pos[s]) for x in S])  # number of candidates from S ranked before of s (not inluding c)
        after = sum([int(pos[x] > pos[s]) for x in S])  # number of candidates from S ranked after s

        #    debug( "--------------------")
        #    debug( "VOTE = " + str(v) )
        #    debug( "S = " + str(S) )
        #    debug( "WORSE("+str(c)+") = " + str(Worse) )
        #    debug( "s = " + str(s) )
        #    debug( "before = " + str(before) + "   after = " + str(after) )

        if (s != c):
            before += 1  # include c among the candidates before s

        pos_before = pos[s] - before  # number of free positions before s
        pos_after = (m - pos[s] - 1) - after  # number of free positions after s

        # iterate over the number of committee members ranked before s
        for t in range(before, k):

            # if we know that gain would be 0 anyway
            if (s != c and OWA[t] == OWA[t - 1]):
                continue

            t_after = k - (t + 1)  # number of guys to be placed after

            # if it is imspossible to have t guys ahaead of s then skip
            if (t - before > pos_before):
                continue

                # if there is not enough committee members to be put after, then skip
            if (t_after < after):
                continue
            # if there is not enough positions after then skip
            if (t_after - after > pos_after):
                continue

            # compute the number of coalitions that have t guys before, t_after guys after
            C = binomial(pos_before, t - before) * binomial(pos_after, t_after - after)

            # compute the gain s has
            if (s == c):
                gain = OWA[t] * score[pos[s]]
            else:
                gain = -OWA[t - 1] * score[pos[s]] + OWA[t] * score[pos[s]]

            #      debug("DEBUG gain = %d, C = %d" % (gain,C))

            DELTA += gain * C

    return DELTA


def BanzhafOWAScoreProfile(k, c, S, V, POS, OWA, score):
    return sum([BanzhafOWAScore(k, c, S, V[i], POS[i], OWA, score) for i in range(len(V))])


def BanzhafOWA(V, k, OWA, score):
    debug("BanzhafOWA")

    m = len(V[0])
    n = len(V)
    C = range(m)
    W = []

    # compute profile of positions
    POS = convertProfile(V)

    # compute each additional member of the committee
    debug("Banzhaf OWA computing")
    debug("OWA = " + str(OWA))
    for i in range(k):
        debug("Banzhaf OWA %d" % i)
        prev_score = -1
        best_score = -1
        prev = []
        best_candidate_set = []
        for i in C:
            s = BanzhafOWAScoreProfile(k, i, W, V, POS, OWA, score)
            #      debug( str(i)+" --> score "+str(s) )
            if (s > best_score):
                prev_score = best_score
                prev = best_candidate_set
                best_score = s
                best_candidate_set = [i]
            elif (s == best_score):
                best_candidate_set += [i]

        best_candidate = choice(best_candidate_set)
        print >> sys.stderr, best_candidate_set
        print >> sys.stderr, [best_score, prev_score, prev]

        W += [best_candidate]
        C.remove(best_candidate)
    return W


def BanzhafOWA_borda(V, k, OWA):
    m = len(V[0])
    return BanzhafOWA(V, k, OWA, [m - i - 1 for i in range(m)])


def BanzhafOWA_kborda(V, k):
    m = len(V[0])
    return BanzhafOWA(V, k, [1] * k, [m - i - 1 for i in range(m)])


def BanzhafOWA_cc(V, k):
    m = len(V[0])
    return BanzhafOWA(V, k, [1] + [0] * (k - 1), [m - i - 1 for i in range(m)])


def BanzhafOWA_topkcc(V, k):
    m = len(V[0])
    return BanzhafOWA(V, k, [1] + [0] * (k - 1), ([1] * k) + ([0] * (m - k)))


# def BanzhafOWA_best3( V, k ):
#  m = len( V[0] )
#  return BanzhafOWA( V, k, ([1]*3)+([0]*(k-3)), [m-i-1 for i in range(m)] ) 

for t in range(1, 20):
    text = "Banzhaf_best_%d_borda = lambda x,y: BanzhafOWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (t, t, t)
    exec (text)


def BanzhafOWA_bordaPAV(V, k):
    m = len(V[0])
    #  return greedyOWA( V, k, [1.0/(i+1) for i in range(k)], [m-i-1 for i in range(m)] )
    return BanzhafOWA(V, k, [1.0 / (i + 1) for i in range(k)], [m - i - 1 for i in range(m)])


def BanzhafOWA_bordaPAV3(V, k):
    m = len(V[0])
    #  return greedyOWA( V, k, [1.0/(i+1) for i in range(k)], [m-i-1 for i in range(m)] )
    return BanzhafOWA(V, k, [1.0 / ((i + 1) ** 3) for i in range(k)], [m - i - 1 for i in range(m)])


def BanzhafOWA_topkPAV(V, k):
    m = len(V[0])
    return BanzhafOWA(V, k, [1.0 / (i + 1) for i in range(k)], ([1] * k) + ([0] * (m - k)))


##################################################################################

######  #       #               #####           #####   #    #  #       ######
#       #       #               #    #          #    #  #    #  #       #
#####   #       #               #    #  #####   #    #  #    #  #       #####
#       #       #               #####           #####   #    #  #       #
#       #       #               #               #   #   #    #  #       #
######  ######  ###### #######  #               #    #   ####   ######  ######


def ellpScoreProfile(P, N, c, m, scoring_vector, p):
    n = len(P)
    S = [(N[i] + (scoring_vector[P[i][c]]) ** p) ** (1.0 / p) for i in range(n)]

    return float(sum(S))


# scoring_vector - m-dimensial scoring protocol to use
# p              - the exponent to use
def greedyEllpRule(V, k, scoring_vector, p):
    debug("greedyEllpRule")

    m = len(V[0])
    n = len(V)
    C = range(m)
    S = convertProfile(V)
    W = []
    N = [0] * n  # scores of the committee so far

    debug("n = %d, m = %d" % (n, m))

    # compute each additional member of the committee
    for i in range(k):
        best_score = -1
        best_candidate_set = []
        for i in C:
            s = ellpScoreProfile(S, N, i, m, scoring_vector, p)
            if (s > best_score):
                best_score = s
                best_candidate_set = [i]
            elif (s == best_score):
                best_candidate_set += [i]

        debug("BEST CANDs = %d " % len(best_candidate_set))
        best_candidate = choice(best_candidate_set)
        W += [best_candidate]
        C.remove(best_candidate)
        for i in range(n):
            N[i] += (scoring_vector[S[i][best_candidate]]) ** p
        sssum = sum(N)
        debug("sum = %d" % sssum)
    return W


def greedyEllpBorda(V, k, p):
    m = len(V[0])
    return greedyEllpRule(V, k, [m - i - 1 for i in range(m)], p)


def greedyEllpBloc(V, k, p):
    m = len(V[0])
    return greedyEllpRule(V, k, ([1] * k) + ([0] * (m - k)), p)


def kborda_score(V, W):
    m = len(V[0])
    s = 0
    for v in V:
        for i in range(m):
            if (v[i] in W):
                s += m - i - 1
    return s


def cc_score(V, W):
    m = len(V[0])
    s = 0
    for v in V:
        for i in range(m):
            if (v[i] in W):
                s += m - i - 1
                break
    return s


def ellpborda_score(V, W, p):
    m = len(V[0])
    s = 0
    for v in V:
        ls = 0.0
        for i in range(m):
            if (v[i] in W):
                ls += (m - i - 1) ** p
        s += ls ** (1.0 / p)
    return s


def metropolis(V, k, score):
    m = len(V[0])
    n = len(V)
    C = range(m)
    best = 0
    bestW = []

    debug("Metropolis!")

    STEPS = 1500
    accept = 0.01

    W = sample(C, k)
    notW = {}
    for c in C:
        notW[c] = 1
    for c in W:
        del notW[c]

    bestW = W
    best = score(V, W)
    current = best

    debug("score = %d" % best)

    for step in range(STEPS):
        i = choice(range(k))
        newW = W[:i] + [choice(notW.keys())] + W[i + 1:]
        s = score(V, newW)

        if (s > best):
            (best, bestW) = (s, newW)

        if (s > current):
            W = newW
            current = s
        elif (random() < accept):
            W = newW
            current = s

        debug("%d %d (%d)" % (step, best, current))

    return bestW


def ell_p_metropolis(V, k, p):
    m = len(V[0])
    n = len(V)
    C = range(m)

    S = convertProfile(V)
    N = [0] * n  # scores of the committee so far

    best = 0
    bestW = []

    debug("Metropolis!")

    #  STEPS  = 10000
    #  accept = 0.001

    STEPS = 2001
    accept = 0.02

    W = sample(C, k)
    notW = {}
    for c in C:
        notW[c] = 1
    for c in W:
        del notW[c]

        # compute the score and N
    best = 0
    for i in range(n):
        for c in W:
            N[i] += (m - S[i][c] - 1) ** p
        best += N[i] ** (1.0 / p)

    bestW = W
    current = best

    debug("score = %d" % best)

    for step in range(STEPS):

        accept *= 0.999

        i = choice(range(k))
        c = W[i]
        new_c = choice(notW.keys())
        newW = W[:i] + [new_c] + W[i + 1:]

        # specific computation of ell_p-Borda score
        s = 0
        NN = [0] * n
        for i in range(n):
            NN[i] = N[i] - (m - S[i][c] - 1) ** p + (m - S[i][new_c] - 1) ** p
            s += NN[i] ** (1.0 / p)

        if (s > best):
            (best, bestW) = (s, newW)

        if (s > current) or (random() < accept):
            W = newW
            current = s
            N = NN
            notW[c] = 1
            del notW[new_c]

        if step % 1000 == 0:
            debug("%d %d (%d)  accept = %f" % (step, best, current, accept))

    return bestW


# running several tries of the Metropolis algorithm
def ell_p_manyMetropolis(V, k, p):
    TRIES = 3
    bestW = []
    best = 0

    for i in range(TRIES):
        W = ell_p_metropolis(V, k, p)
        s = ellpborda_score(V, W, p)
        if (s > best):
            (best, bestW) = (s, W)

    debug("#### METROPOLIS BEST = %d" % best)
    return W


def owa_metropolis(V, k, OWA, score):
    m = len(V[0])
    n = len(V)
    C = range(m)
    pos_per_cand = posPerCand(V)

    best = 0
    bestW = []

    debug("OWA Metropolis!")

    #  STEPS  = 10000
    #  accept = 0.001

    STEPS = 10001
    accept = 0.02

    W = sample(C, k)
    notW = {}
    for c in C:
        notW[c] = 1
    for c in W:
        del notW[c]

        # compute the score of W
    best = owaScoreProfile(W, pos_per_cand, OWA, score)
    bestW = W
    current = best

    debug("score = %d" % best)

    for step in range(STEPS):

        accept *= 0.9995

        i = choice(range(k))
        c = W[i]
        new_c = choice(notW.keys())
        newW = W[:i] + [new_c] + W[i + 1:]

        # specific computation of ell_p-Borda score
        s = owaScoreProfile(newW, pos_per_cand, OWA, score)

        if (s > best):
            (best, bestW) = (s, newW)

        if (s > current) or (random() < accept):
            W = newW
            current = s
            notW[c] = 1
            del notW[new_c]

        if step % 1000 == 0:
            debug("%d %d (%d)  accept = %f" % (step, best, current, accept))

    return bestW


# running several tries of the Metropolis algorithm
def owa_manyMetropolis(V, k, OWA, score):
    TRIES = 4
    bestW = []
    best = 0
    pos_per_cand = posPerCand(V)

    for i in range(TRIES):
        W = owa_metropolis(V, k, OWA, score)
        s = owaScoreProfile(W, pos_per_cand, OWA, score)
        if (s > best):
            (best, bestW) = (s, W)

    debug("#### METROPOLIS BEST = %f" % best)
    return W


def metropolis_OWA_borda(V, k, OWA):
    m = len(V[0])
    return owa_manyMetropolis(V, k, OWA, [m - i - 1 for i in range(m)])


def metropolis_topkPAV(V, k):
    m = len(V[0])
    return owa_manyMetropolis(V, k, [1.0 / (i + 1) for i in range(k)], ([1] * k) + ([0] * (m - k)))


# compute OWA rule with ILP
def OWA_borda(V, k, OWA):
    m = len(V[0])
    n = len(V)

    print >> sys.stderr, "in PAV for real"
    # call ILP..
    print >> sys.stderr, "CPLEX START"
    (total_satisfaction, winning_committee) = ilp.run_ilp_OWA(np.array(V), k, OWA, np.arange(m - 1, -1, -1))
    print >> sys.stderr, "winning_committee"
    print >> sys.stderr, winning_committee
    debug('well')
    debug(list(winning_committee))
    print >> sys.stderr, "CPLEX END"
    return list(winning_committee)


# compute OWA rule with ILP
def OWA_borda_egal(V, k, OWA):
    m = len(V[0])
    n = len(V)

    print >> sys.stderr, "in OWA_borda_egal for real"
    # call ILP..
    print >> sys.stderr, "CPLEX START"
    (total_satisfaction, winning_committee) = ilp.run_ilp_OWA_egal(np.array(V), k, OWA, np.arange(m - 1, -1, -1))
    print >> sys.stderr, "winning_committee"
    print >> sys.stderr, winning_committee
    debug('well')
    debug(list(winning_committee))
    print >> sys.stderr, "CPLEX END"
    return list(winning_committee)


# compute CC-egal rule with ILP
def CCegal(V, k):
    m = len(V[0])
    n = len(V)

    print >> sys.stderr, "in CCegal for real"
    # call ILP..
    print >> sys.stderr, "CPLEX START"
    (total_satisfaction, winning_committee) = ilp.run_ilp_CC_egal(np.array(V), k, np.arange(m - 1, -1, -1))
    print >> sys.stderr, "winning_committee"
    print >> sys.stderr, winning_committee
    debug('well')
    debug(list(winning_committee))
    print >> sys.stderr, "CPLEX END"
    return list(winning_committee)


# MAIN


# define the greedy ell_p rules 
for i in range(200):
    text = "greedyEll%d_Borda = lambda x,y: greedyEllpBorda( x, y, %d.0 )" % (i, i)
    exec (text)

for i in range(200):
    text = "greedyEll%d_Bloc = lambda x,y: greedyEllpBloc( x, y, %d.0 )" % (i, i)
    exec (text)

# the same for metropolis
for i in range(200):
    text = "metropEll%d_Borda = lambda x,y: ell_p_manyMetropolis( x, y, %d.0 )" % (i, i)
    exec (text)

# define best_t OWA rules
for i in range(1, 50):
    text = "Banzhaf_best_%d_borda = lambda x,y: BanzhafOWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

for i in range(1, 50):
    text = "greedy_best_%d_borda = lambda x,y: greedyOWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

for i in range(1, 50):
    text = "reverse_best_%d_borda = lambda x,y: reverseGreedyOWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

for i in range(1, 50):
    text = "prop_reverse_best_%d_borda = lambda x,y: reverseGreedyOWA_borda_prop( x, y, ([1]*%d)+([0]*(y-%d)) )" % (
    i, i, i)
    exec (text)

for i in range(1, 50):
    text = "metropolis_best_%d_borda = lambda x,y: metropolis_OWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

for i in range(1, 50):
    text = "OWA_best_%d_borda = lambda x,y: OWA_borda( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

for i in range(1, 50):
    text = "OWA_best_%d_borda_egal = lambda x,y: OWA_borda_egal( x, y, ([1]*%d)+([0]*(y-%d)) )" % (i, i, i)
    exec (text)

# define OWA-PAV-powers Borda rules

for t in range(1, 50):
    text = "PAV_power_%d_borda = lambda x,y: OWA_borda( x, y, [1.0/((i+1)**(%d)) for i in range(y)] )" % (t, t)
    exec (text)
    text = "greedy_PAV_power_%d_borda = lambda x,y: greedyOWA_borda( x, y, [1.0/((i+1)**(%d)) for i in range(y)] )" % (
    t, t)
    exec (text)
    text = "metropolis_PAV_power_%d_borda = lambda x,y: metropolis_OWA_borda( x, y, [1.0/((i+1)**(%d)) for i in range(y)] )" % (
    t, t)
    exec (text)

    text = "PAV_rev_power_%d_borda = lambda x,y: OWA_borda( x, y, [1.0/((i+1)**(1.0/%d)) for i in range(y)] )" % (t, t)
    exec (text)
    text = "greedy_PAV_rev_power_%d_borda = lambda x,y: greedyOWA_borda( x, y, [1.0/((i+1)**(1.0/%d)) for i in range(y)] )" % (
    t, t)
    exec (text)
    text = "metropolis_PAV_rev_power_%d_borda = lambda x,y: metropolis_OWA_borda( x, y, [1.0/((i+1)**(1.0/(%d/5))) for i in range(y)] )" % (
    t, t)
    exec (text)

for t in range(1, 20):
    text = "greedy_PAV_power_%d_10_borda = lambda x,y: greedyOWA_borda( x, y, [1.0/((i+1)**(float(%d)/10)) for i in range(y)] )" % (
    t, t)
    exec (text)


######   ####     ##    #        #   #####    ##    #####      #      ##     #    #
#       #    #   #  #   #        #     #     #  #   #    #     #     #  #    ##   #
#####   #       #    #  #        #     #    #    #  #    #     #    #    #   # #  #
#       #  ###  ######  #        #     #    ######  #####      #    ######   #  # #
#       #    #  #    #  #        #     #    #    #  #   #      #    #    #   #   ##
######   ####   #    #  ######   #     #    #    #  #    #     #    #    #   #    #


def reverseEgalCC(V, k):
    m = len(V[0])
    n = len(V)

    debug("reverseEgalCC")

    worst_pos = [0] * m

    # compute worst positions of the candidates
    for v in V:
        for p in range(m):
            c = v[p]
            worst_pos[c] = max(worst_pos[c], p)

    #  for c in range(m):
    #    debug( "worst_pos[%d] = %d" % (c, worst_pos[c]) )

    # compute possible winning committees
    S = []
    score = 0
    for s in range(m):
        for c in range(m):
            if (worst_pos[c] == s):
                S += [c]
        if (len(S) >= k):
            score = s
            break

    debug("score = %d   -->   committee size = %d" % (score, len(S)))

    return sample(S, k)
