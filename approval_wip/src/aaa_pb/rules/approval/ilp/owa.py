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


class PAV_ILP(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        owa = [1.0 / i for i in range(1, k + 1)]

        return ApprovalOWA_ILP.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            K=k,
            owa=owa
        )


class CC_ILP(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        owa = [0.0] * k
        owa[0] = 1.0

        return ApprovalOWA_ILP.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            K=k,
            owa=owa
        )


class ApprovalOWA_ILP():
    """
    Based on
    1. OWA based formulation: "Finding a Collective Set of Items: From Proportional Multirepresentation to Group Recommendation"
    """

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, K: int, owa: List[float]) -> List[int]:
        problem = cplex.Cplex()
        problem.objective.set_sense(problem.objective.sense.maximize)

        def get_x_j_name(c: int) -> str:
            """
            Candidate c is included is in the solution, i.e. the winning committee
            """
            return "x_c{0}".format(c)

        def get_x_j_name_inverse(name: str) -> int:
            return int(name[3:])

        def get_x_ijk_name(v: int, c: int, k: int) -> str:
            """
            Voter v ranks candidate c at k-th position in the winning committee
            """
            return "x_v{0}c{1}k{2}".format(v, c, k)

        number_of_voters = len(V)

        from aaa_pb.rules.approval.ilp._cplex_helpers import add_boolean_variable

        # (g) declare x_j variables
        # x_j <==> candidate j is included in the winning committee
        for c in range(number_of_candidates):
            add_boolean_variable(
                problem=problem,
                name=get_x_j_name(c=c),
                obj=0.0)

        # (f) declare x_ijk
        # x_ijk == 1 <==> for voter i the candidate j is the k-th most favourite candidate in the selected committee
        for v, vote in enumerate(V):
            for c in vote:
                for k in range(K):
                    name = get_x_ijk_name(v=v, c=c, k=k)
                    add_boolean_variable(
                        problem=problem,
                        name=name,
                        obj=owa[k]
                    )

        # (a) SUM[from j:=1 to m](x_j) = K
        #
        # winning committee has size K
        names = [get_x_j_name(c) for c in range(number_of_candidates)]
        coefficients = [1.0] * number_of_candidates
        problem.linear_constraints.add(
            lin_expr=[
                [names,
                 coefficients]
            ],
            senses=["E"],
            rhs=[K * 1.0],
            names=["(a)"]
        )

        # (b) x_ijk <= x_j
        # x_j == 1 implies that candidate j is in the committee
        # x_ijk == 1 implies that candidate j is ranked at k-th position in the committee by voter j
        for v, vote in enumerate(V):
            for c in vote:
                x_j_name = get_x_j_name(c=c)
                for k in range(K):
                    x_ijk_name = get_x_ijk_name(v=v, c=c, k=k)
                    problem.linear_constraints.add(
                        lin_expr=[
                            [
                                [x_ijk_name, x_j_name],
                                [1.0, -1.0]
                            ]
                        ],
                        senses=["L"],
                        rhs=[0.0],
                        names=["(b)_c{0}v{1}k{2}".format(c, v, k)]
                    )

        # (c) SUM[from j:=1 to m](x_ijk) = 1
        # exactly one candidate j is ranked on position k by voter i
        #
        # TODO we actually use < 1, because in approval-ballot setting we don't care about candidates that are not approved
        # """
        # constraint (c) says that each agent ranks only one of the
        # candidates from the solution as k-th best, constrain
        # """
        for v, vote in enumerate(V):
            at_most_K = min(K, len(vote))  # candidate doesn't get any value from candidates it doesn't approve of
            for k in range(at_most_K):
                names = [get_x_ijk_name(v=v, c=c, k=k) for c in vote]
                coefficients = [1.0] * number_of_candidates
                problem.linear_constraints.add(
                    lin_expr=[
                        [names, coefficients]
                    ],
                    senses=["L"],
                    rhs=[1.0],
                    names=["(c)_v{0}k{1}".format(v, k)]
                )

        # (d) SUM[from k:=1 to K](x_ijk) <= 1
        # Voter i ranks candidate j as k-th best alternative in the committee.
        # It is equal to 0 when voter i doesn't approve any members of the committee
        #
        # NOTE: In article "Finding a Collective Set of Items ..." this condition says '.. == 1' which is a mistake
        for v, vote in enumerate(V):
            for c in vote:
                names = [get_x_ijk_name(v=v, c=c, k=k) for k in range(K)]
                coefficients = [1.0] * K
                problem.linear_constraints.add(
                    lin_expr=[
                        [names, coefficients]
                    ],
                    senses=["L"],
                    rhs=[1.0],
                    names=["(d)_v{0}c{1}".format(v, c)]
                )

        # (e) SUM[from j:=1 to m](x_ijk) <= SUM[from j:=1 to m](x_ij{k+1})
        #
        # From "Finding a Collective Set of Items ...":
        # """
        # constraint (e), requires that variables x i,j,k indeed for each agent
        # sort the items from the solution in the order of descending utility values. We mention that
        # constraint (e) is necessary only for the case of OWAs alpha that are not-nonincreasing. For
        # a nonincreasing alpha, an optimal solution for our ILP already ensures the correct "sorting"
        # """
        #
        # NOTE: assertion below is setup to fail  if ova is not-nonincreasing
        for i in range(1, len(owa)):
            assert owa[i - 1] >= owa[i]

        import aaa_pb.rules.approval.ilp._cplex_helpers
        aaa_pb.rules.approval.ilp._cplex_helpers.write(problem, "_owa_ilp_pbatko.lp")

        problem.solve()

        committee = aaa_pb.rules.approval.ilp._cplex_helpers.get_committee_from_boolean_variable_names(
            problem=problem,
            number_of_candidates=number_of_candidates,
            candidate_to_var_name_fun=get_x_j_name,
            var_name_to_candidate_fun=get_x_j_name_inverse)

        return committee
