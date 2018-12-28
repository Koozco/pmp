# noinspection PyUnresolvedReferences
from pmp.rules import MultigoalCCBorda, MultigoalTBloc
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

# rule = MultigoalCCBorda((8, 8))
rule = MultigoalTBloc((5, 7, 10))

committee = rule.find_committees(k, profile, method='Bruteforce')
print('Points:', rule.scores)
print('Selected committees:', list(committee))
