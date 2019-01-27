import copy
import itertools


class GenK:
    def __init__(self, k_range):
        self.k_range = k_range
        self.k = copy.deepcopy(self.k_range)
        # create a list of lists from self.k_range
        ll = []
        for i in xrange(len(self.k_range)):
            for key, value in self.k_range[i].iteritems():
                ll.append(range(value[0], value[1] + 1))
        self.iter = itertools.product(*ll)

    def __iter__(self):
        return self

    def next(self):
        try:
            k_vec = self.iter.next()
            idx = 0
            for i in xrange(len(self.k_range)):
                for key, value in self.k_range[i].iteritems():
                    self.k[i][key] = k_vec[idx]
                    idx += 1
            return self.k
        except StopIteration:
            raise StopIteration
