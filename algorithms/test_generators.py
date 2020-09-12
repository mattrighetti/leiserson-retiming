import networkx as nx
from random import randint
from algorithms.common import remove_backward_cycles

__all__ = ['generate_all_weight_one_graph',
           'check_legality']


def generate_all_weight_one_graph(num_nodes=10, p=0.25) -> nx.DiGraph:
    circle_graph = nx.path_graph(num_nodes, create_using=nx.DiGraph)
    circle_graph.add_edge(num_nodes - 1, 0, weight=1.0)
    random_graph = nx.binomial_graph(n=num_nodes, p=p, seed=27, directed=True)

    graph = nx.compose(circle_graph, random_graph)

    for edge in graph.edges:
        graph.edges[edge]["weight"] = 1.0

    for node in graph.nodes:
        graph.nodes[node]["delay"] = randint(1, 10)

    graph = remove_backward_cycles(graph)
    return graph


def check_legality(graph: nx.DiGraph) -> bool:
    for edge in graph.edges:
        if graph.edges[edge]['weight'] < 0:
            return False

    return True