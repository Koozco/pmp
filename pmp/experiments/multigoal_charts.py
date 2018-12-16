import matplotlib.pyplot as plt
import numpy as np

from pmp.experiments import generate_uniform
from pmp.experiments.experiment import preference_orders
from pmp.preferences import Profile


def get_profile(voters_number, candidates_number):
    voters = generate_uniform(-3, -3, 3, 3, voters_number, 'None')
    candidates = generate_uniform(-3, -3, 3, 3, candidates_number, 'None')
    preferences = preference_orders(candidates, voters)
    candidates = list(range(0, candidates_number))
    return Profile(candidates, preferences)


def get_best_score(rule, profile, k):
    best_borda = rule.find_committee(k, profile)
    return rule.committee_score(best_borda, profile)


def plot(x, y, e, rule1, rule2, bpc, title=""):
    axes = plt.gca()
    axes.set_xlim([0, 100])
    plt.xlabel(rule2.__class__.__name__)
    axes.set_ylim([0, y[0] + e[0]])
    plt.ylabel(rule1.__class__.__name__)
    # plt.errorbar(x, y, np.zeros(len(e)), linestale=None)
    plt.errorbar(x, y, np.zeros(len(e)), linestale=None)

    plt.plot(bpc[0], bpc[1], 'ro')
    plt.plot([0, bpc[0]], [bpc[1], bpc[1]], linewidth=1, linestyle="--", c="red")
    plt.plot([bpc[0], bpc[0]], [0, bpc[1]], linewidth=1, linestyle="--", c="red")
    plt.title(title)
    plt.show()


def draw_chart(k, n, m, repetitions, rule1, rule2, multigoal_rule):
    best_point_coordinates = (0, 0)
    best_point = 0

    x = np.array([a for a in range(70, 101, 1)])
    y_samples = np.array([np.zeros(repetitions) for _ in x])

    y = np.zeros(len(x))
    mins = np.zeros(len(x))
    e = np.zeros(len(x))
    for i, r2 in enumerate(x):
        for j in range(repetitions):
            prev_committees = []
            prev_rule1_best = 0
            for r1 in x:
                profile = get_profile(m, n)
                rule1_best = get_best_score(rule1, profile, k)
                rule2_best = get_best_score(rule2, profile, k)
                rule1_threshold = rule1_best * r1 / 100
                rule2_threshold = rule2_best * r2 / 100
                rule = multigoal_rule(s1=rule1_threshold, s2=rule2_threshold)
                committees = rule.find_committees(k, profile, method='Bruteforce')
                if not committees:
                    break
                prev_committees = committees
                prev_rule1_best = rule1_best
            prev_committees_scores = [rule.scores[c] for c in prev_committees]
            y_samples[i][j] = sorted(prev_committees_scores, key=lambda s: s[0])[0][0] / prev_rule1_best * 100
        y[i] = np.mean(y_samples[i])
        mins[i] = np.min(y_samples[i])
        e[i] = np.std(y_samples[i])
        if y[i] * x[i] > best_point:
            best_point = y[i] * x[i]
            best_point_coordinates = (x[i], y[i])
        print(r2, "% - ", y[i], "%, min: ", mins[i], ", error: ", e[i])

    title = "voters: {}, candidates: {}, committee size: {}".format(m, n, k)
    plot(x, mins, e, rule1, rule2, best_point_coordinates, title=title)


# import matplotlib.pyplot as plt
# import numpy as np
# import random
#
# from pmp.experiments import generate_uniform
# from pmp.experiments.experiment import preference_orders
# from pmp.preferences import Profile
# from pmp.rules import Borda, Bloc
# from pmp.rules import MultigoalBlocBorda as BB
#
# repetitions = 100
# best_point_coordinates = (0, 0)
# best_point = 0
#
# # Borda thresholds
# x = np.array([a for a in range(0, 101, 5)])
# y_samples = np.array([np.zeros(repetitions) for _ in x])
#
# # CC thresholds
# y = np.zeros(len(x))
# e = np.zeros(len(x))
# for i, s in enumerate(x):
#     for j in range(repetitions):
#         y_samples[i][j] = repetitions * repetitions - s * s + random.uniform(-100., 100.)
#     y[i] = np.mean(y_samples[i])
#     e[i] = np.max(y_samples[i]) - np.min(y_samples[i])
#     if y[i] * s > best_point:
#         best_point = y[i] * x[i]
#         best_point_coordinates = (s, y[i])
#     print(y[i], e[i])
#
#
# axes = plt.gca()
# axes.set_xlim([0, 100])
# plt.xlabel('k-Borda')
# axes.set_ylim([0, y[0] + e[0]])
# plt.ylabel('Chamberlin-Courant')
# plt.errorbar(x, y, e, linestale=None)
#
# plt.plot(best_point_coordinates[0], best_point_coordinates[1], 'ro')
# plt.plot([0, best_point_coordinates[0]], [best_point_coordinates[1], best_point_coordinates[1]], linewidth=1, linestyle="--", c="red")
# plt.plot([best_point_coordinates[0], best_point_coordinates[0]], [0, best_point_coordinates[1]], linewidth=1, linestyle="--", c="red")
#
# plt.show()
#
#
#
#
# k = 2
# voters = generate_uniform(-3, -3, 3, 3, 100, 'None')
# candidates = generate_uniform(-3, -3, 3, 3, 100, 'None')
# preferences = preference_orders(candidates, voters)
# candidates = list(range(0, 100))
# profile = Profile(candidates, preferences)
#
# borda = Borda()
# bloc = Bloc()
# best_borda = borda.find_committee(k, profile)
# best_bloc = bloc.find_committee(k, profile)
# best_borda_score = borda.committee_score(best_borda, profile)
# best_bloc_score = bloc.committee_score(best_bloc, profile)
# print(best_borda, ":", best_borda_score)
# print(best_bloc, ":", best_bloc_score)
#
# bb = BB(bloc_threshold=12, borda_threshold=13)
# committees = bb.find_committees(k, profile, method='Bruteforce')
# print('Points:', bb.scores)
# print('Selected committees:', committees)
