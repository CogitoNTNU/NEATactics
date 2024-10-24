from src.environments.mario_env import MarioJoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import RIGHT_ONLY
import warnings

def test_gym_environment():
    ENV_NAME = "SuperMarioBros-v0"

    warnings.filterwarnings("ignore")
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, RIGHT_ONLY)
    env.metadata['render_modes'] = "rgb_array"
    env.metadata['render_fps'] = 60
    env.reset()

    for _ in range(100):
        action = RIGHT_ONLY.index(["right"])
        sr = env.step(action) # State, Reward, Done, Info
        
        if sr.done:
            _ = env.reset() # Discarding the new state
        env.render()
    env.close()
