import os
import time
import networkx as nx
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


def perform_evaluation():
    current_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'tests_dot'))

    with open('../../performance.csv', 'a') as ww:
        for file in os.listdir(current_dir_path):
            print("Testing ", file)
            graph = nx.DiGraph(read_graph_from_file(current_dir_path + '/' + file))

            init = time.time()
            opt1(graph)
            mid = time.time()
            opt2(graph)
            end = time.time()

            opt1_time = mid - init
            opt2_time = end - mid

            ww.write(f'{file}, {opt1_time}, {opt2_time}\n')


if __name__ == '__main__':
    perform_evaluation()