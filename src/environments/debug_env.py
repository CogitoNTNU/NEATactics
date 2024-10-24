from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
from src.environments.fitness_function import Fitness
from src.environments.mario_env import MarioJoypadSpace
from src.visualization.visualize_genome import visualize_genome
from src.utils.utils import save_state_as_png
from src.utils.utils import insert_input
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from typing import Tuple
import numpy as np
import time

def env_debug_init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment in human_mode"
    ENV_NAME = "SuperMarioBros-v1"
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
    env.metadata['render_modes'] = "rgb_array"
    env.metadata['render_fps'] = 144
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def run_game_debug(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome, num: int, visualize: bool = True) -> float:
    
    forward = Traverse(genome)
    fitness = Fitness()
    insert_input(genome, initial_state)
    last_fitness_val: float = 0
    stagnation_counter: float = 0
    i = 0
    max_fitness_val = 0
    
    while True:
        action = forward.traverse()
        time.sleep(0.01)
        sr = env.step(action) # State, Reward, Done, Info
        env.render()
        # timeout = 600 + sr.info["x_pos"]
        if visualize:
            save_state_as_png(0, sr.state)
            visualize_genome(genome, 0)
        
        fitness.calculate_fitness(sr.info, action)
        fitness_val: float = fitness.get_fitness()
        if fitness_val > max_fitness_val:
            max_fitness_val = fitness_val
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        if i % 15 == 0:
            print(fitness_val)
        if sr.info["life"] == 1 or stagnation_counter > 150:
            env.close()
            return fitness.get_fitness()
        i += 1
        insert_input(genome, sr.state)
