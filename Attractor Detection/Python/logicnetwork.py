#!/usr/bin/python2.7
# Edited by Hooman Sedghamiz March 2018 
# Temporal Multi-level Discrete Logical treatment of Cell Signalling
import scipy.io
#from graph_tool.all import *
import utils
import genk


class LogicNetwork(object):
    thres = []
    K = []
    max_levels = []
    expected_images = dict()
    num_nodes = None
    stg_edges = dict()
    stg_graph = None

    def __init__(self, in_mat_file=None, in_cycle_file=None):
        if in_mat_file:
            self.load_mat_file(in_mat_file)
        if in_cycle_file:
            self.load_expected_stg(in_cycle_file)

    def load_mat_file(self, in_mat_file):
        """ load mat file and process

        :param in_mat_file:
        :return:
        """
        mat = scipy.io.loadmat(in_mat_file)["example"]
        GeneralLogic = mat['GeneralLogic'][0][0]

        # adjacency list
        adj_list = GeneralLogic['Ad'][0][0]

        # maximum transcription level
        self.max_levels = GeneralLogic['N'][0][0][0]
        self.num_nodes = len(self.max_levels)

        # k vector
        raw_k = GeneralLogic['k'][0][0][0]
        raw_k = [a.astype(int) for a in raw_k]

        self.convert(adj_list, raw_k)

    def load_expected_stg(self, in_stg_file):
        """ load expected cycles

        :return: expected_images
        """
        with open(in_stg_file, 'r') as f:
            for line in f.readlines():
                tokens = line.strip().split(">")
                self.expected_images[tokens[0]] = tokens[1:]
        return self.expected_images

    def convert(self, adj_list, raw_k):
        """ Convert the .mat file to desired format

        :pre: every node has at least one incoming edge

        :return:
        """
        # go through every edges to find incoming edges
        num_row, num_col = adj_list.shape
        num_nodes = len(raw_k)

        self.thres = [dict() for _ in range(num_nodes)]
        for i in xrange(num_col):
            adj = adj_list[:, i]
            self.thres[adj[0] - 1][adj[1]] = adj[2]

        # todo: dict could be replaced using a binary mask to improve efficiency
        self.K = [dict() for _ in range(num_nodes)]
        for in_edges in raw_k:  # impact of incoming edges for all node
            for i in xrange(in_edges.shape[1]):
                in_edge = in_edges[:, i]
                if not i:  # constant term
                    key_tuple = ()
                    dict_index = in_edge[0] - 1
                else:  # non-constant term
                    # collect tuple key
                    key_list = []
                    for j in xrange(len(in_edge) - 1):
                        if not in_edge[j]:
                            break
                        key_list.append(in_edge[j])
                    key_list.sort()
                    key_tuple = tuple(key_list)
                self.K[dict_index][key_tuple] = in_edge[-1]

    def comp_S(self, x, theta):
        """ Threshold function

        :param x: current state as a list of ints
        :param theta:
        :return:
        """
        s = x >= abs(theta)
        if theta < 0:
            s = not s
        return s

    def comp_image(self, in_cur_state, delay='sync', K=None):
        """ compute Image of the current state

        :param in_cur_state: as string
        :param delay:
        :return:
        """
        if not K:
            K = self.K

        in_cur_state = [int(i) for i in in_cur_state]
        image_states = []
        image_states_str = []

        if delay == 'sync':
            # for each node, check activation of incoming edges
            for i in xrange(self.num_nodes):
                action_key_list = self.comp_action_key(in_cur_state, i)
                image_states.append(K[i][action_key_list])
                # step change
                if image_states[i] < in_cur_state[i]:
                    image_states[i] = in_cur_state[i] - 1
                elif image_states[i] > in_cur_state[i]:
                    image_states[i] = in_cur_state[i] + 1
            image_states_str = ["".join([str(i) for i in image_states])]

        elif delay == 'async':
            for i in xrange(self.num_nodes):
                image_state = in_cur_state[:]
                same = False
                action_key_list = self.comp_action_key(in_cur_state, i)
                image_state[i] = K[i][action_key_list]
                # step change
                if image_state[i] < in_cur_state[i]:
                    image_state[i] = in_cur_state[i] - 1
                elif image_state[i] > in_cur_state[i]:
                    image_state[i] = in_cur_state[i] + 1
                else:
                    same = True
                if not same:
                    image_states_str.append("".join([str(i) for i in image_state]))

        return image_states_str

    def state_transition_graph(self):
        """Enumerate Full State Transition Graph

        :return: a dict that maps every possible source node to target node(s)
        """
        if self.stg_edges:
            return self.stg_edges

        # enumerate all possible states
        cur_state = [0 for i in xrange(self.num_nodes)]

        idx = 0
        while True:
            cur_state_str = "".join([str(i) for i in cur_state])
            self.stg_edges[cur_state_str] = self.comp_image(cur_state_str, "sync")[0]

            # move forward to the next state
            # the current bit doesn't fit, carry to the next bits
            carry = False
            while idx < self.num_nodes and cur_state[idx] == self.max_levels[idx]:
                cur_state[idx] = 0
                idx += 1
                carry = True

            if idx < self.num_nodes:
                cur_state[idx] += 1
            else:
                break

            # reset idx if carry is effective
            if carry:
                idx = 0

        return self.stg_edges

    def viz(self):
        """visualize state transition graph using graph-tool

        :return:
        """
        if not self.stg_edges:
            self.state_transition_graph()

        # set seed to get consistent layout
        seed_rng(1)

        self.stg_graph = Graph()
        label_to_vertex = dict()
        vprop = self.stg_graph.new_vertex_property("string")
        self.stg_graph.vp.label = vprop

        for source, target in self.stg_edges.iteritems():
            if source in label_to_vertex:
                source_v = label_to_vertex[source]
            else:
                source_v = self.stg_graph.add_vertex()
                self.stg_graph.vp.label[source_v] = source
                label_to_vertex[source] = source_v

            if target in label_to_vertex:
                target_v = label_to_vertex[target]
            else:
                target_v = self.stg_graph.add_vertex()
                self.stg_graph.vp.label[target_v] = target
                label_to_vertex[target] = target_v

            self.stg_graph.add_edge(source_v, target_v)

        graph_draw(self.stg_graph, vertex_text=self.stg_graph.vp.label,
                   output_size=(1000, 1000), output="example.pdf")

    def comp_action_key(self, cur_state, node):
        action_key_list = []
        for in_edge, thres in self.thres[node].iteritems():
            if self.comp_S(cur_state[in_edge - 1], thres):
                action_key_list.append(in_edge)

        return tuple(action_key_list)

    def check_step_increment(self, expected_images):
        """check if every directed edge satisfies the step increment requirement in synchronous update

        :return: True if satisfied; False, otherwise.
        """
        for source, targets in expected_images.iteritems():
            for target in targets:
                for i in xrange(self.num_nodes):
                    if abs(int(source[i]) - int(target[i])) > 1:
                        return False
        return True

    def config_k(self, expected_stg=None):
        """config k in linear time
        Based on every directed edge in the given expected state transition graph

        :param expected_stg:
        :return:
        """
        # load expected images
        if expected_stg:
            expected_images = self.load_expected_stg(expected_stg)
        else:
            expected_images = self.expected_images

        if not self.check_step_increment(expected_images):
            return None

        # init expected K, according to incoming edges
        got_k_range = [dict() for _ in xrange(self.num_nodes)]

        for node in xrange(self.num_nodes):
            in_edges = self.thres[node].keys()
            for subset in utils.powerset(in_edges):
                got_k_range[node][subset] = [0, self.max_levels[node]]

        for source, targets in expected_images.iteritems():
            source_int = [int(i) for i in source]
            for target in targets:
                for node in xrange(self.num_nodes):
                    action_key = self.comp_action_key(source_int, node)
                    print source, ">", target, "node", node + 1, "action key", action_key, "cur k", \
                        got_k_range[node][action_key], "target k", int(target[node])
                    if int(source[node]) < int(target[node]):
                        # stepwise increment, gives a lower bound (k could go higher)
                        got_k_range[node][action_key][0] = max(got_k_range[node][action_key][0], int(target[node]))
                    elif int(source[node]) > int(target[node]):
                        # stepwise decrement, gives an upper bound (k could go lower)
                        got_k_range[node][action_key][1] = min(got_k_range[node][action_key][1], int(target[node]))
                    else:
                        got_k_range[node][action_key] = [int(target[node]), int(target[node])]

            print 'got k after', source, ">", target
            print got_k_range

        return got_k_range

    def verify_got_k(self, got_k):
        """compare the got K parameters with the expected ones

        :param got_k:
        :return: True if the same; False, otherwise.
        """
        for i in xrange(self.num_nodes):
            diff_keys = utils.diff_dict(got_k[i], self.K[i])
            if diff_keys:
                print "node", i + 1, "diff keys", diff_keys
                return False

        return True

    def verify_got_stg_range(self, got_k_range, expected_stg_file=None):
        """using the got_k_range to generate stg, and compare with the expected one

        :param got_k_range: k_range instead of a single k
        :param expected_stg_file:
        :return:
        """
        # load expected images
        if expected_stg_file:
            expected_images = self.load_expected_stg(expected_stg_file)
        else:
            expected_images = self.expected_images

        if not self.check_step_increment(self.expected_images):
            return None

        # extract got_k from got_k_range to get every combination of k
        for got_k in genk.GenK(got_k_range):
            print 'check', got_k,
            if not self.verify_got_stg(got_k, expected_images):
                print 'fail'
                return False
            print 'pass'
        return True

    def verify_got_stg(self, got_k, expected_images):
        """using the got_k to generate stg, and compare with the expected one

        :param got_k:
        :param expected_images:
        :return:
        """
        for source, targets in expected_images.iteritems():
            got_target = self.comp_image(source, "sync", got_k)
            if set(got_target) != set(targets):
                print "source", source
                print "got target", got_target
                print "expect target", targets
                return False
        return True


if __name__ == "__main__":
    mat_file = "example.mat"
    cycle_file = "sync-reduced.cycle"
    ln = LogicNetwork(mat_file, cycle_file)
    # print 'K', ln.K
    print 'thres', ln.thres
    # print 'max_levels', ln.max_levels

    got_k_range = ln.config_k()

    # print ln.comp_image('1100', delay='sync')
    print ln.verify_got_stg_range(got_k_range)
