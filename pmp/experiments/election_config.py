class ElectionConfig:
    """Election configuration used by an Experiment"""

    def __init__(self, rule, k, id):
        """
        :param rule: Scoring rule
        :type rule: Rule
        :param k: Committee size
        :type k: int
        :param id: Election id. Used in output filenames
        :type id: str

        Config used in experiments with more than one scoring rule.
        """
        self.rule = rule
        self.k = k
        self.id = id
