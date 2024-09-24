from src.visualization.visualize_genome import visualize_genome
from src.genetics.node import Node
from src.genetics.connection_gene import ConnectionGene
from src.genetics.genome import Genome
import random

def generate_nodes():
    list_of_nodes = []
    for i in range(200):
        color = random.random()
        list_of_nodes.append(Node(i, "Input", color))
    for i in range(200, 202):
        color = random.random()
        list_of_nodes.append(Node(i, "Hidden", color))
    for i in range(202, 207):
        color = random.random()
        list_of_nodes.append(Node(i, "Output", color))
    return list_of_nodes

def create_connections(list_of_nodes):
    list_of_connections = []
    for i in range(200):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[i], list_of_nodes[j], 1, True, 1))
    for i in range(202, 207):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[j], list_of_nodes[i], 1, True, 1))
    return list_of_connections

def test_visualize_genome():
    list_of_nodes = generate_nodes()
    list_of_connections = create_connections(list_of_nodes)
    
    genome = Genome(1)
    for i in list_of_nodes:
        genome.add_node(i)
    for i in list_of_connections:
        genome.add_connection(i)
    visualize_genome(genome)


    