"""
You can check available implementations of finding committee without checking actual code
Rules may have different algorithms, eg. brute, approximation, ilp
Like Chamberlin-Courant, having bruteforce and ilp:
"""
from pmp.rules import MultigoalCCBorda as CCB
from pmp.preferences import Ordinal, Profile

# In case of CCB default is ILP
# Let's give a try Bruteforce implementation

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

ccb = CCB(8, 8)

committee = ccb.find_committees(k, profile, method='Bruteforce')
print('Points:', ccb.scores)
print('Selected committees:', committee)
