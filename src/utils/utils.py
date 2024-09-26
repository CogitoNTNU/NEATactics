import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Union

def save_state_as_png(i, state: np.ndarray) -> None:
    """
    Save a frame.
    """
    directory = "./mario_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imsave(f"./mario_frames/frame{i}.png", state, cmap='gray', vmin=0, vmax=1)

def get_color(type: str, value: float) -> Union[str, float]:
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
 