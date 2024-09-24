from src.genetics.node import Node
from src.genetics.genome import Genome
from genetics.species import *
from genetics.traverse import Traverse
import random

genome = Genome(1)
genome.add_node(Node(1, 'input', 1))
genome.add_node(Node(2, 'input', 0.5))
genome.add_node(Node(3, 'input', 0))
genome.add_node(Node(4, 'input', -0.5))
genome.add_node(Node(5, 'input', 0.9))
genome.add_node(Node(6, 'input', -0.3))
genome.add_node(Node(7, 'input', 0.2))
genome.add_node(Node(8, 'output'))
genome.add_node(Node(9, 'output'))
genome.add_node(Node(10, 'output'))



def test():
    rand1 = random.randint(0, 9)
    rand2 = random.randint(0, 9)
    global_inovation_number = 0
    for i in range(15):
        while not genome.add_connection_mutation(node1=genome.nodes[rand1], node2=genome.nodes[rand2], global_innovation_number=global_inovation_number):
            rand1 = random.randint(0, 9)
            rand2 = random.randint(0, 9)
        rand3 = random.randint(0, len(genome.connections)-1)
        genome.add_node_mutation(genome.connections[rand3], len(genome.nodes)+1, global_inovation_number)

test()
forward = Traverse(genome)
something = forward.traverse()
while something != None:
    test()
    something = forward.traverse()

for output in genome.output_nodes:
    print(output, output.value)
# for connection in genome.connections:
#     print(connection)
# print(genome)

