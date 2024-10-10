from src.genetics.genome import Genome
from src.utils.config import Config
import matplotlib.pyplot as plt
import numpy as np
import os

def save_state_as_png(i, state: np.ndarray) -> None:
    """Save a frame."""
    directory = "./mario_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imsave(f"./mario_frames/frame{i}.png", state, cmap='gray', vmin=0, vmax=1)

def normalize_positive_values(positive_vals: np.ndarray) -> None:
    """Takes an ndarray with positive floats as inputs,
    and modifies the array such that all values end up in the range [0, 1]"""
    if len(positive_vals) > 0:
        wmin, wmax = 0, positive_vals.max()
        if wmax == 0:
            positive_vals.fill(0)
            return
        positive_vals -= wmin # Normalize positives to [0, 1]
        positive_vals /= (wmax-wmin)  

def normalize_negative_values(negative_vals: np.ndarray) -> None:
    """Takes an ndarray with negative floats as inputs,
    and modifies the array such that all values end up in the range [0, 1],
    where the most negative input gets the value 1."""
    negative_vals *= -1
    normalize_positive_values(negative_vals)

def insert_input(genome:Genome, state: np.ndarray) -> None:
    """Insert the state of the game into the input nodes of the genome."""
    config = Config()
    start_idx_input_node = config.num_output_nodes
    num_input_nodes = config.num_input_nodes
    num_columns = config.input_shape[-1]
    
    for i, node in enumerate(genome.nodes[start_idx_input_node:start_idx_input_node+num_input_nodes]): # get all input nodes
        node.value = state[i//num_columns][i % num_columns]
