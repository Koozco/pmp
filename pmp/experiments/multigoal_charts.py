import matplotlib.pyplot as plt
import numpy as np
import random

from pmp.experiments import generate_uniform
from pmp.experiments.experiment import preference_orders
from pmp.preferences import Profile
from pmp.rules import Borda, Bloc
from pmp.rules import MultigoalBlocBorda as BB

repetitions = 100
best_point_coordinates = (0, 0)
best_point = 0

# Borda thresholds
x = np.array([a for a in range(0, 101, 5)])
y_samples = np.array([np.zeros(repetitions) for _ in x])

# CC thresholds
y = np.zeros(len(x))
e = np.zeros(len(x))
for i, s in enumerate(x):
    for j in range(repetitions):
        y_samples[i][j] = repetitions * repetitions - s * s + random.uniform(-100., 100.)
    y[i] = np.mean(y_samples[i])
    e[i] = np.max(y_samples[i]) - np.min(y_samples[i])
    if y[i] * s > best_point:
        best_point = y[i] * x[i]
        best_point_coordinates = (s, y[i])
    print(y[i], e[i])


axes = plt.gca()
axes.set_xlim([0, 100])
plt.xlabel('k-Borda')
axes.set_ylim([0, y[0] + e[0]])
plt.ylabel('Chamberlin-Courant')
plt.errorbar(x, y, e, linestale=None)

plt.plot(best_point_coordinates[0], best_point_coordinates[1], 'ro')
plt.plot([0, best_point_coordinates[0]], [best_point_coordinates[1], best_point_coordinates[1]], linewidth=1, linestyle="--", c="red")
plt.plot([best_point_coordinates[0], best_point_coordinates[0]], [0, best_point_coordinates[1]], linewidth=1, linestyle="--", c="red")

plt.show()




k = 2
voters = generate_uniform(-3, -3, 3, 3, 100, 'None')
candidates = generate_uniform(-3, -3, 3, 3, 100, 'None')
preferences = preference_orders(candidates, voters)
candidates = list(range(0, 100))
profile = Profile(candidates, preferences)

borda = Borda()
bloc = Bloc()
best_borda = borda.find_committee(k, profile)
best_bloc = bloc.find_committee(k, profile)
best_borda_score = borda.committee_score(best_borda, profile)
best_bloc_score = bloc.committee_score(best_bloc, profile)
print(best_borda, ":", best_borda_score)
print(best_bloc, ":", best_bloc_score)

bb = BB(bloc_threshold=12, borda_threshold=13)
committees = bb.find_committees(k, profile, method='Bruteforce')
print('Points:', bb.scores)
print('Selected committees:', committees)