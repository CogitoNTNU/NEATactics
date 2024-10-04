from src.genetics.node import Node
from src.genetics.genome import Genome
from src.environments.run_env import env_init, run_game
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
    for i in range(20): # how many connections and node mutations
        while not genome.add_connection_mutation(node1=genome.nodes[rand1], node2=genome.nodes[rand2], global_innovation_number=inn_number):
            rand1 = random.randint(0, len(genome.nodes)-1)
            rand2 = random.randint(0, len(genome.nodes)-1)
        rand3 = random.randint(0, len(genome.connections)-1)
        inn_number += 1
        genome.add_node_mutation(genome.connections[rand3], len(genome.nodes)+1, inn_number)
        inn_number += 1
    return inn_number

def main():
    config_instance = Config()
    neat = NEAT(config_instance)
    neat.initiate_genomes()
    
    for i in range(config_instance.generations):
        # test_generate_genome(neat) # creates randomly more "complex" genomes

        neat.test_genomes()
        for genome in neat.genomes:
            print(f"Genome {genome.id}, old fitness: {genome.fitness_value}")
        
        neat.sort_species(neat.genomes)
        neat.adjust_fitness()
        
        for genome in neat.genomes:
            print(f"Genome {genome.id}, new fitness: {genome.fitness_value}")
        
        for specie in neat.species:
            print(f"total fitness of specie {specie.species_number}: {specie.fitness_value}")
        
        
        
        neat.calculate_number_of_children_of_species()
        new_genomes_list = []
        for specie in neat.species:
            new_genomes_list.append(neat.breeder(specie))
        
        flattened_genomes = [genome for sublist in new_genomes_list for genome in sublist]
        neat.genomes = flattened_genomes
            
        for genome in neat.genomes:
            neat.add_mutation_connection(genome)

    return neat.genomes

# need if __name__ == "__main__": when running test_genomes.
if __name__ == "__main__":
    main()