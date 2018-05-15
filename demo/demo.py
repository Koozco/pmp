import sys
import os

sys.path.append(os.path.join(".."))

from preferences.ordinal import Ordinal
from preferences.profile import Profile
from rules.borda import Borda
from rules.bloc import Bloc
from rules.sntv import SNTV

k = 3
candidates = [i for i in range(0, 5)]
orders = [
    [3, 1, 4, 0, 2],
    [1, 0, 3, 4, 2],
    [2, 3, 0, 1, 4]
]

preferences = [Ordinal(i) for i in orders]
p = Profile(candidates)

rule = Borda(k)
# rule = Bloc(k)
# rule = SNTV(k)

x = rule.find_committee(p, k, candidates, preferences)
print(x)
