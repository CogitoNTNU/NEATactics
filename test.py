from src.genetics.node import Node
from src.genetics.genome import Genome
from src.genetics.species import *
from src.genetics.traverse import Traverse
from src.environments.run_env import env_init, run_game
from src.genetics.species import Species
from src.utils.config import Config
from src.genetics.NEAT import NEAT
import random


def test_generate_genome(neat: NEAT):
    inn_number = 0
    for i in range(0, 40): # how many genomes you want to create. TODO use hyperparameter
        genome = Genome(i)
        
        # Create output nodes
        for i in range(7):
            genome.add_node(Node(i, 'output'))

        # Create input nodes
        for i in range(7, 207):
            genome.add_node(Node(i, 'input'))
        
        inn_number = test(genome, inn_number)
        neat.add_genome(genome)


def test(genome: Genome, inn_number):
    rand1 = random.randint(0, len(genome.nodes)-1)
    rand2 = random.randint(0, len(genome.nodes)-1)
    for i in range(15): # how many connections and node mutations
        while not genome.add_connection_mutation(node1=genome.nodes[rand1], node2=genome.nodes[rand2], global_innovation_number=inn_number):
            rand1 = random.randint(0, len(genome.nodes)-1)
            rand2 = random.randint(0, len(genome.nodes)-1)
        rand3 = random.randint(0, len(genome.connections)-1)
        inn_number += 1
        genome.add_node_mutation(genome.connections[rand3], len(genome.nodes)+1, inn_number)
        inn_number += 1
    return inn_number
    

# need if __name__ == "__main__": when running test_genomes.
if __name__ == "__main__":
    config_instance = Config()
    neat = NEAT(config_instance)
    
    neat.initiate_genomes()
    # test_generate_genome(neat) # creates randomly more "complex" genomes
    
    neat.test_genomes()
    # for genome in neat.genomes:
        # print(genome.fitness_value)

    neat.sort_species(neat.genomes)
    # for specie in neat.species:
    #     print(specie)
    
    
    neat.adjust_fitness()
    for specie in neat.species:
        print(f"total fitness of specie {specie.species_number}: {specie.fitness_value}")
    
    neat.calculate_number_of_children_of_species()
    #for specie in neat.species:
    #    neat.breeder(specie)