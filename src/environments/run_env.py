import time
from src.environments.mario_env import MarioJoypadSpace, StepResult
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
from typing import Tuple
from src.utils.utils import save_state_as_png
from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
from src.visualization.visualize_genome import visualize_genome
import numpy as np
from src.environments.fitness_function import Fitness
from src.utils.config import Config
import warnings

def env_init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment."
    warnings.filterwarnings("ignore")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.")
        ENV_NAME = "SuperMarioBros-v3"
        env = gym_super_mario_bros.make(ENV_NAME)
        env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
        env.metadata['render_modes'] = "rgb_array" # rgb_array, human
        env.metadata['render_fps'] = 10000
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def env_init_with_animation() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment."
    warnings.filterwarnings("ignore")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.")
        ENV_NAME = "SuperMarioBros-v3"
        env = gym_super_mario_bros.make(ENV_NAME)
        env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
        env.metadata['render_modes'] = "human" # rgb_array, human
        env.metadata['render_fps'] = 10000
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def insert_input(genome:Genome, state: list) -> None:
    """
    Insert the state of the game into the input nodes of the genome.
    """
    config = Config()
    start_idx_input_node = config.num_output_nodes
    num_input_nodes = config.num_input_nodes
    
    for i, node in enumerate(genome.nodes[start_idx_input_node:start_idx_input_node+num_input_nodes]): # get all input nodes
        node.value = state[i//20][i % 20] # (Not sure if this is correct)

def run_game(env: MarioJoypadSpace, genome: Genome):
    forward = Traverse(genome)
    fitness = Fitness()
    sr = env.step(0)
    i = 0
    timeout = 400
    while not sr.done:
        insert_input(genome, sr.state)
        action = forward.traverse() 
        sr = env.step(action) # State, Reward, Done, Info
        fitness.calculate_fitness(sr.info, action)

        if sr.info["life"] == 1 or i > timeout:
            reward = fitness.get_fitness()
            env.close()
            return reward
        i+=1
    env.close()
    return -1000

def run_game_with_animation(env: MarioJoypadSpace, genome: Genome, num: int):
    forward = Traverse(genome)
    fitness = Fitness()
    sr = env.step(0)
    i = 0
    timeout = 500
    while not sr.done:
        time.sleep(0.01)
        insert_input(genome, sr.state)
        action = forward.traverse() 
        sr = env.step(action) # State, Reward, Done, Info
        if i == 0:
            save_state_as_png(i + 1, sr.state)
            visualize_genome(genome, num)
            i += 1
        fitness.calculate_fitness(sr.info, action)

        if sr.info["life"] == 1 or i > timeout:
            reward = fitness.get_fitness()
            env.close()
            return reward
        env.render()    
    env.close()
    return -1000
