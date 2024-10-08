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
        env.metadata['render_modes'] = "rgb_array"
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

def run_game(env: MarioJoypadSpace, genome: Genome, debug = False):
    
    forward = Traverse(genome)
    fitness = Fitness("Hallo") # TODO this probably needs to get fixed
    sr = env.step(0)
    i = 0
    timeout = 250
    while not sr.done:
        insert_input(genome, sr.state)
        action = forward.traverse() 
        if action == -1:
            quit()
        sr = env.step(action) # State, Reward, Done, Info
        if i == 1 and genome.id % 10 == 0:
            # save_state_as_png(i + 1, sr.state)
            # visualize_genome(genome, genome.id)
            pass
        
        fitness.calculate_fitness(sr.info, action)

        if sr.info["life"] == 1 or i > timeout:
            # print(f"Game over at frame {i}.")
            reward = fitness.get_fitness()
            env.reset() # Discard the new initial state if done.
            # print(reward)
            env.close()
            return reward
            
        i += 1
    env.close()
    return -1000
