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

def normalize_positive_values(positive_vals: np.ndarray) -> None:
    """Takes an ndarray with positive floats as inputs,
    and modifies the array such that all values end up in the range [0, 1]"""
    if len(positive_vals) > 0:
        wmin, wmax = 0, positive_vals.max()
        if wmax == 0:
            positive_vals = np.zeros(len(positive_vals))
            return
        positive_vals = (positive_vals - wmin) / (wmax - wmin)  # Normalize positives to [0, 1]

def normalize_negative_values(negative_vals: np.ndarray) -> None:
    """Takes an ndarray with negative floats as inputs,
    and modifies the array such that all values end up in the range [0, 1],
    where the most negative input gets the value 1."""
    normalize_positive_values(negative_vals.__neg__())


