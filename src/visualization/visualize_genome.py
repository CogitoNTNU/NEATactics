import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from src.genetics.genome import Genome
from src.genetics.node import Node
import os
import random
from typing import List
from src.visualization.colors_visualization import get_weight_color, get_node_colz
from src.visualization.visualization_position_utils import get_position_dict

# Adjust the size of the visualization whiteboard for the NN:
GRAPH_XMIN = -1.5
GRAPH_XMAX = 17
GRAPH_YMIN = -21
GRAPH_YMAX = 3

def get_node_in_layers(genome: Genome) -> List[List[int]]:
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

def add_nodes_to_graph(graph: nx.DiGraph, genome: Genome):
    """Takes a graph and genome as input, and adds all of the nodes connected to that genome to the graph."""
    for node in genome.nodes:
        if node.type == 'input':
            graph.add_node(node.id, layer_number = 0)
        elif node.type == 'hidden':
            graph.add_node(node.id, layer_number = 1)
        elif node.type == 'output':
            graph.add_node(node.id, layer_number = 2)

def visualize_genome(genome: Genome, frame_number: int):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    G = nx.DiGraph()
    add_nodes_to_graph(G, genome) 
    edge_weights = []
    edges = []  # Track the edges explicitly

    for connection in genome.connections:
        if connection.is_enabled:
            edge = (connection.in_node.id, connection.out_node.id)
            G.add_edge(*edge, weight=connection.weight)
            edges.append(edge)  # Add edge to the list
            edge_weights.append(connection.weight) 

    node_colz = get_node_colz(list(genome.nodes)) # Make a copy of the genome.nodes list
    edge_colz = get_weight_color(edge_weights)
    
    layers = get_node_in_layers(genome)
    pos_dict = get_position_dict(layers)
    
    nx.draw(G, pos_dict, with_labels=True, edgelist=edges, edge_color=edge_colz, node_size=500,
            font_size=8, font_color='y', font_weight='bold',
            node_color=node_colz, ax=ax)

    fig.set_facecolor('#d4e6f1') # Background color of network popup.
    edge_labels = {(connection.in_node.id, connection.out_node.id): round(connection.weight, 2)
                   for connection in genome.connections if connection.is_enabled}
    nx.draw_networkx_edge_labels(G, pos_dict, edge_labels=edge_labels, font_size=8, ax=ax) 

    plt.xlim(GRAPH_XMIN, GRAPH_XMAX)
    plt.ylim(GRAPH_YMIN, GRAPH_YMAX)
    directory = "./genome_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(f'./genome_frames/genome_{frame_number}.png')
    plt.close()

   