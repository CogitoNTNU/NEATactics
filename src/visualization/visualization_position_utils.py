import random
from typing import List, Dict, Tuple
from src.visualization.viz_config import HORIZONTAL_GAP_INPUT, VERTICAL_GAP, NUM_INPUT_COLS, NUM_INPUT_ROWS, XSTART_INPUT, YSTART, XSTART_OUTPUT

INPUT_HEIGHT = NUM_INPUT_ROWS * VERTICAL_GAP
INPUT_XEND = XSTART_INPUT + HORIZONTAL_GAP_INPUT * (NUM_INPUT_COLS - 1)

def get_position_dict(layers: List[List[int]]) -> Dict[int, Tuple[float, float]]:
    """
    Creates a custom layout for the graph G, ensuring nodes are separated by layers.
    
    :param layers: A list of lists, where each inner list contains the nodes in that layer.
    :return: A dictionary with node positions suitable for visualization.
    """
    pos:  Dict[int, Tuple[float, float]] = {}
    total_layers = len(layers) # Total number of layers (currently 3: input, hidden, output)
    random.seed(10)
    
    for layer_idx, layer in enumerate(layers): # Loop through layers and assign positions
        if layer_idx == 0:
            get_input_pos(pos, layer)
        elif layer_idx == total_layers - 1:
            get_output_pos(pos, layer)
        else:
            get_hidden_pos(pos, layer)
    return pos

def get_input_pos(pos: Dict[int, Tuple[float, float]], layer: List[int]):
    """Provide positions to all input nodes. These input nodes consist of the state (which is a frame of the mario game) + a bias node."""
    for i, node in enumerate(layer[:-1:]): # Organize the first layer into a 20x10 grid, starting from top-left (0,0)
        row = i // NUM_INPUT_COLS  # There are 10 rows, so row is determined by i // 20
        col = i % NUM_INPUT_COLS  # Columns are determined by i % 20
        pos[node] = (XSTART_INPUT + col * HORIZONTAL_GAP_INPUT, YSTART + ((NUM_INPUT_ROWS - 1) - row) * VERTICAL_GAP)  # Adjust x (columns) and y (rows)
    pos[layer[-1]] = (INPUT_XEND, YSTART + NUM_INPUT_ROWS * VERTICAL_GAP) # bias node

def get_hidden_pos(pos: Dict[int, Tuple[float, float]], layer: List[int]):
    """Hidden nodes are currently being placed randomly within a pre-defined square box in the graph"""
    for node in layer:
        x_pos = round(random.uniform(INPUT_XEND + 0.5, XSTART_OUTPUT - 0.5), 2)
        y_pos = round(random.uniform(YSTART, YSTART + INPUT_HEIGHT), 2)
        pos[node] = (x_pos, y_pos)
    
def get_output_pos(pos: Dict[int, Tuple[float, float]], layer: List[int]):
    """Get positions for the output nodes. Each output node represents an action which can be taken in the environment. EXAMPLE: GO_RIGHT"""
    y_gap = NUM_INPUT_ROWS * VERTICAL_GAP / len(layer)
    for i, node in enumerate(layer):
        y_pos = YSTART + y_gap * i
        pos[node] = (XSTART_OUTPUT, y_pos)  # Place nodes vertically


