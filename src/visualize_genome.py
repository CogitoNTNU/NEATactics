import networkx as nx
import matplotlib.pyplot as plt
from nodes import Genome

def visualize_genome(genome: Genome):
    G = nx.DiGraph()
    for node in genome.nodes:
        G.add_node(node.id, layer_number = node.layer_number)
    for connection in genome.connections:
        if connection.is_enabled:
            G.add_edge(connection.in_node.id, connection.out_node.id, weight = connection.weight)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()