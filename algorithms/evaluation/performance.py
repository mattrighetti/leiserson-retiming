import os
import time
import os.path
import numpy as np
from os import path
import networkx as nx
from algorithms.wd import wd
from algorithms.test_generators import *
from algorithms.retiming.strategies import *
from algorithms.common import apply_retiming
from io_utils.plot_utils import save_graph_to_file
from io_utils.plot_utils import read_graph_from_file


def create_graph_files():
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
    current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))

    with open('../../performance.csv', 'a') as ww:
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


def perform_evaluation(function):
    def run_evaluation():
        current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))

        with open('../../performance.csv', 'a') as ww:
            for file in os.listdir(current_dir_path):
                print("Testing ", file)
                graph = nx.DiGraph(read_graph_from_file(current_dir_path + '/' + file))

                init = time.time()
                function(graph)
                mid = time.time()

                opt1_time = mid - init
                print(f'{file}, {opt1_time}\n')
                ww.write(f'{file}, {opt1_time}\n')

    return run_evaluation


if __name__ == '__main__':
    test_opts()