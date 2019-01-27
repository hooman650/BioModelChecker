import logicnetwork
import random


class LocalSearch(object):
    """Local Search for tuning K parameter.

   Tuning K such that the network generate the expected behavior in the state transition graph.
    """
    ln = None
    cur_state = None

    def __init__(self, in_ln):
        self.ln = in_ln

        self.init()

    def init(self):
        print self.ln.K
        # self.cur_state = [random.randint(0, i) for i in self.ln.max_levels]
        # print 'eval', self.eval(self.cur_state)

    def eval(self, state):
        return 0


if __name__ == "__main__":
    random.seed(0)

    mat_file = "example.mat"
    cycle_file = "sync.cycle"
    ln = logicnetwork.LogicNetwork(mat_file, cycle_file)

    ls = LocalSearch(ln)
