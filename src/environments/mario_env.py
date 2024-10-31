import numpy as np
from nes_py.wrappers import JoypadSpace
from skimage.transform import resize
from typing import NamedTuple, Dict, Any
import numpy as np
from gym.spaces import Box
from gym.core import ObservationWrapper
import numpy as np
import cv2
from skimage.transform import resize
from src.utils.config import Config

class StepResult(NamedTuple):
    """A namedtuple-like class representing the result of an environment step.
    
    Attributes:
        state (np.ndarray): The current state of the environment, processed and downsampled.
        reward (float): The reward obtained from the step.
        done (bool): Whether the game/episode is finished.
        info (dict): Additional information about the environment state, with the following keys:
            - coins (int): The number of coins collected.
            - flag_get (bool): Whether the flag has been reached.
            - life (int): The remaining life count.
            - score (int): The current score.
            - stage (int): The current stage number.
            - status (str): The player status (e.g., 'small', 'big', 'fire').
            - time (int): The remaining time in the level.
            - world (int): The current world number.
            - x_pos (int): The x-coordinate of the player.
            - y_pos (int): The y-coordinate of the player.
    """
    state: np.ndarray
    """The current state."""
    reward: float
    """The reward obtained when getting to this state."""
    done: bool
    """Whether you are finished playing or not."""
    info: Dict[str, Any]
    """A dictionary containing detailed information about the environment state."""


class MarioJoypadSpace(JoypadSpace):
    """A custom JoypadSpace makes the type hinter happy :)"""

    def __init__(self, env, actions):
        super().__init__(env, actions)
        self.config = Config()
        # Potentially add extra variables here.

    def reset(self) -> np.ndarray:
        """Reset the environment, and return the initial state."""
        return self.interpret_state(np.array(super().reset()))
    
    def step(self, action: int) -> StepResult:
        """Perform an action, and get the next frame."""
        state, reward, done, info = super().step(action)
        # Convert to greyscale and downsample, cut image.
        state = self.interpret_state(state)
        return StepResult(state, reward, done, info)
    
    # def interpret_state(self, state: np.ndarray) -> np.ndarray:
    #     """
    #     Preprocessing of state:\n
    #     Input:
    #     - ndarray with shape (240, 256, 3)\n
    #     Output:
    #     - ndarray with shape (20, 40)        
    #     """
    #     MAX_COLOR = 255
    #     state = state[80:216] # Cut the picture
        
    #     # Example: Limit to 4 colors
    #     state = np.dot(state[..., :3], [0.2989, 0.5870, 0.1140]) # Convert to grayscale
    #     state = state.astype(np.uint8) # Ensure valid grayscale value (can't be float)
        
    #     state = resize(state, (self.config.input_shape[0], self.config.input_shape[1]), anti_aliasing=True, preserve_range=True).astype(np.uint8) # Reduce pixel count.
        
    #     state = np.array(state)
    #     grayscale_pixel_values = state / MAX_COLOR
    #     return grayscale_pixel_values
    
    def interpret_state(self, state: np.ndarray) -> np.ndarray:
        """
        Preprocessing of state:
        Input:
        - ndarray with shape (240, 256, 3)
        Output:
        - ndarray with shape (20, 40, 3)
        """
        MAX_COLOR = 255
        
        # Cut the picture
        state = state[80:216]
        
        # Resize while preserving RGB channels
        state = resize(
            state, 
            (self.config.input_shape[0], self.config.input_shape[1], 3),
            anti_aliasing=True,
            preserve_range=True
        ).astype(np.uint8)
        
        # Normalize to [0,1] range
        return state / MAX_COLOR

class ResizeEnv(ObservationWrapper):
    def __init__(self, env, size):
        super(ResizeEnv, self).__init__(env)
        (oldh, oldw, oldc) = env.observation_space.shape
        newshape = (size, size, oldc)
        self.observation_space = Box(low=0, high=255, shape=newshape, dtype=np.uint8)

    def observation(self, frame):
        if self.observation_space.shape is not None:
            height, width, _ = self.observation_space.shape
        else:
            raise ValueError("Observation space shape is None")
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        if frame.ndim == 2:
            frame = frame[:, :, None]
        return frame