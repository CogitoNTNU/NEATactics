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

def env_debug_init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment in human_mode"
    ENV_NAME = "SuperMarioBros-v3"
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
    env.metadata['render_modes'] = "human"
    env.metadata['render_fps'] = 144
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def run_game_debug(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome):
    
    forward = Traverse(genome)
    fitness = Fitness("Hallo") # TODO this probably needs to get fixed
    i = 0
    timeout = 250
    insert_input(genome, initial_state)

    while True:
        action = forward.traverse() 
        sr = env.step(action) # State, Reward, Done, Info
        if i == 1 and genome.id % 10 == 0:
            save_state_as_png(i + 1, sr.state)
            visualize_genome(genome, genome.id)
        
        fitness.calculate_fitness(sr.info, action)

        if sr.info["life"] == 1 or i > timeout:
            env.close()
            return fitness.get_fitness()
            
        i += 1
        insert_input(genome, sr.state)