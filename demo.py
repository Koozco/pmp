import os
import sys

sys.path.append(os.path.join(".."))

from pmp.preferences import Ordinal
from pmp.preferences import Profile
from pmp.rules.borda import Borda
from pmp.rules.sntv import SNTV
from pmp.algorithms import greedy
from pmp.rules import lexical_winner

k = 3
candidates = [i for i in range(0, 5)]
orders = [
    [3, 1, 4, 0, 2],
    [1, 0, 3, 4, 2],
    [2, 3, 0, 1, 4],
    [0, 2, 3, 4, 1]
]

preferences = [Ordinal(i) for i in orders]
p = Profile(candidates, preferences=preferences)

# w = WeaklySeparable(3, [2, 1])
# print(w.find_committee(p))
# print(p.scores)
#
# bloc = Bloc(k)
# print(bloc.find_committee(p))
# print(p.scores)

sntv = SNTV(tie_break=lexical_winner)
print(sntv.find_committee(k, p))
print(p.scores)

borda = Borda()
print(borda.find_committee(k, p))
print(p.scores)

new_sntv = greedy(SNTV)
print(new_sntv.find_committee(k, p))
print(p.scores)

new_borda = greedy(Borda)
print(new_borda.find_committee(k, p))
print(p.scores)
