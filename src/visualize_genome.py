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
                row = i // 10  # There are 10 rows, so row is determined by i % 10
                col = i % 10  # Columns are determined by i // 10
                pos[node] = (x_pos + col * 0.5, -row * node_gap)  # Adjust x (columns) and y (rows)
        elif layer_idx == total_layers - 1:  # Output layer case
            x_pos = total_layers * layer_gap  # Place output nodes at the farthest right
            y_start = -(len(layer) - 1) * node_gap * 2   # Center the output nodes vertically
            for i, node in enumerate(layer):
                pos[node] = (x_pos, y_start + i * node_gap)  # Place nodes vertically
        else:
            # Hidden layers are placed regularly between the input and output layers
            x_pos = layer_idx * layer_gap  # Horizontal position for hidden layers
            y_start = -(len(layer) - 1) * node_gap / 2  # Center the layer vertically
            for i, node in enumerate(layer):
                pos[node] = (x_pos, y_start + i * node_gap)  # Place nodes vertically
    
    return pos



def visualize_genome(genome: Genome):
    G = nx.DiGraph()
    for node in genome.nodes:
        if node.type == 'Input':
            G.add_node(node.id, layer_number = 0)
        elif node.type == 'Hidden':
            G.add_node(node.id, layer_number = 1)
        elif node.type == 'Output':
            G.add_node(node.id, layer_number = 2)
    for connection in genome.connections:
        if connection.is_enabled:
            G.add_edge(connection.in_node.id, connection.out_node.id, weight = connection.weight)
    colors_node = []
    for node in genome.nodes:
        colors_node.append(get_color(node.type, node.value))


    layers = [[] for _ in range(3)]
    for node in genome.nodes:
        if node.type == 'Input':
            layers[0].append(node.id)
        elif node.type == 'Hidden':
            layers[1].append(node.id)
        else:
            layers[2].append(node.id)
    pos = create_custom_layout(G, layers)
    nx.draw(G, pos, with_labels=True, edge_color='b', node_size=500, font_size=8, font_color='w', font_weight='bold', node_color=colors_node)
    plt.show()


def get_color(type: str, value: float) -> str:
    """
    Takes a value which is assumed to be in range [0, 1],
    and returns a simple string like 'r' which representsn the color.
    """
    if type == 'input':
        if value < 0.25:
            return 'b'
        elif value < 0.5:
            return 'g'
        elif value < 0.75:
            return 'y'
        else:
            return 'r'

    else:
        return 'g'