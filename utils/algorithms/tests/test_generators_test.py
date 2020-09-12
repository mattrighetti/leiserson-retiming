import networkx as nx
from utils.algorithms.test_generators import *


def test_all_weight_one():
    for n in [10, 100, 1000]:
        graph = generate_all_weight_one_graph(num_nodes=n)

        for edge in graph.edges:
            assert graph.edges[edge]['weight'] == 1.0


def test_single_register():
    from functools import reduce

    for n in [10, 100, 1000]:
        graph = generate_single_register_graph(num_nodes=n)

        register_sum = reduce(lambda a, b: a+b, [graph.edges[e]['weight'] for e in graph.edges])

        assert register_sum == 1.0
        assert graph.edges[n-1, 0]['weight'] == 1.0