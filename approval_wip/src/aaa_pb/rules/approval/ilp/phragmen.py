from typing import List, Callable, Tuple, Any

import cplex

import aaa_pb.rules.approval.ilp._cplex_helpers
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


# Special Ordered Sets?
# Explanations:
# http://lpsolve.sourceforge.net/5.0/SOS.htm
# https://en.wikipedia.org/wiki/Special_ordered_set

# https://github.com/Pyomo/pyomo

class PhragmenMax_ILP(ApprovalBasedRuleBase):

    @classmethod
    def apply(cls, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee, voter_loads = cls.computeCommitteeAndLoads(number_of_candidates=number_of_candidates,
                                                              k=k,
                                                              V=V, )

        # NOTE: uncomment below to draw load vector graph
        # # voter_loads_desc = sorted(voter_loads, key=lambda x: -x)
        # cls.draw_bar_graph(
        #     values=voter_loads_desc,
        #     output_file_name="/home/pbatko/src/code-misc/python/voting-rules/piotr/plots/phragmen12_more_indicator.png")

        return committee

    @classmethod
    def computeCommitteeAndLoads(cls,
                                 number_of_candidates: int,
                                 k: int,
                                 V: List[List[int]],
                                 quiet: bool = True,
                                 lp_output_file_name: str = None,
                                 verify_boolean_variable: Callable = None) -> Tuple[List[int], List[float]]:

        number_of_voters = len(V)

        # initialize y vector: y = [k, 0, 0, 0, .., 0]
        y = [0.0] * number_of_voters
        y[0] = 1.0 * k

        # TODO should we use mip_integrality_tolerance when comparing epsilon to 0?
        # p = cplex.Cplex()
        # mip_integrality_tolerance = p.parameters.mip.tolerances.integrality.get()
        # default is probably ~1.e-05

        committee: List[int] = None
        load_vector: List[float] = None

        for l in range(number_of_voters):
            epsilon, load_vector, committee = Phragmen_ILP.solve_ilp_max(V=V,
                                                                         number_of_candidates=number_of_candidates,
                                                                         k=k,
                                                                         y_vector=y,
                                                                         quiet=quiet,
                                                                         lp_output_file_name=lp_output_file_name,
                                                                         verify_boolean_variable=verify_boolean_variable)
            voter_loads_desc = sorted(load_vector, key=lambda x: -x)
            if epsilon == 0:
                epsilon, load_vector, committee = Phragmen_ILP.solve_ilp_max(V=V,
                                                                             number_of_candidates=number_of_candidates,
                                                                             k=k,
                                                                             y_vector=voter_loads_desc,
                                                                             quiet=quiet,
                                                                             lp_output_file_name=lp_output_file_name,
                                                                             verify_boolean_variable=verify_boolean_variable)
                if epsilon == 0:
                    break

            y = voter_loads_desc[:l + 2] + [0.0] * (number_of_voters - l - 2)

        return committee, load_vector

    pass


class PhragmenVar_ILP(ApprovalBasedRuleBase):

    @classmethod
    def apply(cls, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        committee, _ = cls.computeCommitteeAndLoads(number_of_candidates=number_of_candidates,
                                                    k=k,
                                                    V=V)

        return committee

    @classmethod
    def computeCommitteeAndLoads(cls,
                                 number_of_candidates: int,
                                 k: int,
                                 V: List[List[int]],
                                 quiet: bool=True,
                                 lp_output_file_name: str=None) -> Tuple[List[int], List[float]]:
        load_vector, committee = Phragmen_ILP.solve_ilp_var(V=V,
                                                            number_of_candidates=number_of_candidates,
                                                            k=k,
                                                            quiet=quiet,
                                                            lp_output_file_name=lp_output_file_name)

        return committee, load_vector


class Phragmen_ILP():

    @classmethod
    def solve_ilp_var(cls,
                      V: List[List[int]],
                      number_of_candidates: int,
                      k: int,
                      quiet: bool,
                      lp_output_file_name: str) -> Tuple[List[float], List[int]]:

        problem = cplex.Cplex()

        # if quiet:
        #     _cplex_helpers.suppress_output(problem)

        problem.objective.set_sense(problem.objective.sense.minimize)

        x_vc_names_byVoter = cls.set_fundamental_phragmen_constraints(V=V,
                                                                      k=k,
                                                                      number_of_candidates=number_of_candidates,
                                                                      problem=problem)

        def get_x_v_name(v):
            # type: (int) -> str
            # total load of voter v
            return "x_v{0}".format(v)

        # Setup a new variable for each load vector
        # This effectively serves an alias
        # which we then use in the objective function definition
        x_v_names = []
        for voter, x_vc_names in enumerate(x_vc_names_byVoter):
            x_v_name = get_x_v_name(voter)
            problem.variables.add(
                obj=[0.0],
                lb=[0.0],
                ub=[1.0 * k],
                names=[x_v_name]
            )
            x_v_names.append(x_v_name)

            coefficients = [1.0] * len(x_vc_names) + [-1.0]
            names = x_vc_names + [x_v_name]

            problem.linear_constraints.add(
                lin_expr=[
                    [names, coefficients]
                ],
                senses=["E"],
                rhs=[0.0],
                names=["x_v{0}_alias".format(voter)]
            )

        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.3/ilog.odms.cplex.help/CPLEX/UsrMan/topics/discr_optim/mip_quadratic/02_introMIQP.html
        # If the problem contains an objective function with no quadratic term, (a linear objective),
        # then the problem is termed a Mixed Integer Linear Program (MILP).
        #
        # However, if there is a quadratic term in the objective function,
        # the problem is termed a Mixed Integer Quadratic Program (MIQP).

        # https://stackoverflow.com/questions/38949055/linear-and-quadratic-terms-in-cplex-objective-function

        # set quadratic objective function
        triplets = [(n, n, 1.0) for n in (x_v_names)]
        problem.objective.set_quadratic_coefficients(
            triplets
        )

        if lp_output_file_name is not None:
            aaa_pb.rules.approval.ilp._cplex_helpers.write(problem, lp_output_file_name)

        # solve
        problem.solve()

        # TODO tidy up
        # solution.get_status() returns an integer code
        print("Solution status = ", problem.solution.get_status(), ":")
        # the following line prints the corresponding string
        print(problem.solution.status[problem.solution.get_status()])
        print("Solution value  = ", problem.solution.get_objective_value())

        # get solution
        committee = cls.get_committee_from_solution(problem, number_of_candidates=number_of_candidates, k=k)
        load_vector = cls.get_load_vector_from_solution(problem, x_vc_names_byVoter=x_vc_names_byVoter)

        return load_vector, committee

    @classmethod
    def solve_ilp_max(cls,
                      V: List[List[int]],
                      number_of_candidates: int,
                      k: int,
                      y_vector: List[float],
                      quiet: bool,
                      lp_output_file_name: str,
                      verify_boolean_variable: Callable) -> Tuple[float, List[float], List[int]]:

        # import cplex_bak
        problem = cplex.Cplex()

        # https://www.ibm.com/support/knowledgecenter/SS9UKU_12.7.0/com.ibm.cplex.zos.help/CPLEX/Parameters/topics/MIPEmphasis.html
        # 1	CPX_MIPEMPHASIS_FEASIBILITY	Emphasize feasibility over optimality
        # problem.parameters.emphasis.mip.set(1)
        problem.parameters.emphasis.mip.set(0)

        # List of parameters: https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/introListAlpha.html

        # TODO use this parameters to get tighter results
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/EpInt.html
        # problem.parameters.mip.tolerances.integrality.set(0.0)
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/EpGap.html
        # problem.parameters.mip.tolerances.mipgap.set(0.0)
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/EpAGap.html
        # problem.parameters.mip.tolerances.absmipgap.set(0.0)

        # problem.parameters.
        # if quiet:
        #     _cplex_helpers.suppress_output(problem)

        problem.objective.set_sense(problem.objective.sense.maximize)

        x_vc_names_byVoter = cls.set_fundamental_phragmen_constraints(V, k, number_of_candidates,
                                                                      problem)

        ####################
        ####################

        # TODO I tried this option to achieve faster convergence, but they did nothing that mattered
        # In the end indicator variables did the trick.
        # Leaving the names of tried parameters and links for future reference.

        # relative MIP gap tolerance
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/EpGap.html
        # -> increase the gap
        # problem.parameters.mip.tolerances.mipgap.set(0.1)  # default: 0.0001

        # relative objective difference cutoff
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/RelObjDif.html
        # problem.parameters.mip.tolerances.relobjdifference.set(0.1)

        # CPLEX MIP Tolerance Parameter Options
        # http://www.maximalsoftware.com/solvopt/optCpxMipTol.html

        # CPLEX MIP termination
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/UsrMan/topics/discr_optim/mip/usage/11_terminate.html

        number_of_voters = len(V)

        def get_e_ij_name(voter1: int, voter2: int) -> str:
            return "e_i{0}j{1}".format(voter1, voter2)

        def get_s_i_name(v: int) -> str:
            return "s_i{0}".format(v)

        def get_t_j_name(v: int) -> str:
            return "t_j{0}".format(v)

        boolean_variable_names = []

        def add_boolean_variable(name):
            boolean_variable_names.append(name)
            problem.variables.add(
                obj=[0.0],
                lb=[0.0],
                ub=[1.0],
                names=[name],
                types=[problem.variables.type.integer]
            )

        # (7) e_ij in {0, 1}
        for i in range(number_of_voters):
            for j in range(number_of_voters):
                add_boolean_variable(name=get_e_ij_name(i, j))

        # (8) s_i in {0, 1}
        for i in range(number_of_voters):
            add_boolean_variable(name=get_s_i_name(i))

        # TODO don't define t_j for j where y_j is zero
        # TODO don't define t_j for j where y_j is optimal
        # but cplex seems to be figuring these things out for itself

        # (9) t_j in {0, 1}
        for j in range(number_of_voters):
            add_boolean_variable(name=get_t_j_name(j))

        # (10) s_i + sum over all j e_ij = 1
        for i in range(number_of_voters):
            s_i = get_s_i_name(i)
            e_ijs = [get_e_ij_name(i, j) for j in range(number_of_voters)]
            constraint = [
                e_ijs + [s_i],
                [1.0] * (number_of_voters + 1)
            ]
            problem.linear_constraints.add(
                lin_expr=[constraint],
                senses=["E"],
                rhs=[1.0],
                names=["(10)_i{0}".format(i)]
            )

        # (11) t_i + sum over all i e_ij <= 1
        for j in range(number_of_voters):
            t_j = get_t_j_name(j)
            e_ijs = [get_e_ij_name(i, j) for i in range(number_of_voters)]
            constraint = [
                e_ijs + [t_j],
                [1.0] * (number_of_voters + 1)
            ]
            problem.linear_constraints.add(
                lin_expr=[constraint],
                senses=["L"],
                rhs=[1.0],
                names=["(11)_j{0}".format(j)]
            )

        # (12) sum t_j = 1
        t_js = [get_t_j_name(j) for j in range(number_of_voters)]
        problem.linear_constraints.add(
            lin_expr=[
                [
                    t_js,
                    [1.0] * len(t_js)
                ]
            ],
            senses=["E"],
            rhs=[1.0],
            names=["(12)"]
        )

        def get_y_j_name(j: int) -> str:
            return "y_{0}".format(j)

        def get_e_name() -> str:
            return "e"

        problem.variables.add(
            obj=[1.0],
            names=[get_e_name()]
        )

        # define a variable with a constant value for each element of y vector
        # TODO why don't we just use constants, instead of variables where ub == lb? does it matter?
        ys = y_vector
        ys_names = [get_y_j_name(j) for j in range(number_of_voters)]
        problem.variables.add(
            obj=[0.0] * number_of_voters,
            ub=ys,
            lb=ys,
            names=ys_names
        )

        # (13) voter_load - k(1 - e_ij) <= y_j         for all i,j in voters
        # and
        # (14) voter_load - k(2 - s_i - tj) <= y_j - e         for all i,j in voters
        for i in range(number_of_voters):
            for j in range(number_of_voters):
                x_vc_names_from_one_voter = x_vc_names_byVoter[i]
                x_vc_coefficients = [1.0] * len(x_vc_names_from_one_voter)

                # e_ij == 1 => xBar_i <= y_j
                # in other words:
                # e_ij == 1 => xBar_i - y_j <= 0
                constraint13 = [
                    x_vc_names_from_one_voter + [get_y_j_name(j)],
                    x_vc_coefficients + [-1.0]
                ]
                problem.indicator_constraints.add(
                    indvar=get_e_ij_name(i, j),
                    complemented=0,
                    rhs=0.0,
                    lin_expr=constraint13,
                    name="(13)_i{0}j{0}".format(i, j),
                    sense="L",
                    indtype=problem.indicator_constraints.type_.if_
                )

                # t_j == 1 => xBar_i - k(1 - s_i) <= y_j - e
                # in other words
                # t_j == 1 => xBar_i + k(s_i) - y_j + e <= k
                constraint14 = [
                    x_vc_names_from_one_voter + [get_s_i_name(i), get_y_j_name(j), get_e_name()],
                    x_vc_coefficients + [k * 1.0, -1.0, 1.0]
                ]
                problem.indicator_constraints.add(
                    indvar=get_t_j_name(j),
                    complemented=0,
                    rhs=1.0 * k,
                    lin_expr=constraint14,
                    name="(14)_i{0}j{0}".format(i, j),
                    sense="L",
                    indtype=problem.indicator_constraints.type_.if_
                )

        if lp_output_file_name is not None:
            aaa_pb.rules.approval.ilp._cplex_helpers.write(problem, lp_output_file_name)

        # _cplex_helpers.write(problem, "_phragmen.lp")
        problem.solve()

        if not quiet:
            aaa_pb.rules.approval.ilp._cplex_helpers.print_all_variables(problem)
        # verify if boolean like variables have boolean values
        if verify_boolean_variable is not None:
            for name in boolean_variable_names:
                value = problem.solution.get_values(name)
                verify_boolean_variable(value, name)

        epsilon_value: float = problem.solution.get_values(get_e_name())
        voters_load_vector: List[float] = cls.get_load_vector_from_solution(problem, x_vc_names_byVoter)
        committee: List[int] = cls.get_committee_from_solution(problem, number_of_candidates=number_of_candidates, k=k)

        return epsilon_value, voters_load_vector, committee

    @classmethod
    def get_load_vector_from_solution(self, problem: cplex.Cplex, x_vc_names_byVoter: List[List[str]]) -> List[float]:
        load_vector = []
        for x_vc_names in x_vc_names_byVoter:
            load = sum(problem.solution.get_values(x_vc_names))
            load_vector.append(load)
        return load_vector

    @classmethod
    def get_committee_from_solution(cls, problem: cplex.Cplex, number_of_candidates: int, k: int) -> List[int]:
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/Parameters/topics/EpInt.html
        # problem.parameters.mip.tolerances.integrality
        # Why does a binary or integer variable take on a noninteger value in the solution?: https://www-01.ibm.com/support/docview.wss?uid=swg21399984

        committee = []
        mip_integrality_tolerance = problem.parameters.mip.tolerances.integrality.get()
        for c in range(number_of_candidates):
            x_c_name = cls.get_x_c_name(c)
            x_c_value = problem.solution.get_values(x_c_name)
            if x_c_value > mip_integrality_tolerance:  # ~ value > 1e-05 ~ 0.0
                committee.append(cls.get_x_c_name_inverse(x_c_name))
        # sanity check
        if len(set(committee)) != k:
            raise Exception
        return committee

    @classmethod
    def x_vc_name(cls, c: int, v: int) -> str:
        # load received be voter v from candidate v
        return "x_v{0}c{1}".format(v, c)

    @classmethod
    def get_x_c_name(cls, c: int) -> str:
        # total load induced by candidate c
        return "x_c{0}".format(c)

    @classmethod
    def get_x_c_name_inverse(cls, name: str) -> int:
        return int(name[3:])

    @classmethod
    def set_fundamental_phragmen_constraints(cls, V: List[List[int]], k: int, number_of_candidates: int, problem: cplex.Cplex) -> List[List[str]]:

        number_of_voters = len(V)
        x_vc_names_byVoter = [[] for _ in range(number_of_voters)]
        x_vc_names_byCandidate = [[] for _ in range(number_of_candidates)]
        # (1) 0 <= x_v,c <= 1 for all v in V, c in C
        # and
        # (2) x_v,c = 0 if c not in V[v] // c not int A_v
        #
        # i.e. load induced by a candidate c on a voter c is a real number in range [0, 1]
        for voter, vote in enumerate(V):
            for c in vote:
                name = cls.x_vc_name(c=c, v=voter)
                x_vc_names_byVoter[voter].append(name)
                x_vc_names_byCandidate[c].append(name)
                problem.variables.add(
                    obj=[0.0],
                    lb=[0.0],
                    ub=[1.0],
                    names=[name]
                )
        # (3) sum of all x_v,c = k
        #
        # i.e. sum of all loads equals to k
        x_vc_names_flattened = []
        for total_load_of_voter in x_vc_names_byVoter:
            x_vc_names_flattened.extend(total_load_of_voter)
        constraint = [
            x_vc_names_flattened,
            [1.0] * len(x_vc_names_flattened)
        ]
        problem.linear_constraints.add(
            lin_expr=[constraint],
            senses=["E"],
            rhs=[k],
            names=["(3)"]
        )
        # (4)
        # sum over v in V of x_v,c is either 0 or 1, for each c
        #
        # i.e. load induced by a candidate over its voters sums up to 1 if candidate is in the selected committee
        # 0 otherwise
        #
        # TODO see what would the impact of defining x_c_name as an indicator variable
        # TODO would it improve performance?
        # TODO probably not, as a quick check showed performance degradation
        for c, loads_induced_by_one_candidate in enumerate(x_vc_names_byCandidate):
            x_c_name = cls.get_x_c_name(c)
            problem.variables.add(
                obj=[0.0],
                lb=[0.0],
                ub=[1.0],
                types=[problem.variables.type.integer],
                names=[x_c_name]
            )
            constraint = [
                loads_induced_by_one_candidate + [x_c_name],
                [1.0] * len(loads_induced_by_one_candidate) + [-1.0]
            ]
            problem.linear_constraints.add(
                lin_expr=[constraint],
                senses=["E"],
                rhs=[0.0],
                names=["(4)_c{0}".format(c)]
            )
        return x_vc_names_byVoter

    @classmethod
    def draw_bar_graph(cls, values: List[Any], output_file_name: str=None) -> None:
        # https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
        # https://plot.ly/matplotlib/bar-charts/

        import matplotlib.pyplot as plt
        import numpy as np

        values_len = len(values)
        x = np.arange(values_len)
        plt.bar(x, height=values)
        plt.xticks(x + .5, range(values_len))
        # plt.show()
        if output_file_name is not None:
            # https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
            # https://stackoverflow.com/a/9890599/554036
            plt.savefig(output_file_name, bbox_inches='tight')
