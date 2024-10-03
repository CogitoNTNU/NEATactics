from src.utils.utils import normalize_negative_values, normalize_positive_values
import numpy as np
from typing import Union, List
import matplotlib.cm as cm

GREEN = cm.Greens # type: ignore
GRAY = cm.gray # type: ignore
RED = cm.Reds # type: ignore

def get_node_color(type: str, value: float) -> Union[str, float]:
    """
    Takes a value which is assumed to be in range [0, 1],
    and returns a simple string like 'r' which representsn the color.
    """
    if type == 'input':
        return GRAY(value)

    if type == 'hidden':
        return RED(value)

    if type == 'output':
        print(value)
        return GREEN(value) # TODO: Try to see if passing 'r' is stable.

    raise ValueError(f"Encountered invalid type: {type}")

def get_weight_color(edge_weights: List[float]) -> List[float]:
    """Input: A list of weights for the genome, in sorted order.\n
    Output: A list of RGBA values."""

    norm_negative = np.array([w for w in edge_weights if w < 0])
    normalize_negative_values(norm_negative)
    norm_positive = np.array([w for w in edge_weights if w >= 0])
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

