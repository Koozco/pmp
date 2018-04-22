class Algorithm:
    def __init__(self, rule):
        self.rule = rule.copy_rule()

    def find_committee(self):
        """Find committee referring to rule attributes as self.rule.*"""
        raise NotImplementedError()

    def set_algorithm(self):
        """Return rule instance with substituted find_committee method."""
        raise NotImplementedError()
