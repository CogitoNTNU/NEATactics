import random
from typing import List, Dict, Tuple
from src.visualization.viz_config import HORIZONTAL_GAP_INPUT, VERTICAL_GAP, LAYER_GAP_OUTPUT, BOX_HEIGHT

def get_position_dict(layers: List[List[int]]) -> Dict[int, Tuple[float, float]]:
    """
    Creates a custom layout for the graph G, ensuring nodes are separated by layers.
    
    :param layers: A list of lists, where each inner list contains the nodes in that layer.
    :return: A dictionary with node positions suitable for visualization.
    """
    pos = {}
    total_layers = len(layers) # Total number of layers (currently 3: input, hidden, output)
    random.seed(10)
    
    for layer_idx, layer in enumerate(layers): # Loop through layers and assign positions
        if layer_idx == 0:
            get_input_pos(pos, layer)
        elif layer_idx == total_layers - 1:
            get_output_pos(pos, layer, total_layers)
        else:
            get_hidden_pos(pos, layer)
    return pos

def get_input_pos(pos: Dict[int, Tuple[float, float]], layer: List[int]):
    x_pos = 0  # Input layer starts at the far left
    for i, node in enumerate(layer[:-1]): # Organize the first layer into a 20x10 grid, starting from top-left (0,0)
        row = i // 20  # There are 10 rows, so row is determined by i // 20
        col = i % 20  # Columns are determined by i % 20
        pos[node] = (x_pos + col * HORIZONTAL_GAP_INPUT, -row * VERTICAL_GAP)  # Adjust x (columns) and y (rows)
    pos[layer[-1]] = ((x_pos + 19 * HORIZONTAL_GAP_INPUT), -10 * VERTICAL_GAP) # bias node

def get_hidden_pos(pos: Dict[int, Tuple[float, float]], layer: List[int]):
    # Hidden layers are placed regularly between the input and output layers
    y_start = -(len(layer) - 1) * VERTICAL_GAP / 2  # Center the layer vertically
    for i, node in enumerate(layer):
        x_pos = round(random.uniform(10.5, 14.5), 2)
        y_pos = round(random.uniform(0, 18), 2)
        pos[node] = (x_pos, -y_pos)  # Place nodes vertically
    
def get_output_pos(pos: Dict[int, Tuple[float, float]], layer: List[int], total_layers: int):
    x_pos = total_layers * LAYER_GAP_OUTPUT   # Place output nodes at the farthest right
    y_gap = (BOX_HEIGHT) / (len(layer))  # Center the output layer vertically
    
    for i, node in enumerate(layer):
        y_pos = - y_gap * i - y_gap/2
        pos[node] = (x_pos, y_pos)  # Place nodes vertically


