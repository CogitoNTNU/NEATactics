import numpy as np
import warnings
import time
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from typing import Tuple
from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
from src.environments.fitness_function import Fitness
from src.environments.mario_env import MarioJoypadSpace
from src.visualization.visualize_genome import visualize_genome
from src.utils.utils import save_state_as_png
from src.utils.utils import insert_input


def env_playback_init(environment) -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment in human_mode"
    ENV_NAME = f"SuperMarioBros-v{environment}"
    warnings.filterwarnings("ignore")
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
    env.metadata['render_modes'] = "rgb_array"
    env.metadata['render_fps'] = 144
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state


def run_game_playback(env: MarioJoypadSpace, initial_state: np.ndarray, genome: Genome, neat_name: str, visualize: bool = True, frame_queue=None) -> float:
    
    fitness = Fitness()
    i = 0
    
    while True:
        if i >= len(genome.actions)-1:
            env.close()
            return fitness.get_fitness()
        action = genome.actions[i]
        time.sleep(0.01)
        sr = env.step(action) # State, Reward, Done, Info
        
        # timeout = 600 + sr.info["x_pos"]
        if visualize and i % 1 == 0:
            save_state_as_png(i, sr.state, neat_name)
            visualize_genome(genome, neat_name, 0)
        
        fitness.calculate_fitness(sr.info, action)

        fitness_val: float = fitness.get_fitness()
        print(fitness_val)

        
        env.render()
        i += 1
        insert_input(genome, sr.state)