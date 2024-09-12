import networkx as nx
import matplotlib.pyplot as plt
from src.nodes import Genome

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
        x_pos = layer_idx * layer_gap  # Move each layer horizontally
        
        # Sort nodes by their ID (or any other property) to place the smallest at the top
        sorted_layer = sorted(layer)  # Sorting based on node ID by default
        
        y_start = -(len(sorted_layer) - 1) * node_gap / 2  # Center the layer vertically
        for i, node in enumerate(sorted_layer):
            pos[node] = (x_pos, y_start + i * node_gap)  # Place nodes vertically, shift horizontally by layer
    
    return pos

def visualize_genome(genome: Genome):
    G = nx.DiGraph()
    for node in genome.nodes:
        G.add_node(node.id, layer_number = node.layer_number)
    for connection in genome.connections:
        if connection.is_enabled:
            G.add_edge(connection.in_node.id, connection.out_node.id, weight = connection.weight)
    layers = [[] for _ in range(max([node.layer_number for node in genome.nodes]) + 1)]
    for node in genome.nodes:
        layers[node.layer_number].append(node.id)
    pos = create_custom_layout(G, layers)
    nx.draw(G, pos, with_labels=True)
    plt.show()