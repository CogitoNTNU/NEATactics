from src.genetics.genome import Genome
from src.environments.train_env import env_init, run_game
from src.environments.debug_env import env_debug_init, run_game_debug
from src.utils.config import Config
from src.genetics.NEAT import NEAT
from src.utils.utils import save_fitness, save_best_genome, load_best_genome
import warnings
import pickle
import os
from typing import Dict

warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.1.*")

def create_a_genome_for_visualization(genome: Genome, mutations, neat: NEAT):
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    
    for i in range(mutations):
        neat.add_mutation(genome)

def test_genome(i):
    genome = load_best_genome(i)
    env, state = env_debug_init()
    fitness = run_game_debug(env, state, genome, i)
    print(fitness)

def main():
    config_instance = Config()
    neat = NEAT(config_instance)
    neat.initiate_genomes()

    best_fitnesses = []
    avg_fitnesses = []
    min_fitnesses = []
    try:
        for generation in range(config_instance.generations):
            neat.test_genomes()
            
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
                if genome.fitness_value == 0:
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
    main()
    
    # for i in range(5):
    #     test_genome(i)
    