from src.environments.mario_env import MarioJoypadSpace, StepResult
import gym_super_mario_bros
from gym_super_mario_bros.actions import RIGHT_ONLY
import numpy as np
import time
from typing import Tuple
from src.utils.utils import save_state_as_png

def init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment. Returns the environment."

    ENV_NAME = "SuperMarioBros-v3"
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, RIGHT_ONLY) # Select available actions for AI
    env.metadata['render_modes'] = "human"
    env.metadata['render_fps'] = 144
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def test_gym_environment(env: MarioJoypadSpace):
    """Simulates 100 frames where your only action is to move right."""

    for i in range(200): # Simulate 200 frames.
        
        action = RIGHT_ONLY.index(["right"]) # Choose to go right
        sr = env.step(action) # State, Reward, Done, Info
        save_state_as_png(i + 1, sr.state) 
        time.sleep(0.02)
        print(sr.state)
        if sr.info["life"] == 2:
            print(f"Lost a life at frame {i}.")
        if sr.info["life"] == 0:
            print(f"Zero lives at fram: {i}.")
            
        if sr.done:
            print(f"Game over at frame {i}.")
            
            break
            _ = env.reset() # Discard the new initial state if done.

        env.render()

    env.close()
def get_state_from_environment(env: MarioJoypadSpace):
    """Simulates 100 frames where your only action is to move right."""

    for i in range(1): # Simulate 200 frames.
        
        action = RIGHT_ONLY.index(["right"]) # Choose to go right
        sr = env.step(action) # State, Reward, Done, Info
        
        print(sr.state)

        with open(f"state_frame_{i}.pkl", "wb") as f:
            pickle.dump(sr.state, f)
        
        if sr.info["life"] == 2:
            print(f"Lost a life at frame {i}.")
        if sr.info["life"] == 0:
            print(f"Zero lives at fram: {i}.")
            
        if sr.done:
            print(f"Game over at frame {i}.")
            
            break
            _ = env.reset() # Discard the new initial state if done.

        env.render()

    env.close()
def simulate_one_frame(env: MarioJoypadSpace) -> StepResult:
    return env.step(RIGHT_ONLY.index(["right"]))

if __name__ == '__main__':

    env, state = init()
    test_gym_environment(env)

    env, state = init()
    sr = simulate_one_frame(env)
    print(sr.reward)
    print(sr.info)

"""
Notes:

State is np.ndarray with shape (240, 256, 3)
240 represents the number of pixels in y-direction.
256 pixels in the x-direction.
3 numbers (r, g, b) for each pixel.

Thus:
state[i, j]
will index the picture the same way which you index a matrix.
i represents the row (counting from the top left), while j represents the column index.

Extra:
state[0] Will give you the pixel values of the first row.
state[:, 0, :] gives you the pixel values of the first column.


reward is a single float.
It is unclear what the reward float is based upon.

done is a boolean value, either True or False.
done = True if you die or grab the flag, else False.

info is a dictionary with length 10.

{
coins: int
flag_get: bool
life: int
score: int
stage: int
status: str
time: int
world: int
x_pos: int
y_pos: int
}
"""

