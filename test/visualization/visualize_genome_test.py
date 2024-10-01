from src.visualization.visualize_genome import visualize_genome
from src.utils.config import Config
from src.genetics.NEAT import NEAT
import numpy as np
import pickle
import os

XLEN = 20
YLEN = 10

def get_state(file_path: str) -> np.ndarray:
    """Get a (10, 20) ndarray representing the mario state from a stored .pkl file."""
    with open(file_path, "rb") as f:
        return pickle.load(f)

def get_genome_from_NEAT():
    conf = Config(population_size=4)
    neat = NEAT(conf)
    neat.initiate_genomes()
    return neat.genomes[0]
    
def test_visualize_genome():
    state = get_state(os.path.join(os.path.dirname(__file__), "state_frame_151.pkl"))

    #list_of_nodes = create_nodes(state)
    #list_of_connections = create_connections(list_of_nodes)
    #genome = create_genome(0, list_of_nodes, list_of_connections)
    genome = get_genome_from_NEAT()
    i = 0
    for node in genome.nodes:
        if node.type == 'input':
            print(i)
            node.set_value(state[i//XLEN][i%XLEN])
            i += 1
        
    visualize_genome(genome)

if __name__ == "__main__":
    get_genome_from_NEAT()