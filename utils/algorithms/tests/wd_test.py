import numpy as np
import networkx as nx
from utils.algorithms.wd import wd


def test_wd():
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

    W, D = wd(graph)
    matrix_n = graph.number_of_nodes()

    W_test = np.empty([matrix_n, matrix_n], dtype=np.int)
    W_test[0, 1] = 2
    W_test[0, 2] = 2
    W_test[0, 3] = 2

    D_test = np.empty([matrix_n, matrix_n])
    D_test[0, 0] = 0
    D_test[0, 1] = 3
    D_test[0, 2] = 6
    D_test[0, 3] = 13
    D_test[1, 0] = 13
    D_test[1, 1] = 3
    D_test[1, 2] = 6
    D_test[1, 3] = 13
    D_test[2, 0] = 10
    D_test[2, 2] = 3
    D_test[2, 3] = 10
    D_test[3, 0] = 7
    D_test[3, 3] = 7

    assert W.shape == W_test.shape
    assert D.shape == D_test.shape

    assert W[0, 1] == W_test[0, 1]
    assert W[0, 2] == W_test[0, 2]
    assert W[0, 3] == W_test[0, 3]

    assert D[0, 1] == D_test[0, 1]
    assert D[0, 1] == D_test[0, 1]
    assert D[0, 2] == D_test[0, 2]
    assert D[0, 3] == D_test[0, 3]
    assert D[1, 0] == D_test[1, 0]
    assert D[1, 1] == D_test[1, 1]
    assert D[1, 2] == D_test[1, 2]
    assert D[1, 3] == D_test[1, 3]
    assert D[2, 0] == D_test[2, 0]
    assert D[2, 2] == D_test[2, 2]
    assert D[2, 3] == D_test[2, 3]
    assert D[3, 0] == D_test[3, 0]
    assert D[3, 3] == D_test[3, 3]