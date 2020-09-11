import networkx as nx
from utils.algorithms.clock_period import *


def test_cp():
    graph1 = nx.DiGraph()
    graph1.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 7})
    ])
    graph1.add_weighted_edges_from([(0, 1, 2.0),
                                    (1, 2, 0.0),
                                    (1, 3, 0.0),
                                    (2, 3, 0.0),
                                    (3, 0, 0.0)])

    graph2 = nx.DiGraph()
    graph2.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 3}),
        (4, {'delay': 3}),
        (5, {'delay': 7}),
        (6, {'delay': 7}),
        (7, {'delay': 7})
    ])
    graph2.add_weighted_edges_from([(0, 1, 1.0),
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

    assert cp(graph1) == 13.0
    assert cp(graph2) == 24.0


def test_cp_delta():
    graph1 = nx.DiGraph()
    graph1.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 7})
    ])
    graph1.add_weighted_edges_from([(0, 1, 2.0),
                                    (1, 2, 0.0),
                                    (1, 3, 0.0),
                                    (2, 3, 0.0),
                                    (3, 0, 0.0)])

    graph2 = nx.DiGraph()
    graph2.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 3}),
        (3, {'delay': 3}),
        (4, {'delay': 3}),
        (5, {'delay': 7}),
        (6, {'delay': 7}),
        (7, {'delay': 7})
    ])
    graph2.add_weighted_edges_from([(0, 1, 1.0),
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

    graph3 = nx.DiGraph()
    graph3.add_nodes_from([
        (0, {'delay': 0}),
        (1, {'delay': 3}),
        (2, {'delay': 4}),
        (3, {'delay': 5}),
        (4, {'delay': 6}),
        (5, {'delay': 7})
    ])
    graph3.add_weighted_edges_from([(0, 1, 2.0),
                                    (1, 2, 2.0),
                                    (2, 3, 0.0),
                                    (3, 4, 0.0),
                                    (2, 4, 0.0),
                                    (4, 5, 0.0),
                                    (5, 0, 0.0)])

    deltas_1 = delta_cp(graph1)
    deltas_2 = delta_cp(graph2)
    deltas_3 = delta_cp(graph3)

    assert deltas_1[0] == 13.0
    assert deltas_1[1] == 3.0
    assert deltas_1[2] == 6.0
    assert deltas_1[3] == 13.0

    assert deltas_2[0] == 24.0
    assert deltas_2[1] == 3.0
    assert deltas_2[2] == 3.0
    assert deltas_2[3] == 3.0
    assert deltas_2[4] == 3.0
    assert deltas_2[5] == 10.0
    assert deltas_2[6] == 17.0
    assert deltas_2[7] == 24.0

    assert deltas_3[0] == 22.0
    assert deltas_3[1] == 3.0
    assert deltas_3[2] == 4.0
    assert deltas_3[3] == 9.0
    assert deltas_3[4] == 15.0
    assert deltas_3[5] == 22.0