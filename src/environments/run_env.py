from src.environments.mario_env import MarioJoypadSpace, StepResult
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
from typing import Tuple
from src.utils.utils import save_state_as_png, insert_input
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
        env.metadata['render_modes'] = "rgb_array"
        env.metadata['render_fps'] = 10000
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def run_game(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome):
    
    forward = Traverse(genome)
    fitness = Fitness("Hallo") # TODO this probably needs to get fixed
    i = 0
    timeout = 250
    insert_input(genome, initial_state)
    
    while True:
        action = forward.traverse() 
        sr = env.step(action)
        fitness.calculate_fitness(sr.info, action)

        if sr.info["life"] == 1 or i > timeout or sr.done: # What is happening here?
            env.close()
            return fitness.get_fitness()
            
        insert_input(genome, sr.state) # Prepare for next iteration
        i += 1
