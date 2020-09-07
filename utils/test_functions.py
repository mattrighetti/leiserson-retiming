import networkx as nx


def is_retiming_legal(graph: nx.DiGraph) -> bool:
    for e in graph.edges:
        if graph.edges[e]["weight"] < 0:
            return False
    return True
