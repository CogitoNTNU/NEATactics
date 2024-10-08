from src.genetics.genome import Genome
from src.environments.run_env import env_init, run_game
from src.utils.config import Config
from src.genetics.NEAT import NEAT
import warnings
import pickle

warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.1.*")

def create_a_genome_for_visualization(genome: Genome, mutations, neat: NEAT):
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    neat.add_node_mutation(genome)
    
    for i in range(mutations):
        neat.add_mutation(genome)

def save_fitness(best: list, avg: list, min: list):
    with open("fitness_values.txt", "w") as f:
        for i in range(len(best)):
            f.write(f"Generation: {i} - Best: {best[i]} - Avg: {avg[i]} - Min: {min[i]}\n")

def save_best_genome(genome: Genome, id):
    filehandler = open('best_genome'+str(id)+'.obj', 'w') 
    pickle.dump(genome, filehandler)

def load_best_genome(filename):
    return pickle.load(open(filename, 'r'))

def main():
    config_instance = Config()
    neat = NEAT(config_instance)
    neat.initiate_genomes()

    best_fitnesses = []
    avg_fitnesses = []
    min_fitnesses = []
    try:
        for _ in range(config_instance.generations):
            neat.test_genomes()
            
            # Store the best, avg and min fitness value for each generation.
            fitnesses = []
            best_genome = {}
            for genome in neat.genomes: 
                fitnesses.append(genome.fitness_value)
                best_genome[genome.fitness_value] = genome
            save_best_genome(best_genome[max(fitnesses)], best_genome[max(fitnesses)].id)
            best_fitnesses.append(max(fitnesses))
            avg_fitnesses.append(sum(fitnesses)/len(fitnesses))
            min_fitnesses.append(min(fitnesses))
            print(f"Generation: {_} - Best: {best_fitnesses[-1]} - Avg: {avg_fitnesses[-1]} - Min: {min_fitnesses[-1]}")
            
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
    main()