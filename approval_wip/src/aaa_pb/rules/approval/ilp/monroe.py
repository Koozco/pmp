from typing import List

import cplex

from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


# CPLEX misc reading
#
# 1. What is a special ordered set (SOS)?
# https://www.ibm.com/support/knowledgecenter/SSSA5P_12.5.1/ilog.odms.cplex.help/CPLEX/UsrMan/topics/discr_optim/sos/02_SOS_defn.html
#
# 2. Why does a binary or integer variable take on a noninteger value in the solution?
# https://www-01.ibm.com/support/docview.wss?uid=swg21399984
#
# 3. Difference between using indicator constraints and a big-M formulation
# https://www-01.ibm.com/support/docview.wss?uid=swg21400084
#
# 4. LP file format
# http://www.rpi.edu/dept/math/math-programming/cplex66/sun4x_58/doc/refman/html/appendixE13.html
#
# 5. Some tutorial on linear programming
# http://doc.sagemath.org/html/en/thematic_tutorials/linear_programming.html

class Monroe_ILP(ApprovalBasedRuleBase):
    """
    Achieving Fully Proportional Representation: Approximability Results
    """

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        owa = [0.0] * k
        owa[0] = 1.0

        return Approval_Monroe_ILP_Base.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            K=k,
        )


class Approval_Monroe_ILP_Base:
    # Based on
    # 2. Monroe: "Achieving Fully Proportional Representation: Approximability Results"

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, K: int) -> List[int]:
        problem = cplex.Cplex()

        number_of_voters = len(V)

        def add_boolean_variable(name: str, obj: float) -> None:
            problem.variables.add(
                obj=[obj],
                lb=[0.0],
                ub=[1.0],
                names=[name],
                types=[problem.variables.type.integer]
            )
            pass

        def get_x_j_name(c: int) -> str:
            """
            Candidate c is included is in the solution, i.e. the winning committee
            """
            return "x_c{0}".format(c)

        def get_x_j_name_inverse(name: str) -> int:
            return int(name[3:])

        def get_a_ij_name(v: int, c: int) -> str:
            """
            Voter v is represented by candidate c
            """
            return "a_i{0}j{1}".format(v, c)

        # Iterate over on every (voter, candidate) pair
        # even if a voter doesn't approve the candidate.
        # I.e. the representative of a voter might not be approved by the voter.
        #
        # 0 <= a_ij <= 1
        #
        # Objective:
        # Maximize SUM[from i:=1 to n](SUM[j: i approves j](a_ij))
        #
        for v in range(number_of_voters):
            for c in range(number_of_candidates):
                add_boolean_variable(
                    name=get_a_ij_name(v=v, c=c),
                    obj=1.0)

        for c in range(number_of_candidates):
            add_boolean_variable(
                name=get_x_j_name(c=c),
                obj=0.0
            )

        # 2.(a)
        # 0 <= a_ij <= x_j
        #
        # Candidate c can represent voter v only if candidate c is in the solution
        for c in range(number_of_candidates):
            x_j_name = get_x_j_name(c=c)
            for v in range(number_of_voters):
                a_ij_name = get_a_ij_name(v=v, c=c)
                constraint = [
                    [a_ij_name, x_j_name],
                    [1.0, -1.0]
                ]
                problem.linear_constraints.add(
                    lin_expr=[constraint],
                    senses=["L"],
                    rhs=[0.0]
                )

        # 2.(b)
        # SUM[from j:=1 to m](a_ij) == 1
        #
        # Every voter is represented by exactly one candidate
        for v in range(number_of_voters):
            names = [get_a_ij_name(v=v, c=c) for c in range(number_of_candidates)]
            coefficients = [1.0] * number_of_candidates
            constraint = [names, coefficients]
            problem.linear_constraints.add(
                lin_expr=[constraint],
                senses=["E"],
                rhs=[1.0]
            )

        # 2.(c)
        # x_j*floor(n/K) <= SUM[from i:=1 to n](a_ij) <= x_j*ceiling(n/K)
        #
        # Each candidate either doesn't represent anyone or represents an equal segment of voters
        #
        if number_of_voters % K == 0:
            # If K divides n we can use simpler formulation:
            # SUM[from i:=1 to n](a_ij) == x_j*n/K
            #
            voters_segment_exact = number_of_voters / K
            for c in range(number_of_candidates):
                voter_represented_by_c_names = [get_a_ij_name(c=c, v=v) for v in range(number_of_voters)]
                coefficients = [1.0] * number_of_candidates
                constraint = [
                    voter_represented_by_c_names + [get_x_j_name(c)],
                    coefficients + [-1.0 * voters_segment_exact]
                ]
                problem.linear_constraints.add(
                    lin_expr=[constraint],
                    senses=["E"],
                    rhs=[0.0]
                )
        else:
            voters_segment_lb = number_of_voters / K
            voters_segment_ub = voters_segment_lb + 1
            for c in range(number_of_candidates):
                voter_represented_by_c_names = [get_a_ij_name(c=c, v=v) for v in range(number_of_voters)]
                coefficients = [1.0] * number_of_voters
                # ub
                # SUM[from i:=1 to n](a_ij) - x_j*ceiling(n/K) <= 0
                constraint_ub = [
                    voter_represented_by_c_names + [get_x_j_name(c)],
                    coefficients + [-1.0 * voters_segment_ub]
                ]
                problem.linear_constraints.add(
                    lin_expr=[constraint_ub],
                    senses=["L"],
                    rhs=[0.0]
                )
                # lb
                # SUM[from i:=1 to n](a_ij) - x_j*floor(n/K) => 0
                constraint_lb = [
                    voter_represented_by_c_names + [get_x_j_name(c)],
                    coefficients + [-1.0 * voters_segment_lb]
                ]
                problem.linear_constraints.add(
                    lin_expr=[constraint_lb],
                    senses=["G"],
                    rhs=[0.0]
                )

        # 2.(d)
        # SUM[from j:= 1 to n](x_j) == K (in the paper its <= K)
        # there are exactly K winners
        #
        # """ ???
        # For the Monroe framework inequality here is equivalent to equality. We use the inequality so that
        # deleting constraints from item (2c) leads to an ILP for the Chamberlin-Courant rule.
        # """
        #
        x_j_names = [get_x_j_name(c=c) for c in range(number_of_candidates)]
        constraint = [
            x_j_names,
            [1.0] * number_of_candidates
        ]
        problem.linear_constraints.add(
            lin_expr=[constraint],
            senses=["E"],
            rhs=[1.0*K]
        )

        import aaa_pb.rules.approval.ilp._cplex_helpers
        aaa_pb.rules.approval.ilp._cplex_helpers.write(problem, "_monroe_ilp_pbatko.lp")

        problem.solve()

        candidates_names = [get_x_j_name(c=c) for c in range(number_of_candidates)]
        candidates_values = problem.solution.get_values(candidates_names)
        committee = []
        committee_values = []
        committee_names = []
        for name, value in zip(candidates_names, candidates_values):
            if value > 0.0:
                committee_values.append(value)
                committee_names.append(name)
                committee.append(get_x_j_name_inverse(name))

        # cplex_helpers.print_all_variables(problem)

        return committee

