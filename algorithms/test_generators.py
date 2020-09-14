import networkx as nx
from random import randint
from algorithms.common import remove_backward_cycles

__all__ = ['generate_all_weight_one_graph',
           'check_legality',
           'get_random_retiming']


def generate_all_weight_one_graph(num_nodes=10, p=0.25) -> nx.DiGraph:
    """
    Generates a graph that has edge weight equal to 1.0

    :param num_nodes: Number of nodes that the graph must have
    :param p: Probability used by the graph generator to decide how dense the graph will be
    :return: Generated graph
    """
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
    """
    Checks if a graph satisfies condition W1 (all edges must have weight grater or equal than zero)
    provided in the paper

    :param graph: Graph on which to check condition W1
    :return: True if legal, False if not legal
    """
    for edge in graph.edges:
        if graph.edges[edge]['weight'] < 0:
            return False

    return True


def get_random_retiming(graph: nx.DiGraph) -> dict:
    """
    Generates a random and legal retiming on a graph that has weight 1.0 on all of its edges

    :param graph: nx.DiGraph with weight greater than zero on its edges
    :return: Legal retiming dictionary
    """
    r = dict([(node, 0) for node in graph.nodes])

    for node in graph.nodes:
        in_list = [e for e in graph.in_edges(node)]
        out_list = [e for e in graph.out_edges(node)]

        low = [weight - r[u] for ((u, v), weight) in nx.get_edge_attributes(graph, 'weight').items()
               if (u, v) in in_list]
        high = [weight + r[v] for ((u, v), weight) in nx.get_edge_attributes(graph, 'weight').items()
                if (u, v) in out_list]

        min_low = 0
        min_high = 0

        if len(low) > 0:
            min_low = -min(low)

        if len(high) > 0:
            min_high = min(high)

        r[node] = randint(min_low, min_high)

    return r