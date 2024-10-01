import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
from typing import Union, List


def save_state_as_png(i, state: np.ndarray) -> None:
    """
    Save a frame.
    """
    directory = "./mario_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imsave(f"./mario_frames/frame{i}.png", state, cmap='gray', vmin=0, vmax=1)

def get_node_color(type: str, value: float) -> Union[str, float]:
    """
    Takes a value which is assumed to be in range [0, 1],
    and returns a simple string like 'r' which representsn the color.
    """
    if type == 'input':
        return value

    if type == 'hidden':
        return 0.384

    if type == 'output':
        return 0.796 # TODO: Try to see if passing 'r' is stable.

    raise ValueError(f"Encountered invalid type: {type}")

def get_weight_color(edge_weights: List[float]) -> List[float]:
    """
    Input: A list of weights for the genome, in sorted order.
    """
    negative_weights = np.array([w for w in edge_weights if w < 0])
    positive_weights = np.array([w for w in edge_weights if w >= 0])

    # Normalize negative and positive weights separately
    if len(negative_weights) > 0:
        wmin, wmax = negative_weights.min(), 0
        norm_negative = (negative_weights - wmax) / (wmin - wmax)  # Normalize negatives to [0, 1]
    else:
        norm_negative = []

    if len(positive_weights) > 0:
        wmin, wmax = 0, positive_weights.max()
        norm_positive = (positive_weights - wmin) / (wmax - wmin)  # Normalize positives to [0, 1]
    else:
        norm_positive = []

    
    edge_colors = [] # Create a full edge color list matching original order
    cmap_red = cm.Reds  # type: ignore
    cmap_green = cm.Greens  # type: ignore
    index_neg, index_pos = 0, 0  # To track position in the normalized lists 

    weight_valz = np.array(edge_weights)

    for w in edge_weights:
        if w < 0:
            edge_colors.append(cmap_red(norm_negative[index_neg]))  # Map negative weight to red shade
            index_neg += 1
        else:
            edge_colors.append(cmap_green(norm_positive[index_pos]))  # Map positive weight to green shade
            index_pos += 1

    return edge_colors
