from src.visualization.visualize_genome import visualize_genome
from src.utils.config import Config
from src.genetics.NEAT import NEAT
import numpy as np
import pickle
import os
from typing import List
from src.genetics.node import Node
from src.genetics.traverse import Traverse

XLEN = 20
YLEN = 10

def get_state(file_path: str) -> np.ndarray:
    """Get a (10, 20) ndarray representing the mario state from a stored .pkl file."""
    with open(file_path, "rb") as f:
        return pickle.load(f)

def set_input_node_values(state: np.ndarray, node_list: List[Node]):
    i = 0
    for node in node_list:
        if node.type == 'input' and node.value != 1: # Avoid bias node
            node.set_value(state[i//XLEN][i%XLEN])
            i += 1

def get_genome_from_NEAT():
    conf = Config(population_size=4)
    neat = NEAT(conf)
    neat.initiate_genomes()
    return neat.genomes[0], neat
    
def test_visualize_genome():
    state = get_state(os.path.join(os.path.dirname(__file__), "state_frame_151.pkl"))

    genome, neat = get_genome_from_NEAT()
    set_input_node_values(state, genome.nodes)
    traverse = Traverse(genome)
    traverse.traverse()
    visualize_genome(genome, 0)

if __name__ == "__main__":
    get_genome_from_NEAT()