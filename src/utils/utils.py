import matplotlib.pyplot as plt
import numpy as np
import os

def save_state_as_png(i, state: np.ndarray) -> None:
    """
    Save a frame.
    """
    directory = "./mario_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imsave(f"./mario_frames/frame{i}.png", state, cmap='gray')
