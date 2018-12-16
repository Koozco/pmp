"""
CC + kB with ILP
"""
from pmp.rules import MultigoalCCBorda as CCkB
from pmp.preferences import Ordinal, Profile

n = 5
m = 3
k = 2
orders = [
    [1, 2, 0],
    [2, 1, 0],
    [2, 0, 1],
    [1, 2, 0],
    [1, 0, 2]
]

preferences = [Ordinal(o) for o in orders]
candidates = [0, 1, 2]

profile = Profile(candidates, preferences)

cckb = CCkB(9, 8)

committee = cckb.find_committees(k, profile, method='ILP')
print('Selected committees:', list(committee))
