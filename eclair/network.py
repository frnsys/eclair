import networkx as nx
from collections import defaultdict


def build_network(emails, min_degree=2):
    G = nx.DiGraph()
    senders = {e.sender.address for e in emails}

    edges = defaultdict(lambda: {'weight':0})
    for e in emails:
        for r in e.recipients:
            edge = (e.sender.address, r.address)
            edges[edge]['weight'] += 1

    # Normalize weights
    max_edge = max(edges, key=lambda k: edges[k]['weight'])
    max_weight = float(edges[max_edge]['weight'])
    for edge, meta in edges.items():
        edges[edge]['n_weight'] = meta['weight']/max_weight

    # Mutate into proper format for graph edges
    edges = [x + (y,) for x, y in edges.items()]

    G.add_nodes_from(senders)
    G.add_edges_from(edges)

    # Filter to nodes with degree of at least `min_degree`
    for node in G.nodes():
        deg = G.degree(node)
        if deg < min_degree:
            G.remove_node(node)
        else:
            G.node[node]['degree'] = deg

    return G
