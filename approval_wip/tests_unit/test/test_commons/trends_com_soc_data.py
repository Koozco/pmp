class TrendsComSoc_Data:
    # These test cases are based on example from:
    # """
    # Piotr Faliszewski, Piotr Skowron, Arkadii Slinko, and
    # Nimrod Talmon. Multiwinner Voting: A New Challenge for Social
    # Choice Theory. In Ulle Endriss (editor), Trends in Computational
    # Social Choice, chapter 2, pages 27-47. AI Access, 2017.
    # """
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4

    V_call_rule_for_example_2_3 = [
        [a, b, c],
        [a, e],
        [d],
        [b, c, d],
        [b, c],
        [b]
    ]

    @classmethod
    def call_rule_for_example_2_3(cls, rule):


        committee = rule.apply(
            number_of_candidates=5,
            k=2,
            V=cls.V_call_rule_for_example_2_3

        )
        return sorted(committee)

