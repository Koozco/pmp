# import gurobipy as gb
# import rule_approval
# from profile import Profile
# from preference import DichotomousPreference
#
#
# def compute_thiele_methods_ilp(profile, committeesize, scorefct_str, tiebreaking=False):
#     rule_approval.__enough_approved_candiates(profile, committeesize)
#     scorefct = rule_approval.__get_scorefct(scorefct_str, committeesize)
#
#     m = gb.Model()
#     C = list(range(profile.num_cand))
#
#     # a binary variable indicating whether c is in the committee
#     in_committee = m.addVars(profile.num_cand, vtype=gb.GRB.BINARY, name="in_comm")
#
#     # a (intended binary) variable indicating whether v approves at least l candidates in the committee
#     utility = {}
#     for v in profile.preferences:
#         for l in range(1, committeesize + 1):
#             utility[(v, l)] = m.addVar(ub=1.0)
#
#     # constraint: the committee has the required size
#     m.addConstr(gb.quicksum(in_committee[c] for c in C) == committeesize)
#
#     # constraint: utilities are consistent with actual committee
#     for v in profile.preferences:
#         m.addConstr(gb.quicksum(utility[v, l] for l in range(1, committeesize + 1))
#                     == gb.quicksum(in_committee[c] for c in v.approved))
#
#     # objective: the PAV score of the committee
#     m.setObjective(gb.quicksum(float(scorefct(l)) * v.weight * utility[(v, l)] for v in profile.preferences for l in
#                                range(1, committeesize + 1)), gb.GRB.MAXIMIZE)
#
#     m.setParam('OutputFlag', False)
#
#     if tiebreaking:
#         m.setParam('PoolSearchMode', 0)
#     else:
#         # output all optimal committees
#         m.setParam('PoolSearchMode', 2)
#         m.setParam('PoolSolutions', 11)
#         m.setParam('PoolGap', 0)  # ignore suboptimal committees
#
#     m.optimize()
#
#     if m.Status != 2:
#         print "Warning (" + scorefct_str + "): solutions may ne incomplete or not optimal. (Gurobi return code", m.Status, ")"
#
#     # extract committees from model
#     committees = []
#     for sol in range(m.SolCount):
#         m.setParam('SolutionNumber', sol)
#         committees.append([c for c in C if in_committee[c].Xn >= 0.99])
#
#     if len(committees) > 10:
#         print "Warning (" + scorefct_str + "): more than 10 committees found; returning first 10 (", scorefct_str, ")"
#         committees = committees[:10]
#
#     if tiebreaking:
#         return [committees[0]]
#
#     return committees
#
#
# def compute_optphragmen_ilp(profile, committeesize, variant):
#     # variant in ["maxphrag-refined","maxphrag-unrefined","maxphrag-1sol","varphrag"]
#
#     cands = list(range(profile.num_cand))
#
#     m = gb.Model()
#     m.setParam('OutputFlag', False)
#
#     # a binary variable indicating whether c is in the committee
#     in_committee = m.addVars(profile.num_cand, vtype=gb.GRB.BINARY, name="in_comm")
#
#     load = {}
#     for c in cands:
#         for v in profile.preferences:
#             load[(v, c)] = m.addVar(ub=1.0, lb=0.0)
#
#     # constraint: the committee has the required size
#     m.addConstr(gb.quicksum(in_committee[c] for c in cands) == committeesize)
#
#     for c in cands:
#         for v in profile.preferences:
#             if not c in v.approved:
#                 m.addConstr(load[(v, c)] == 0)
#
#     # a candidate's load is distributed among his approvers
#     for c in cands:
#         m.addConstr(gb.quicksum(v.weight * load[(v, c)] for v in profile.preferences if c in cands) == in_committee[c])
#
#     if variant == "varphrag":
#         loadbound = m.addVar(name="loadbound")
#         m.addConstr(gb.quicksum(
#             [v.weight * load[(v, c1)] * load[(v, c2)] for v in profile.preferences for c1 in v.approved for c2 in
#              v.approved]) <= loadbound)
#         m.setObjective(loadbound, gb.GRB.MINIMIZE)
#     elif variant == "maxphrag-unrefined" or variant == "maxphrag-refined" or variant == "maxphrag-1sol":
#         loadbound = m.addVar(name="loadbound")
#         for v in profile.preferences:
#             m.addConstr(gb.quicksum(load[(v, c)] for c in v.approved) <= loadbound)
#         m.setObjective(loadbound, gb.GRB.MINIMIZE)
#     else:
#         print "Error: Phragmen variant", variant, "not known."
#         return
#
#     if variant == 'varphrag' or variant == "maxphrag-1sol":
#         # output one optimal committees
#         # (solution pools and MIQP is currently not compatible)
#         m.setParam('PoolSearchMode', 0)
#         m.setParam('PoolGap', 0)  # ignore suboptimal committees
#     else:
#         # output all optimal committees
#         m.setParam('PoolSearchMode', 2)
#         m.setParam('PoolSolutions', 11)
#         m.setParam('PoolGap', 0)  # ignore suboptimal committees
#
#     m.optimize()
#
#     if m.Status != 2:
#         print "Warning (" + variant + "): solutions may be incomplete or not optimal. (Gurobi return code", m.Status, ")"
#
#     # extract committees from model
#     committees = []
#     for sol in range(m.SolCount):
#         m.setParam('SolutionNumber', sol)
#         committees.append([c for c in cands if in_committee[c].Xn >= 0.99])
#         #    print "load bounds:", [loadbound[i].Xn for i in range(len(profile.preferences))]
#         # else:
#         #    print "load bound:",loadbound.Xn
#         # print "loads:      ", sorted([sum(load[(v,c)].Xn for c in v.approved) for v in profile.preferences], reverse=True)
#
#     if variant == "maxphrag-refined":
#
#         avscores = [sum(len(set(com) & v.approved) for v in profile.preferences) for com in committees]
#         reduced_committees = []
#         for i in range(len(committees)):
#             if avscores[i] == max(avscores):
#                 reduced_committees.append(committees[i])
#         if len(committees) > 10 and len(reduced_committees) <= 10:
#             print "Warning (" + variant + "): possibly not all optimal committees found"
#         committees = reduced_committees
#
#     if len(committees) > 10:
#         print "Warning (" + variant + "): more than 10 committees found; returning first 10"
#
#         committees = committees[:10]
#
#     if variant == "varphrag":
#         return [committees[0]]
#     else:
#         return committees
#
#
# def compute_monroe_ilp(profile, committeesize):
#     # generate new profile with all weights = 1
#     prof2 = Profile(profile.num_cand)
#     for v in profile:
#         for _ in range(v.weight):
#             prof2.add_preference(DichotomousPreference(v.approved, profile.num_cand))
#     total_weight = profile.voters_num()
#
#     m = gb.Model()
#
#     # optimization goal: variable "satisfaction"
#     satisfaction = m.addVar(vtype=gb.GRB.INTEGER, name="satisfaction")
#
#     # a list of committee members
#     in_committee = m.addVars(profile.num_cand, vtype=gb.GRB.BINARY, name="in_comm")
#     m.addConstr(gb.quicksum(in_committee[c] for c in range(profile.num_cand)) == committeesize)
#
#     # a partition of voters into committeesize many sets
#     partition = m.addVars(profile.num_cand, len(profile.preferences), vtype=gb.GRB.INTEGER, lb=0, name="partition")
#     for i in range(len(profile.preferences)):
#         # every voter has to be part of a voter partition set
#         m.addConstr(gb.quicksum(partition[(j, i)] for j in range(profile.num_cand)) == profile.preferences[i].weight)
#     for i in range(profile.num_cand):
#         # every voter set in the partition has to contain at least int(total_weight/committeesize) candidates
#         m.addConstr(gb.quicksum(partition[(i, j)] for j in range(len(profile.preferences))) >= int(
#             total_weight / committeesize) - total_weight * (1 - in_committee[i]))
#         # if in_committee[i] = 0 then partition[(i,j) = 0
#         m.addConstr(
#             gb.quicksum(partition[(i, j)] for j in range(len(profile.preferences))) <= total_weight * in_committee[i])
#
#     m.update()
#
#     # constraint for objective variable "satisfaction"
#     m.addConstr(gb.quicksum(
#         partition[(i, j)] * (i in profile.preferences[j].approved) for j in range(len(profile.preferences)) for i in
#         range(profile.num_cand)) >= satisfaction)
#
#     # optimization objective
#     m.setObjective(satisfaction, gb.GRB.MAXIMIZE)
#
#     m.setParam('OutputFlag', False)
#
#     # output all optimal committees
#     # m.setParam('PoolSearchMode', 2)
#     # m.setParam('PoolSolutions', 11)
#     # m.setParam('PoolGap',0)  # ignore suboptimal committees
#
#     m.optimize()
#     # m.write("monroe.lp")
#
#     if m.Status != 2:
#         print "Warning (Monroe): solutions may not be optimal. (Gurobi return code", m.Status, ")"
#         return
#
#     opt = satisfaction.x
#
#     com = [c for c in range(profile.num_cand) if in_committee[c].x >= 0.99]
#
#     return [com]
#
# # def compute_cc_extended_ilp(profile, committeesize):
# #     rule_approval.__enough_approved_candiates(profile, committeesize)
# #
# #     m = gb.Model()
# #     C = list(range(profile.num_cand))
# #
# #     # a binary variable indicating whether c is in the committee
# #     in_committee = m.addVars(profile.num_cand, vtype=gb.GRB.BINARY, name="in_comm")
# #
# #     # a (intended binary) variable indicating whether v approves at least l candidates in the committee
# #     utility = {}
# #     for v in profile.preferences:
# #         for l in range(1, committeesize+1):
# #             utility[(v,l)] = m.addVar(ub=1.0)
# #
# #     # constraint: the committee has the required size
# #     m.addConstr(gb.quicksum(in_committee[c] for c in C) == committeesize)
# #
# #     # constraint: utilities are consistent with actual committee
# #     for v in profile.preferences:
# #         m.addConstr(gb.quicksum(utility[v,l] for l in range(1, committeesize+1))
# #                     == gb.quicksum(in_committee[c] for c in v.approved))
# #
# #     m.setParam('OutputFlag', False)
# #
# #     for minappr in range(1,committeesize+1):
# #         # objective: maximize the number of voters with at least minappr approved candidates in the committee
# #         m.setObjective(gb.quicksum(v.weight * utility[(v,minappr)] for v in profile.preferences), gb.GRB.MAXIMIZE)
# #
# #         if minappr > 1:
# #             for v in profile.preferences:
# #                 m.addConstr(utility[(v,minappr-1)] == 1)
# #
# #         m.optimize()
# #
# #         if sum(v.weight * utility[(v,minappr)].X for v in profile.preferences) < profile.gettotalweight():
# #             return [c for c in C if in_committee[c].X >= 0.99]
# #
# #     return [c for c in C if in_committee[c].X >= 0.99]
