import matplotlib.pyplot as plt
import numpy as np
import random

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
