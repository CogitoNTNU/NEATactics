from src.environments.mario_env import MarioJoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
from typing import Tuple
from src.utils.utils import insert_input
from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
import numpy as np
from src.environments.fitness_function import Fitness
import warnings

def env_init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment."
    warnings.filterwarnings("ignore")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.")
        ENV_NAME = "SuperMarioBros-v1"
        env = gym_super_mario_bros.make(ENV_NAME)
        env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
        env.metadata['render_modes'] = "rgb_array"
        env.metadata['render_fps'] = 10000
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def run_game(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome):
    
    forward = Traverse(genome)
    fitness = Fitness()
    insert_input(genome, initial_state)
    
    last_fitness_val: float = 0
    stagnation_counter: float = 0

    while True:
        action = forward.traverse()
        # time.sleep(0.001)
        sr = env.step(action) # State, Reward, Done, Info
        genome.add_action(action)
        
        fitness.calculate_fitness(sr.info, action)

        fitness_val: float = fitness.get_fitness()
        if fitness_val > last_fitness_val:
            last_fitness_val = fitness_val
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if sr.info["life"] == 1 or stagnation_counter > 150:
            env.close()
            return fitness.get_fitness(), genome.actions
            
        insert_input(genome, sr.state)