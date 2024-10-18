from numpy import save
from src.genetics.genome import Genome
from src.environments.debug_env import env_debug_init, run_game_debug
from src.utils.config import Config
from src.genetics.NEAT import NEAT
from src.utils.utils import save_fitness, save_best_genome, load_best_genome, save_neat, load_neat, save_fitness_data
import warnings
import cProfile
import pstats
import argparse
from typing import Dict

warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.1.*")

def play_genome():
    genome = load_best_genome(0)
    env, state = env_debug_init()
    run_game_debug(env, state, genome, 0, visualize=False)

def test_genome(from_gen: int, to_gen: int):
    for i in range(from_gen, to_gen + 1):
        print(f"Testing genome {i}...")
        genome = load_best_genome(i)
        env, state = env_debug_init()
        fitness = run_game_debug(env, state, genome, i)
        print(fitness)

def collect_fitnesses(genomes, generation, min_fitnesses, avg_fitnesses, best_fitnesses):
    fitnesses = [genome.fitness_value for genome in genomes]

    best_genome = max(genomes, key=lambda genome: genome.fitness_value)
    save_best_genome(best_genome, generation)

    min_fitness, avg_fitness, max_fitness = min(fitnesses), sum(fitnesses) / len(fitnesses), max(fitnesses)
    best_fitnesses.append(max_fitness)
    avg_fitnesses.append(avg_fitness)
    min_fitnesses.append(min_fitness)

    print(f"Generation: {generation} - Best: {max_fitness} - Avg: {avg_fitness} - Min: {min_fitness}")


def main(neat_name: str = '', to_generations: int = 0):
    profiler = cProfile.Profile()
    profiler.enable()
    if neat_name == '':
        config_instance = Config()
        neat = NEAT(config_instance)
        neat.initiate_genomes()
        from_generation = 0
        generations = config_instance.generations if to_generations == 0 else to_generations
    else:
        neat = load_neat(neat_name)
        config_instance = neat.config
        # from_generation = neat.generation
        from_generation = 0
        generations = (config_instance.generations - from_generation) if to_generations == 0 else to_generations

    min_fitnesses, avg_fitnesses, best_fitnesses = [], [], []
    print(f"Training from generation {from_generation} to generation {from_generation + generations}")
    
    try:
        for generation in range(from_generation, from_generation + generations):
            neat.train_genomes()
            collect_fitnesses(neat.genomes, generation, min_fitnesses, avg_fitnesses, best_fitnesses)
            
            neat.sort_species(neat.genomes)
            neat.adjust_fitness()

            save_fitness(best_fitnesses, avg_fitnesses, min_fitnesses)
            neat.calculate_number_of_children_of_species()
            new_genomes_list = []
            for specie in neat.species:
                new_genomes_list.append(neat.generate_offspring(specie))
            
            flattened_genomes = [genome for sublist in new_genomes_list for genome in sublist]
            neat.genomes = flattened_genomes
            
            print(f"new generation size: {len(neat.genomes)}" )
                
            for genome in neat.genomes:
                if not genome.elite:
                    neat.add_mutation(genome)
    except KeyboardInterrupt:
        print("\nProcess interrupted! Saving fitness data...")
    finally:
        # Always save fitness data before exiting, whether interrupted or completed
        save_fitness(best_fitnesses, avg_fitnesses, min_fitnesses)
        save_neat(neat, "latest")
        print("Fitness data saved.")
    
    profiler.disable()

    # Create a stats object to print out profiling results
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    return neat.genomes
    
def command_line_interface():
    parser = argparse.ArgumentParser(description="Train or Test Genomes")
    
    subparsers = parser.add_subparsers(dest="command", help="Choose 'train', 'test', 'graph', or 'play'")
    
    # Train command (runs main())
    train_parser = subparsers.add_parser('train', help="Run the training process")
    train_parser.add_argument('--neat_name', type=str, default='', help="The name of the NEAT object to load from 'trained_population/'")
    train_parser.add_argument('extra_number', type=int, nargs='?', default=0, help="An optional extra number (e.g., the number of generations or any other parameter)")

    # Test command (runs test_genome with a range of genomes)
    test_parser = subparsers.add_parser('test', help="Test genomes in the environment")
    test_parser.add_argument('from_gen', type=int, help="The starting genome to test")
    test_parser.add_argument('to_gen', type=int, help="The ending genome to test (exclusive)")

    graph_parser = subparsers.add_parser('graph', help="Graph the fitness data")
    
    play_parser = subparsers.add_parser('play', help="Play the best genome")
    
    args = parser.parse_args()
    
    if args.command == "train":
        main(neat_name=args.neat_name, to_generations=args.extra_number)
    elif args.command == "test":
        test_genome(args.from_gen, args.to_gen)
    elif args.command == "graph":
        save_fitness_data()
    elif args.command == "play":
        play_genome()
    else:
        parser.print_help()
        
if __name__ == "__main__":
    # main()
    command_line_interface()