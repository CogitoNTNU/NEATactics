import numpy as np
from nes_py.wrappers import JoypadSpace
from collections import namedtuple
from skimage.transform import resize

StepResult = namedtuple('StepResult', ['state', 'reward', 'done', 'info'])

class MarioJoypadSpace(JoypadSpace):
    """A custom JoypadSpace makes the type hinter happy :)"""

    def __init__(self, env, actions):
        super().__init__(env, actions)
        # Potentially add extra variables here.

    def reset(self) -> np.ndarray:
        """Reset the environment, and return the initial state."""
        return np.array(super().reset())
        ## return self.interpret_state(np.array(super().reset()))
    
    def step(self, action: int) -> StepResult:
        """Perform an action, and get the next frame."""
        state, reward, done, info = super().step(action)
        # Convert to greyscale and downsample, cut image.
        state = self.interpret_state(state)
        return StepResult(state, reward, done, info)
    
    def interpret_state(self, state: np.ndarray) -> np.ndarray:
        # We get a np.ndarray with shape (240, 256, 3)

        # Cut the picture
        state = state[80:216]
        

        # Convert to grayscale
        state = np.dot(state[..., :3], [0.2989, 0.5870, 0.1140])  # Grayscale conversion
        state = state.astype(np.uint8)
        # Reduce pixel count
        state = resize(state, (10, 20), anti_aliasing=False, preserve_range=True).astype(np.uint8)
        
        
        return np.array(state)
