import numpy as np
from algorithms.retiming.strategies import *


def binary_search(search_algorithm):
    """
    Binary search meant to be used as a decorator for algorithms OPT1 and OPT2

    :param search_algorithm: OPT1 or OPT2 algorithms
    :return:
    """

    if search_algorithm != opt1 and search_algorithm != opt2:
        raise Exception("Cannot apply this specific binary search to specified search_algorithm")

    def bin_search(*args):
        low = 0
        high = len(args[1]) - 1

        tuple_ = (np.inf, None)

        while low <= high:
            mid = (high + low) // 2
            results = search_algorithm(args[0], args[1][mid], *args[2:])

            if results['valid']:
                tuple_ = (args[1][mid], results['r'])
                high = mid - 1
            else:
                low = mid + 1

        return tuple_[0], tuple_[1]

    return bin_search