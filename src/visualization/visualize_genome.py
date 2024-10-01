import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from src.genetics.genome import Genome
from src.genetics.node import Node
import random
from typing import List
from src.utils.utils import get_node_color, get_weight_color

# Adjust the size of the visualization whiteboard for the NN:
GRAPH_XMIN = -1.5
GRAPH_XMAX = 17
GRAPH_YMIN = -20
GRAPH_YMAX = 3

def get_node_in_layers(genome: Genome) -> List[List[Node]]:
    """
    Input:
    - genome

    Output:
    - A list with shape (1, 3)\n

    The first list represents the nodes in the input layer.\n
    Seconds list: hidden layer.\n
    Third list: output layer.\n 
    """
    layers = [[] for _ in range(3)]
    for node in genome.nodes:
        if node.type == 'input':
            layers[0].append(node.id)
        elif node.type == 'hidden':
            layers[1].append(node.id)
        else:
            layers[2].append(node.id)
    return layers

def get_position_dict(layers):
    """
    Creates a custom layout for the graph G, ensuring nodes are separated by layers.
    
    :param G: The directed graph (DiGraph) representing the neural network or genome.
    :param layers: A list of lists, where each inner list contains the nodes in that layer.
    :return: A dictionary with node positions suitable for visualization.
    """
    pos = {}
    layer_gap = 5  # Horizontal gap between layers
    node_gap = 2   # Vertical gap between nodes in the same layer
    
    # Total number of layers
    total_layers = len(layers)
    
    # Loop through layers and assign positions
    for layer_idx, layer in enumerate(layers):
        # Special case for the input layer (first layer)
        if layer_idx == 0:
            x_pos = 0  # Input layer starts at the far left
            # Organize the first layer into a 20x10 grid, starting from top-left (0,0)
            for i, node in enumerate(layer):
                row = i // 20  # There are 10 rows, so row is determined by i // 20
                col = i % 20  # Columns are determined by i % 20
                pos[node] = (x_pos + col * 0.5, -row * node_gap)  # Adjust x (columns) and y (rows)
        elif layer_idx == total_layers - 1:  # Output layer case
            x_pos = total_layers * layer_gap   # Place output nodes at the farthest right
            y_start = -(len(layer) - 1) * node_gap * 2   # Center the output nodes vertically
            for i, node in enumerate(layer):
                pos[node] = (x_pos, y_start + 8 + i * node_gap)  # Place nodes vertically
        else:
            # Hidden layers are placed regularly between the input and output layers
            y_start = -(len(layer) - 1) * node_gap / 2  # Center the layer vertically
            for i, node in enumerate(layer):
                x_pos = round(random.uniform(10.5, 14.5), 2)
                pos[node] = (x_pos, y_start + i * node_gap)  # Place nodes vertically
    
    return pos

def add_nodes_to_graph(graph: nx.DiGraph, genome: Genome):
    """Takes a graph and genome as input, and adds all of the nodes connected to that genome to the graph."""
    for node in genome.nodes:
        if node.type == 'input':
            graph.add_node(node.id, layer_number = 0)
        elif node.type == 'hidden':
            graph.add_node(node.id, layer_number = 1)
        elif node.type == 'output':
            graph.add_node(node.id, layer_number = 2)

def visualize_genome(genome: Genome):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    G = nx.DiGraph()
    add_nodes_to_graph(G, genome) 

    edge_weights = []
    for connection in genome.connections:
        if connection.is_enabled:
            G.add_edge(connection.in_node.id, connection.out_node.id, weight = connection.weight)
            edge_weights.append(connection.weight)

    node_colz = [get_node_color(node.type, node.value) for node in genome.nodes]
    edge_colz = get_weight_color(edge_weights)
    
    layers = get_node_in_layers(genome)
    pos_dict = get_position_dict(layers)
    nx.draw(G, pos_dict, with_labels=True, edge_color=edge_colz, node_size=500,
            font_size=8, font_color='y', font_weight='bold',
            node_color=node_colz, cmap='gray', vmin=0, vmax=1, ax=ax)

    fig.set_facecolor('#d4e6f1') # Background color of network popup.
    
    plt.xlim(GRAPH_XMIN, GRAPH_XMAX)
    plt.ylim(GRAPH_YMIN, GRAPH_YMAX)
    plt.show()
   