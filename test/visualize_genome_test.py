from src.visualize_genome import visualize_genome
from src.nodes import Genome, Node, ConnectionGene

def test_visualize_genome():
    list_of_nodes = []
    list_of_connections = []
    for i in range(5):
        list_of_nodes.append(Node(i, "input", 0))
    for i in range(5, 10):
        list_of_nodes.append(Node(i, "output", 1))
    for i in range(5):
        for j in range(5, 10):
            list_of_connections.append(ConnectionGene(list_of_nodes[i], list_of_nodes[j], 1, True, 1))
    genome = Genome(1)
    for i in list_of_nodes:
        genome.add_node(i)
    for i in list_of_connections:
        genome.add_connection(i)
    visualize_genome(genome)
test_visualize_genome()

    