from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

ENV_NAME = "SuperMarioBros-v0"

env = gym_super_mario_bros.make(ENV_NAME)
env = JoypadSpace(env, SIMPLE_MOVEMENT)
env.metadata['render_fps'] = 10000
env.metadata["render_modes"] = "human"

done = True
for step in range(5000):
    action = SIMPLE_MOVEMENT.index(["right"])
    if done:
        state = env.reset()
    state, reward, done, info = env.step(action)
    print(info)
    
    env.render()

env.close()
