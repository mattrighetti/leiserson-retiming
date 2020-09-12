import pytest
import networkx as nx
from utils.algorithms.opt1 import opt1
from utils.algorithms.clock_period import cp
from utils.algorithms.test_generators import generate_all_weight_one_graph


def test_opt1():
    graph = nx.DiGraph()
    graph.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 7})
    ])
    graph.add_weighted_edges_from([(0, 1, 2.0),
                                   (1, 2, 0.0),
                                   (1, 3, 0.0),
                                   (2, 3, 0.0),
                                   (3, 0, 0.0)])
    result = opt1(graph)

    assert result[0] == 7.0
    assert len(result[1]) == graph.number_of_nodes()

    for key in [0, 1, 2, 3]:
        if key not in result[1]:
            pytest.fail(f'{key} was not found in retiming values')

    values = [0, -1, -1, 0]
    for i in range(len(values)):
        assert result[1][i] == values[i]

    graph = nx.DiGraph()
    graph.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 3}),
        (4, {'delay': 3}),
        (5, {'delay': 7}),
        (6, {'delay': 7}),
        (7, {'delay': 7})
    ])
    graph.add_weighted_edges_from([(0, 1, 1.0),
                                   (1, 2, 1.0),
                                   (2, 3, 1.0),
                                   (3, 4, 1.0),
                                   (4, 5, 0.0),
                                   (5, 6, 0.0),
                                   (6, 7, 0.0),
                                   (7, 0, 0.0),
                                   (3, 5, 0.0),
                                   (1, 7, 0.0),
                                   (2, 6, 0.0)])

    result = opt1(graph)

    assert result[0] == 13.0
    assert len(result[1]) == graph.number_of_nodes()

    for key in [0, 1, 2, 3, 4, 5, 6, 7]:
        if key not in result[1]:
            pytest.fail(f'{key} was not found in retiming values')

    values = [0, -1, -1, -2, -2, -2, -1, 0]
    for i in range(len(values)):
        assert result[1][i] == values[i]


def test_random_opt1():
    for n in [10, 100, 1000]:
        graph = generate_all_weight_one_graph(n)
        assert opt1(graph)[0] == max(nx.get_node_attributes(graph, 'delay').values())