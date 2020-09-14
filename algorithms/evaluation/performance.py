import os
import time
import os.path
import numpy as np
from os import path
import networkx as nx
from algorithms.wd import wd
from datetime import datetime
from algorithms.test_generators import *
from memory_profiler import memory_usage
from algorithms.retiming.strategies import *
from algorithms.common import apply_retiming
from io_utils.plot_utils import save_graph_to_file
from io_utils.plot_utils import read_graph_from_file


def create_graph_files():
    """
    Creates graph files that can be used to perform evaluation on. Test graphs will be written in the root
    directory in a folder named `tests_dot`

    :return: None
    """
    current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))
    print("Writing files in ", current_dir_path)

    for n in [100, 200, 300, 400, 500, 1000]:
        graph = generate_all_weight_one_graph(n, 0)

        for i in range(5):
            r = get_random_retiming(graph)
            g_r = apply_retiming(graph, r)

            print("Saving ", str(current_dir_path) + f'/{i}_{n}.dot')
            save_graph_to_file(g_r, str(current_dir_path) + f'/{i}_{n}.dot')


def test_opts():
    """
    Runs evaluation bot for OPT1 and OPT2 on a set of graph that are in `tests_dot` folder and writes the results
    to a `.csv` file

    :return: None
    """
    current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))

    dir_path = '../../results/'
    result_file = f'{dir_path}performance_{datetime.now().strftime("%H_%M_%S")}.csv'

    if not path.exists('../../results/'):
        os.makedirs(dir_path)

    if not path.exists(result_file):
        open(result_file, 'w').close()

    with open(result_file, 'w+') as ww:
        for file in os.listdir(current_dir_path):
            print("Testing ", file)
            graph = nx.DiGraph(read_graph_from_file(current_dir_path + '/' + file))

            num_edges = graph.number_of_edges()
            num_nodes = graph.number_of_nodes()

            W, D = get_W_D(current_dir_path + '/WD/' + file, graph)

            init = time.time()
            opt1(graph, W, D)
            mid = time.time()
            opt2(graph, W, D)
            end = time.time()

            opt1_time = mid - init
            opt2_time = end - mid
            print(f'{file}, {num_nodes}, {num_edges}, {opt1_time}, {opt2_time}\n')
            ww.write(f'{file}, {num_nodes}, {num_edges}, {opt1_time}, {opt2_time}\n')


def get_W_D(filepath, graph):
    """
    Utility function that stores WD matrices to lower execution time of the performance algorithm

    :param filepath: filepath where the matrices can be found
    :param graph: Graph that will be used to calculate W and D in case a file could not be found
    :return: W and D matrices
    """
    W_filepath = filepath + '_W'
    D_filepath = filepath + '_D'

    if path.exists(W_filepath) and path.exists(D_filepath):
        print(f"Reading {W_filepath} and {D_filepath}")
        W = np.loadtxt(W_filepath)
        D = np.loadtxt(D_filepath)
    else:
        print(f"Calculating {W_filepath} and {D_filepath}")
        W, D = wd(graph)
        np.savetxt(W_filepath, W)
        np.savetxt(D_filepath, D)

    return W, D


def perform_evaluation(function, filename='2_500.dot'):
    """
    Runs time evaluation of a specified graph saved on a file

    :param function: OPT1 or OPT2 algorithms
    :param filename: Filename of the graph file found in folder tests_dot/
    :raise Exception: If the passed function is not OPT1 or OPT2
    :return: Function to run evaluation of the specified algorithm
    """

    if function != opt1 and function != opt2:
        raise Exception(f'Cannot run performance evaluation on function {function}')

    def run_evaluation():
        """
        Runs time evaluation of the passed function, reading W and D from file to reduce calculation time

        :return: Prints execution time
        """
        current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))
        graph = nx.DiGraph(read_graph_from_file(current_dir_path + '/' + filename))

        W, D = get_W_D(current_dir_path + '/WD/' + filename, graph)

        init = time.time()
        function(graph, W, D)
        mid = time.time()

        time_delta = mid - init
        print(f'{filename}, took {time_delta:.2f}s\n')

    return run_evaluation


def profile_memory(function):
    """
    Performs memory evaluation on OPT1 and OPT2
    :param function: OPT1 or OPT2 functions
    :return: Function to profile either OPT1 and OPT2
    """
    def run_memory_profiling():
        """
        Function that retrieves the memory usage for a specified function

        :raise Exception: If the passed function is not OPT1 or OPT2
        :return: None
        """
        if function != opt1 and function != opt2:
            raise Exception(f"Cannot perform evaluation on function {function}")

        print("Evaluating memory for", function)
        usage, tuple_ = memory_usage(perform_evaluation(function), retval=True)
        usage = max(usage)
        print("Usage", usage)

    return run_memory_profiling


if __name__ == '__main__':
    profile_memory(opt1)()
    profile_memory(opt2)()