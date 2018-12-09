"""
You can check available implementations of finding committee without checking actual code
Rules may have different algorithms, eg. brute, approximation, ilp
Like Chamberlin-Courant, having bruteforce and ilp:
"""
from pmp.experiments import generate_uniform
from pmp.experiments.experiment import preference_orders
from pmp.rules import MultigoalCCBorda as CCB
from pmp.rules import MultigoalBlocBorda as BB
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

ccb = CCB(cc_threshold=8, borda_threshold=8)

committees = ccb.find_committees(k, profile, method='Bruteforce')
print('Points:', ccb.scores)
print('Selected committees:', committees)


# Borda + Bloc + Bruteforce + uniform distribution of voters and candidates
voters = generate_uniform(-3, -3, 3, 3, 100, 'None')
candidates = generate_uniform(-3, -3, 3, 3, 100, 'None')
preferences = preference_orders(candidates, voters)
candidates = list(range(0, 100))
profile = Profile(candidates, preferences)

bb = BB(bloc_threshold=12, borda_threshold=13)
committees = bb.find_committees(k, profile, method='Bruteforce')
print('Points:', bb.scores)
print('Selected committees:', committees)
