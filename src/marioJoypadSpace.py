import numpy as np
from nes_py.wrappers import JoypadSpace
from collections import namedtuple

StepResult = namedtuple('StepResult', ['state', 'reward', 'done', 'info'])

class MarioJoypadSpace(JoypadSpace):
    """A custom JoypadSpace makes the type hinter happy :)"""

    def reset(self) -> np.ndarray:
        """Reset the environment, and return the initial state."""
        return self.interpret_state(np.array(super().reset()))
    
    def step(self, action: int) -> StepResult:
        """Perform an action, and get the next frame."""
        state, reward, done, info = super().step(action)
        # Convert to greyscale and downsample, cut image.
        # state = self.interpret_state()
        return StepResult(state, reward, done, info)
    
    def interpret_state(self, state: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    