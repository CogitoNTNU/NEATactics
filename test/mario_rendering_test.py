from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

def test_gym_environment():
    ENV_NAME = "SuperMarioBros-v0"

    env = gym_super_mario_bros.make(ENV_NAME)
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    env.metadata['render_fps'] = 10000
    env.metadata["render_modes"] = "human"
    env.reset()

    for _ in range(100):
        action = SIMPLE_MOVEMENT.index(["right"])
        _, _, done, _ = env.step(action) # State, Reward, Done, Info
        if done:
            _ = env.reset() # Discarding the final state.
        env.render()
    env.close()
