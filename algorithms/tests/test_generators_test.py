from algorithms.test_generators import *


def test_all_weight_one():
    for n in [10, 100, 1000]:
        graph = generate_all_weight_one_graph(num_nodes=n)

        for edge in graph.edges:
            assert graph.edges[edge]['weight'] == 1.0