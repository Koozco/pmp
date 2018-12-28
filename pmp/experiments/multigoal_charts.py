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
    candidates = list(range(candidates_number))
    return Profile(candidates, preferences)


def get_best_score(rule, profile, k):
    best_committee = list(rule.find_committee(k, profile))
    return rule.committee_score(best_committee, profile)


def plot(x, y, e, rule1, rule2, title=""):
    axes = plt.gca()
    axes.set_xlim([0, 100])
    plt.xlabel(rule2.__class__.__name__)
    axes.set_ylim([0, y[0] + e[0]])
    plt.ylabel(rule1.__class__.__name__)
    plt.errorbar(x, y, np.zeros(len(e)), linestale=None)
    plt.title(title)


def draw_chart(filename, k, n, m, repetitions, rule1, rule2, multigoal_rule, step=5, log_errors=True):
    x = np.array([a for a in range(70, 101, step)])
    y_samples = np.array([np.zeros(repetitions) for _ in x])

    y = np.zeros(len(x))
    mins = np.zeros(len(x))
    maxs = np.zeros(len(x))
    e = np.zeros(len(x))
    for i, r2 in enumerate(x):
        for j in range(repetitions):
            for r1 in range(100, 0, -step):
                profile = get_profile(n, m)
                rule1_best = get_best_score(rule1, profile, k)
                rule2_best = get_best_score(rule2, profile, k)
                rule1_threshold = rule1_best * r1 / 100
                rule2_threshold = rule2_best * r2 / 100
                rule = multigoal_rule((rule1_threshold, rule2_threshold), log_errors=log_errors)
                try:
                    committee = list(rule.find_committees(k, profile, method='ILP'))
                    y_samples[i][j] = rule.committee_score(committee, profile)[0] / float(rule1_best) * 100
                    break
                except CplexSolverError:
                    continue
        y[i] = np.mean(y_samples[i])
        mins[i] = np.min(y_samples[i])
        maxs[i] = np.max(y_samples[i])
        e[i] = np.std(y_samples[i])
        print("r1: {}% - r2: {}%, r2_min: {}, error: {}".format(r2, y[i], mins[i], e[i]))

    title = "voters: {}, candidates: {}, committee size: {}".format(n, m, k)
    plot(x, y, e, rule1, rule2, title=title)
    plot(x, mins, e, rule1, rule2, title=title)
    plt.savefig(filename)
