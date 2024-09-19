from src.visualize_genome import visualize_genome
from src.nodes import Genome, Node, ConnectionGene
import random

def test_visualize_genome():
    list_of_nodes = []
    list_of_connections = []
    for i in range(200):
        color = random.random()
        list_of_nodes.append(Node(i, "Input", color))
    for i in range(200, 202):
        color = random.random()
        list_of_nodes.append(Node(i, "Hidden", color))
    for i in range(202, 207):
        color = random.random()
        list_of_nodes.append(Node(i, "Output", color))
    for i in range(200):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[i], list_of_nodes[j], 1, True, 1))
    for i in range(202, 207):
        for j in range(200, 202):
            list_of_connections.append(ConnectionGene(list_of_nodes[j], list_of_nodes[i], 1, True, 1))

    genome = Genome(1)
    for i in list_of_nodes:
        genome.add_node(i)
    for i in list_of_connections:
        genome.add_connection(i)
    visualize_genome(genome)


    