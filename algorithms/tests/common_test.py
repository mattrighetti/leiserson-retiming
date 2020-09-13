import networkx as nx
import numpy as np
from algorithms.common import apply_retiming, check_if_legal


def test_apply_retiming():
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

    retiming = {
        0: 0.0,
        1: -1.0,
        2: -1.0,
        3: 0.0
    }

    original_graph = graph.copy()
    graph = apply_retiming(graph, retiming)

    assert graph.number_of_nodes() == original_graph.number_of_nodes()
    assert np.array_equal(graph.edges, original_graph.edges)
    assert np.array_equal(graph.nodes, original_graph.nodes)

    assert graph.edges[0, 1]['weight'] == 1.0
    assert graph.edges[1, 2]['weight'] == 0.0
    assert graph.edges[1, 3]['weight'] == 1.0
    assert graph.edges[2, 3]['weight'] == 1.0
    assert graph.edges[3, 0]['weight'] == 0.0


def test_legal_checker():
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

    retiming = {
        0: 0.0,
        1: -1.0,
        2: -1.0,
        3: 0.0
    }

    original_graph = graph.copy()
    graph = apply_retiming(graph, retiming)

    assert check_if_legal(original_graph)
    assert check_if_legal(graph)