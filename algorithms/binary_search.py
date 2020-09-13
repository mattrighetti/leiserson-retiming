import numpy as np

__all__ = ['binary_search']


def binary_search(search_algorithm):
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