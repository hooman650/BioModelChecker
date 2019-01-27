import itertools


def powerset(elems):
    """Get the all 2^n subsets of given set of elems (i.e., powerset)

    :param elems:
    :return:
    """
    elems.sort()
    return set(itertools.chain.from_iterable(itertools.combinations(elems, r) for r in range(len(elems) + 1)))


def diff_dict(d1, d2):
    """check if two dicts with the same keys have the same values

    :param d1:
    :param d2:
    :return: [], if the two dicts are the same;
             Otherwise, return the list of keys that leads to different values
    """
    return [k for k in d1 if d1[k] != d2[k]]
