import networkx as nx
import matplotlib.pyplot as plt
from src.nodes import Genome
from networkx.drawing.nx_pydot import graphviz_layout

def create_custom_layout(G, layers):
    """
    Creates a custom layout for the graph G, ensuring nodes are separated by layers.
    
    :param G: The directed graph (DiGraph) representing the neural network or genome.
    :param layers: A list of lists, where each inner list contains the nodes in that layer.
    :return: A dictionary with node positions suitable for visualization.
    """
    pos = {}
    layer_gap = 5  # Vertical gap between layers
    node_gap = 2   # Horizontal gap between nodes in the same layer
    
    # Loop through layers and assign positions
    for layer_idx, layer in enumerate(layers):
        y_pos = -layer_idx * layer_gap  # Move each layer vertically
        x_start = -(len(layer) - 1) * node_gap / 2  # Center the layer horizontally
        for i, node in enumerate(layer):
            pos[node] = (x_start + i * node_gap, y_pos)
    
    return pos

def visualize_genome(genome: Genome):
    G = nx.DiGraph()
    for node in genome.nodes:
        G.add_node(node.id, layer_number = node.layer_number)
    for connection in genome.connections:
        if connection.is_enabled:
            G.add_edge(connection.in_node.id, connection.out_node.id, weight = connection.weight)
    pos = create_custom_layout(G, 2)
    nx.draw(G, pos, with_labels=True)
    plt.show()