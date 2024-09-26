from src.genetics.node import Node
from src.genetics.genome import Genome
from src.genetics.species import *
from src.genetics.traverse import Traverse
from src.environments.run_env import env_init, run_game
from src.genetics.species import Species
import random


def test_generate_genome():
    for i in range(300):
        genome = Genome(i)
        
        # Create output nodes
        for i in range(7):
            genome.add_node(Node(i, 'output'))

        # Create input nodes
        for i in range(7, 207):
            genome.add_node(Node(i, 'input'))


def test(genome: Genome):
    rand1 = random.randint(0, len(genome.nodes)-1)
    rand2 = random.randint(0, len(genome.nodes)-1)
    global_inovation_number = 0
    for i in range(10):
        while not genome.add_connection_mutation(node1=genome.nodes[rand1], node2=genome.nodes[rand2], global_innovation_number=global_inovation_number):
            rand1 = random.randint(0, len(genome.nodes)-1)
            rand2 = random.randint(0, len(genome.nodes)-1)
        rand3 = random.randint(0, len(genome.connections)-1)
        genome.add_node_mutation(genome.connections[rand3], len(genome.nodes)+1, global_inovation_number)


species = Species()
genomes = species.initialize_genomes()


for genome in genomes:
    test(genome)
    env, _ = env_init()
    run_game(env=env, genome=genome)
    # test(genome)

    
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

