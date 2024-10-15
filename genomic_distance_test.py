from copy import deepcopy
import neat_test_file
from src.genetics.genome import Genome
from src.environments.train_env import env_init, run_game
from src.environments.debug_env import env_debug_init, run_game_debug
from src.utils.config import Config
from src.genetics.NEAT import NEAT
from src.utils.utils import save_fitness, save_best_genome, load_best_genome
from src.genetics.genomic_distance import genomic_distance
import warnings
from typing import Dict

warnings.filterwarnings("ignore")

def test_genomic_distance():
    config_instance = Config()
    neat = NEAT(config_instance)
    neat.initiate_genomes()
    genome1 = neat.genomes[0]
    genome2 = deepcopy(genome1)
    #neat.add_connection_mutation(genome2)
    neat.add_node_mutation(genome2)
    neat.random_weight_mutation(genome2)
    distance = genomic_distance(genome1, genome2, config_instance)
    print(f"Genomic distance after weight mutation: {distance}")
    for connection in genome1.connections:
        if connection.is_enabled:
            print(f"Genome1 innovation_number: {connection.innovation_number} weights: {round(connection.weight, 4)}")
    print()
    for connection in genome2.connections:
        if connection.is_enabled:
            print(f"Genome2 innovation_number: {connection.innovation_number} weights: {round(connection.weight, 4)}")

    genome3 = deepcopy(genome2)
    for _ in range(800):
        distance = genomic_distance(genome2, genome3, config_instance)
        neat.add_connection_mutation(genome3)
        neat.add_node_mutation(genome3)

def main():
    config_instance = Config(
        generations=100,
        population_size=100,
    )
    neat = NEAT(config_instance)
    neat.initiate_genomes()

    best_fitnesses = []
    avg_fitnesses = []
    min_fitnesses = []
    try:
        for generation in range(config_instance.generations):
            neat.train_genomes()
            
            # Store the best, avg and min fitness value for each generation.
            fitnesses = []
            best_genome: Dict[float, Genome] = {}
            for genome in neat.genomes: 
                fitnesses.append(genome.fitness_value)
                best_genome[genome.fitness_value] = genome
            save_best_genome(best_genome[max(fitnesses)], generation)
            best_fitnesses.append(max(fitnesses))
            avg_fitnesses.append(sum(fitnesses)/len(fitnesses))
            min_fitnesses.append(min(fitnesses))
            print(f"Generation: {generation} - Best: {best_fitnesses[-1]} - Avg: {avg_fitnesses[-1]} - Min: {min_fitnesses[-1]}")
            
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
    except KeyboardInterrupt:
        print("\nProcess interrupted! Saving fitness data...")
    finally:
        # Always save fitness data before exiting, whether interrupted or completed
        save_fitness(best_fitnesses, avg_fitnesses, min_fitnesses)
        print("Fitness data saved.")

    return neat.genomes

# need if __name__ == "__main__": when running test_genomes.
if __name__ == "__main__":
    #main()
    test_genomic_distance()
    # for i in range(5):
    #     test_genome(i)
    