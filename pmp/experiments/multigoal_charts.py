import matplotlib.pyplot as plt
import numpy as np
from cplex.exceptions import CplexSolverError

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
    best_committee = list(rule.find_committee(k, profile))
    return rule.committee_score(best_committee, profile)


def plot(x, y, e, rule1, rule2, bpc, title=""):
    axes = plt.gca()
    axes.set_xlim([0, 100])
    plt.xlabel(rule2.__class__.__name__)
    axes.set_ylim([0, y[0] + e[0]])
    plt.ylabel(rule1.__class__.__name__)
    plt.errorbar(x, y, np.zeros(len(e)), linestale=None)

    # plt.plot(bpc[0], bpc[1], 'ro')
    # plt.plot([0, bpc[0]], [bpc[1], bpc[1]], linewidth=1, linestyle="--", c="red")
    # plt.plot([bpc[0], bpc[0]], [0, bpc[1]], linewidth=1, linestyle="--", c="red")
    plt.title(title)


def draw_chart(k, n, m, repetitions, rule1, rule2, multigoal_rule):
    best_point_coordinates = (0, 0)
    best_point = 0

    x = np.array([a for a in range(70, 101, 5)])
    y_samples = np.array([np.zeros(repetitions) for _ in x])

    y = np.zeros(len(x))
    mins = np.zeros(len(x))
    e = np.zeros(len(x))
    for i, r2 in enumerate(x):
        for j in range(repetitions):
            for r1 in x:
                profile = get_profile(n, m)
                rule1_best = get_best_score(rule1, profile, k)
                rule2_best = get_best_score(rule2, profile, k)
                rule1_threshold = rule1_best * r1 / 100
                rule2_threshold = rule2_best * r2 / 100
                rule = multigoal_rule(s1=rule1_threshold, s2=rule2_threshold)
                try:
                    committee = tuple(rule.find_committees(k, profile, method='ILP'))
                    y_samples[i][j] = rule.committee_score(committee, profile)[0] / float(rule1_best) * 100
                except CplexSolverError:
                    break
        print(y_samples[i])
        y[i] = np.mean(y_samples[i])
        mins[i] = np.min(y_samples[i])
        e[i] = np.std(y_samples[i])
        if y[i] * x[i] > best_point:
            best_point = y[i] * x[i]
            best_point_coordinates = (x[i], y[i])
        print(r2, "% - ", y[i], "%, min: ", mins[i], ", error: ", e[i])

    title = "voters: {}, candidates: {}, committee size: {}".format(n, m, k)
    plot(x, y, e, rule1, rule2, best_point_coordinates, title=title)
    plot(x, mins, e, rule1, rule2, best_point_coordinates, title=title)
    plt.show()
