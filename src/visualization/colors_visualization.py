from src.utils.utils import normalize_negative_values, normalize_positive_values
import numpy as np
from typing import List
import matplotlib.cm as cm
from src.genetics.node import Node

GREEN = cm.Greens # type: ignore
GRAY = cm.gray # type: ignore
RED = cm.Reds # type: ignore

def get_node_colz(nodez: List[Node]) -> List[float]:

    input_vals, hidden_vals, output_vals = [], [], []
    for node in nodez:
        if node.type == 'input':
            input_vals.append(node.value)
        if node.type == 'hidden':
            hidden_vals.append(node.value)
        if node.type == 'output':
            output_vals.append(node.value)
    
    npout = np.array(output_vals)
    normalize_positive_values(npout)
    hidden_colz = get_weight_color(hidden_vals)

    hidden_idx, output_idx = 0, 0
    colors = []

    for node in nodez:
        if node.type == 'input':
            color = GRAY(node.value) # For input nodes, use their value directly
        elif node.type == 'hidden':
            color = hidden_colz[hidden_idx]
            hidden_idx += 1
        elif node.type == 'output':
            color = GREEN(npout[output_idx])
            output_idx += 1
        colors.append(color)

    return colors
 

def get_weight_color(edge_weights: List[float]) -> List[float]:
    """Input: A list of weights for the genome, in sorted order.\n
    Output: A list of RGBA values."""

    norm_negative = np.array([w for w in edge_weights if w < 0])
    norm_positive = np.array([w for w in edge_weights if w >= 0])
    normalize_negative_values(norm_negative)
    normalize_positive_values(norm_positive)
    
    edge_colors = [] # Create a full edge color list matching original order
    index_neg, index_pos = 0, 0  # To track position in the normalized lists 

    for w in edge_weights:
        if w < 0:
            edge_colors.append(RED(norm_negative[index_neg]))  # type: ignore | Map negative weight to red shade
            index_neg += 1
        else:
            edge_colors.append(GREEN(norm_positive[index_pos]))  # type: ignore | positive weight to green shade
            index_pos += 1

    return edge_colors

