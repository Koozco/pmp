class Preference(object):
    def __init__(self, weight):
        self.weight = weight

    def larger(self, pred, succ):
        raise NotImplementedError()

    def smaller(self, pred, succ):
        raise NotImplementedError()

    def tied(self, pred, succ):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def is_valid(self, num_cand):
        raise NotImplementedError()

    def remove_candidate(self, cand):
        raise NotImplementedError()


class OrdinalPreference(Preference):
    def __init__(self, weight, order):
        Preference.__init__(self, weight)
        self.order = order
        self.positions = {}
        self.weight = weight
        for pos, cand in enumerate(order):
            self.positions[cand] = pos

    def larger(self, pred, succ):
        self.positions[pred] > self.positions[succ]

    def smaller(self, pred, succ):
        self.positions[pred] < self.positions[succ]

    def tied(self, pred, succ):
        return False

    def pos_of(self, cand):
        return self.positions[cand]

    def at_pos(self, pos):
        return self.order[pos]

    def remove_candidate(self, cand):
        new_order = list(self.order)
        new_order.remove(cand)
        return OrdinalPreference(self.weight, new_order)

    def is_valid(self, num_cand):
        return len(self.order) == num_cand and len(set(self.order)) == num_cand


class DichotomousPreference(Preference):

    def __init__(self, approved, num_cand, weight=1):
        self.approved = set(approved)
        self.num_cand = num_cand
        self.is_valid(num_cand)
        self.approved01 = []
        self.weight = weight
        for i in range(num_cand):
            if (i in self.approved):
                self.approved01.append(True)
            else:
                self.approved01.append(False)

    def __str__(self):
        return str(list(self.approved))

    def is_valid(self, num_cand):
        if num_cand != self.num_cand:
            print(self, " not valid for num_cand =", num_cand)
            exit()
        for c in self.approved:
            if c < 0 or c >= num_cand:
                print(self, " not valid for num_cand =", num_cand)
                exit()
        return True

    def larger(self, pair):
        assert len(pair) == 2
        return (self.approves(pair[0])) and not (self.approves(pair[1]))

    def smaller(self, pair):
        return (self.approves(pair[1])) and not (self.approves(pair[0]))

    def tied(self, pair):
        assert len(pair) == 2
        return not self.smaller(pair) and not self.larger(pair)

    def approves(self, candidate):
        return self.approved01[candidate]
