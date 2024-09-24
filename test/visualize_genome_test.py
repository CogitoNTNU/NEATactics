from src.visualization.visualize_genome import visualize_genome
from src.genetics.node import Node
from src.genetics.connection_gene import ConnectionGene
from src.genetics.genome import Genome
import random
import numpy as np
import pickle
from typing import List

def get_state(file_path: str) -> np.ndarray:
    """Get a (10, 20) ndarray representing the mario state from a stored .pkl file."""
    with open(file_path, "rb") as f:
        return pickle.load(f)

def create_nodes(state) -> List[Node]:
    """Generate some sample nodes to visualize."""
    list_of_nodes = []
    i = 0
    for row in state:
        for value in row:
            list_of_nodes.append(Node(i, "input", value))
            i += 1

    for i in range(200, 202):
        color = random.random()
        list_of_nodes.append(Node(i, "hidden", color))
    for i in range(202, 207):
        color = random.random()
        list_of_nodes.append(Node(i, "output", color))

    return list_of_nodes

def create_connections(list_of_nodes) -> List[ConnectionGene]:
    """Create some connections to visualize."""
    list_of_connections = []
    for i in range(200):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[i], list_of_nodes[j], 1, True, 1))
    for i in range(202, 207):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[j], list_of_nodes[i], 1, True, 1))
    return list_of_connections

def create_genome(id: int, list_of_nodes: List[Node], list_of_connections: List[ConnectionGene]) -> Genome:
    """
    Input:
    - id: Unique id for Genome
    - list_of_nodes: All the nodes which the genome shall have
    - list_of_connections: All the connectoins in the Genome\n
    Output:
    - Genome object
    """
    genome = Genome(id)
    for i in list_of_nodes:
        genome.add_node(i)
    for i in list_of_connections:
        genome.add_connection(i)
    return genome
    
def test_visualize_genome():
    state = get_state("./test/state_frame_0.pkl")
    state = state / 255 # Remove this line when new state functionality is implemented.

    list_of_nodes = create_nodes(state)
    list_of_connections = create_connections(list_of_nodes)
    genome = create_genome(0, list_of_nodes, list_of_connections)
    
    visualize_genome(genome)


    