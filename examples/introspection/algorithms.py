"""
You can check available implementations of finding committee without checking actual code
Rules may have different algorithms, eg. brute, approximation, ilp
Like Chamberlin-Courant, having bruteforce and ilp:
"""
from pmp.rules import ChamberlinCourant as CC
from pmp.preferences import Ordinal, Profile

# Classes of rules with multiple algorithms have static member methods
# Methods contains:
print('Dictionary of all available methods { "method_name": function_reference }')
print(CC.methods.all)
print("\n")

print('Dictionary of optional comments regarding these methods { "method_name": "comment" }')
print(CC.methods.comments)
print("\n")

print('Name of method used in find_committee by default')
print(CC.methods.default)
print("\n")

# In case of CC default is ILP
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

cc = CC()
committee = cc.find_committee(k, profile, method='ILP')
print(committee)
