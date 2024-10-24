from src.genetics.genome import Genome
from src.utils.config import Config
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    # These imports will only be used for type hinting, not at runtime
    from src.genetics.NEAT import NEAT

def save_state_as_png(i, state: np.ndarray) -> None:
    """Save a frame."""
    directory = "./data/mario_frames"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imsave(f"./data/mario_frames/frame{i}.png", state, cmap='gray', vmin=0, vmax=1)

def normalize_positive_values(positive_vals: np.ndarray) -> None:
    """Takes an ndarray with positive floats as inputs,
    and modifies the array such that all values end up in the range [0, 1]"""
    if len(positive_vals) > 0:
        wmin, wmax = 0, positive_vals.max()
        if wmax == 0:
            positive_vals.fill(0)
            return
        positive_vals -= wmin # Normalize positives to [0, 1]
        positive_vals /= (wmax-wmin)  

def normalize_negative_values(negative_vals: np.ndarray) -> None:
    """Takes an ndarray with negative floats as inputs,
    and modifies the array such that all values end up in the range [0, 1],
    where the most negative input gets the value 1."""
    negative_vals *= -1
    normalize_positive_values(negative_vals)

def insert_input(genome:Genome, state: np.ndarray) -> None:
    """Insert the state of the game into the input nodes of the genome."""
    config = Config()
    start_idx_input_node = config.num_output_nodes
    num_input_nodes = config.num_input_nodes
    num_columns = config.input_shape[-1]
    
    for i, node in enumerate(genome.nodes[start_idx_input_node:start_idx_input_node+num_input_nodes]): # get all input nodes
        node.value = state[i//num_columns][i % num_columns]

def save_fitness(best: list, avg: list, min: list, append: bool = False):
    os.makedirs('data/fitness', exist_ok=True)
    with open("data/fitness/fitness_values.txt", "w") as f:
        for i in range(len(best)):
            f.write(f"Generation: {i} - Best: {best[i]} - Avg: {avg[i]} - Min: {min[i]}\n")

def save_best_genome(genome: Genome, generation: int):
    os.makedirs('data/good_genomes', exist_ok=True)
    with open(f'data/good_genomes/best_genome_{generation}.obj', 'wb') as f:
        pickle.dump(genome, f) # type: ignore

def load_best_genome(generation: int):
    if generation == -1:
        files = os.listdir('data/good_genomes')
        pattern = re.compile(r'best_genome_(\d+).obj')
        generations = []
        for file in files:
            match = pattern.match(file)
            if match:
                generations.append(int(match.group(1)))
        if generations:
            generation = max(generations)
            print("Loading best genome from generation:", generation)
        else:
            raise FileNotFoundError("No valid genome files found in 'data/good_genomes'.")
    
    with open(f'data/good_genomes/best_genome_{generation}.obj', 'rb') as f:
        return pickle.load(f)

def save_neat(neat: 'NEAT', name: str):
    os.makedirs('data/trained_population', exist_ok=True)
    with open(f'data/trained_population/neat_{name}.obj', 'wb') as f:
        pickle.dump(neat, f) # type: ignore
        
def load_neat(name: str):
    # Check if file exists first
    if not os.path.exists(f'data/trained_population/neat_{name}.obj'):
        return None
    with open(f'data/trained_population/neat_{name}.obj', 'rb') as f:
        return pickle.load(f) # type: ignore

# Function to read and parse the file
def read_fitness_file(filename):
    generations = []
    best_values = []
    avg_values = []
    min_values = []
    os.makedirs('data/fitness', exist_ok=True)

    # Open the file and extract data
    with open(filename, 'r') as file:
        for line in file:
            match = re.match(r"Generation: (\d+) - Best: ([\d\.]+) - Avg: ([\d\.]+) - Min: ([\d\.]+)", line)
            if match:
                generations.append(int(match.group(1)))
                best_values.append(float(match.group(2)))
                avg_values.append(float(match.group(3)))
                min_values.append(float(match.group(4)))

    return generations, best_values, avg_values, min_values

# Function to plot the data
def plot_fitness_data(generations, best_values, avg_values, min_values, show=False):
    plt.clf()

    plt.plot(generations, best_values, label='Best')
    plt.plot(generations, avg_values, label='Avg')
    plt.plot(generations, min_values, label='Min')

    plt.xlabel('Generation')
    plt.ylabel('Values')
    plt.title('Generation vs Best, Avg, and Min')
    
    plt.legend()
    plt.grid(True)
    plt.savefig('data/fitness/fitness_plot.png')
    if show:
        plt.show()

def save_fitness_data(show=False):
    filename = 'data/fitness/fitness_values.txt'  # Make sure the file is named 'fitness.txt' and is in the same directory
    generations, best_values, avg_values, min_values = read_fitness_file(filename)
    plot_fitness_data(generations, best_values, avg_values, min_values, show=show)

def get_fitnesses_from_file(f_name: str):
    filename = f'data/fitness/{f_name}.txt'  # Make sure the file is named 'fitness.txt' and is in the same directory
    return read_fitness_file(filename)