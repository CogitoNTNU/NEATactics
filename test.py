from src.genetics.node import Node
from src.genetics.genome import Genome
from src.genetics.species import *
from src.genetics.traverse import Traverse
from src.environments.run_env import env_init, run_game

import random

genome = Genome(1)
for i in range(5):
    genome.add_node(Node(i, 'output'))

genome.add_node(Node(5, 'input', 1))
genome.add_node(Node(6, 'input', 0.5))
genome.add_node(Node(7, 'input', 0))
genome.add_node(Node(8, 'input', -0.5))
genome.add_node(Node(9, 'input', 0.9))
genome.add_node(Node(10, 'input', -0.3))
genome.add_node(Node(11, 'input', 0.2))





def test():
    rand1 = random.randint(0, len(genome.nodes)-1)
    rand2 = random.randint(0, len(genome.nodes)-1)
    global_inovation_number = 0
    for i in range(10):
        while not genome.add_connection_mutation(node1=genome.nodes[rand1], node2=genome.nodes[rand2], global_innovation_number=global_inovation_number):
            rand1 = random.randint(0, len(genome.nodes)-1)
            rand2 = random.randint(0, len(genome.nodes)-1)
        rand3 = random.randint(0, len(genome.connections)-1)
        genome.add_node_mutation(genome.connections[rand3], len(genome.nodes)+1, global_inovation_number)


test()
    
forward = Traverse(genome)
something = forward.traverse()
# while something != None:
#     test()
# print(something)

# for output in genome.output_nodes:
#     print(output, output.value)
    
# for connection in genome.connections:
#     print(connection)
# print(genome)

env, _ = env_init()
run_game(env=env, genome=genome)