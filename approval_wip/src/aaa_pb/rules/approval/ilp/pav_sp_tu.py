from typing import List

import aaa_pb.rules.approval.ilp._cplex_helpers
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


class PAV_SinglePeaked_ILP(ApprovalBasedRuleBase):
    #
    # Based on
    # """
    # Single-Peakedness and Total Unimodularity
    # New Polynomial-Time Algorithms for Multi-Winner Election
    #
    # Dominik Peters
    # """
    #
    #

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        number_of_voters = len(V)
        pav_coefficients = [1.0 / i for i in range(1, k + 1)]

        def get_x_il_name(v, l):
            # type: (int, int) -> str
            # Voter v approves at least l candidates
            return "x_i{0}_l{1}".format(v, l)

        def get_y_c_name(c):
            # type: (int) -> str
            # Candidate c is in the winning committee
            return "y_c{0}".format(c)

        def get_y_c_name_inverse(name):
            # type: (str) -> int
            return int(name[3:])

        import cplex
        from aaa_pb.rules.approval.ilp._cplex_helpers import add_boolean_variable

        problem = cplex.Cplex()
        problem.objective.set_sense(problem.objective.sense.maximize)

        # 0 <= x_il <= 1
        # x_il == 1 implies voter i approves at least l in the committee
        #
        # Objective:
        # Maximize
        # SUM[from i:=0 to n](
        #   SUM[from l:=0 to k](alpha_l * x_il)
        # )
        #
        # where
        #   alpha_l is pav_coefficients[l]
        for v in range(number_of_voters):
            for l in range(k):
                add_boolean_variable(
                    problem=problem,
                    name=get_x_il_name(v=v, l=l),
                    obj=pav_coefficients[l]
                )

        # 0 <= y_c <= 1
        # y_c == 0 implies candidate c is in the winning committee
        for c in range(number_of_candidates):
            add_boolean_variable(
                problem=problem,
                name=get_y_c_name(c),
                obj=0.0
            )

        # (2)
        # SUM[from c:=0 to number_of_candidates](y_c) == k
        # Winning committee has size k
        #
        y_c_names = [get_y_c_name(c) for c in range(number_of_candidates)]
        problem.linear_constraints.add(
            lin_expr=[
                [
                    y_c_names,
                    [1.0] * number_of_candidates
                ]
            ],
            senses=["E"],
            rhs=[k],
            names=["(2)"]
        )

        # (3)
        # SUM[from l:=0 to k](x_il) <= SUM[for c approved by voter i](y_c)
        # A voter approves at least l candidates.
        #
        # Right hand side evaluates to the number of candidates present in the committee supported by the voter.
        # Right hand side variables are shared across voters.
        #
        # On the left hand side we have variables x_il that participate in the objective function.
        # These variables are distinct for each voter.
        for v, vote in enumerate(V):
            lhs_names = [get_x_il_name(v=v, l=l) for l in range(k)]
            rhs_names = [get_y_c_name(c) for c in vote]
            constraint = [
                lhs_names + rhs_names,
                [1.0] * len(lhs_names) + [-1.0] * len(rhs_names)
            ]
            problem.linear_constraints.add(
                lin_expr=[
                    constraint
                ],
                senses=["L"],
                rhs=[0.0],
                names=["(3)"]
            )

        aaa_pb.rules.approval.ilp._cplex_helpers.write(problem, "_pav_sp_tu.lp")


        problem.solve()


        committee = aaa_pb.rules.approval.ilp._cplex_helpers.get_committee_from_boolean_variable_names(
            problem=problem,
            number_of_candidates=number_of_candidates,
            candidate_to_var_name_fun=get_y_c_name,
            var_name_to_candidate_fun=get_y_c_name_inverse)

        return committee
