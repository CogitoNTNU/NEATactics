from src.genetics.genome import Genome
from src.environments.run_env import env_init, run_game
from src.utils.config import Config
from src.genetics.NEAT import NEAT

def create_a_genome_for_visualization(genome: Genome, mutations, neat: NEAT):
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    
    for i in range(mutations):
        neat.add_mutation(genome)

def main():
    config_instance = Config()
    neat = NEAT(config_instance)
    neat.initiate_genomes()
    
    for i in range(config_instance.generations):
        neat.test_genomes()
        
        neat.sort_species(neat.genomes)
        neat.adjust_fitness()
        neat.calculate_number_of_children_of_species()
        new_genomes_list = []
        for specie in neat.species:
            new_genomes_list.append(neat.generate_offspring(specie))
        
        flattened_genomes = [genome for sublist in new_genomes_list for genome in sublist]
        neat.genomes = flattened_genomes
            
        for genome in neat.genomes:
            neat.add_mutation(genome)

    return neat.genomes

# need if __name__ == "__main__": when running test_genomes.
if __name__ == "__main__":
    main()