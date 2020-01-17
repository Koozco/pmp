class ElectionConfig:
    def __init__(self, rule, k, id):
        """
        :param rule: Scoring rule
        :type rule: Rule
        :param k: Committee size
        :type k: Integer
        :param id: Election id. Used in output filenames
        :type id: String

        Config used in experiments with more than one scoring rule.
        """
        self.rule = rule
        self.k = k
        self.id = id
