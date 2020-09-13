from algorithms.test_generators import *
from algorithms.common import apply_retiming


def test_all_weight_one():
    for n in [10, 100, 1000]:
        graph = generate_all_weight_one_graph(num_nodes=n)

        for edge in graph.edges:
            assert graph.edges[edge]['weight'] == 1.0


def test_random_retiming():
    for n in range(100):
        graph = generate_all_weight_one_graph(num_nodes=n)
        r = get_random_retiming(graph)
        g_r = apply_retiming(graph, r)
        assert check_legality(g_r)