from src.environments.debug_env import env_debug_init, run_game_debug
from src.utils.config import Config
from src.genetics.NEAT import NEAT
from src.utils.utils import read_fitness_file, save_fitness, save_best_genome, load_best_genome, save_neat, load_neat, save_fitness_graph_file
import warnings
import cProfile
import pstats
import argparse

warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.1.*")

def play_genome(args):
    neat_name = "latest"
    if args.neat_name != '':
        neat_name = args.neat_name

    if args.to_gen is not None:
        to_gen = args.to_gen
        if args.from_gen is not None:
            from_gen = args.from_gen
        else:
            from_gen = 0
        test_genome(from_gen, to_gen, neat_name)
    
    generation_num = args.generation if args.generation is not None else -1
    genome = load_best_genome(generation_num, neat_name)
    env, state = env_debug_init()
    run_game_debug(env, state, genome, 0, visualize=False)

def test_genome(from_gen: int, to_gen: int, neat_name: str):
    for i in range(from_gen, to_gen + 1):
        print(f"Testing genome {i}...")
        genome = load_best_genome(i, neat_name)
        env, state = env_debug_init()
        fitness = run_game_debug(env, state, genome, i)
        print(fitness)

def collect_fitnesses(genomes, generation, min_fitnesses, avg_fitnesses, best_fitnesses, neat_name):
    fitnesses = [genome.fitness_value for genome in genomes]

    best_genome = max(genomes, key=lambda genome: genome.fitness_value)
    save_best_genome(best_genome, generation, neat_name)

    min_fitness, avg_fitness, max_fitness = min(fitnesses), sum(fitnesses) / len(fitnesses), max(fitnesses)
    best_fitnesses.append(max_fitness)
    avg_fitnesses.append(avg_fitness)
    min_fitnesses.append(min_fitness)

    print(f"Generation: {generation} - Best: {max_fitness} - Avg: {avg_fitness} - Min: {min_fitness}")


def main(args):
    neat_name = args.neat_name
    print("\nTraining NEAT with name: ", neat_name)
    print()
    profiler = cProfile.Profile()
    profiler.enable()
    min_fitnesses, avg_fitnesses, best_fitnesses = [], [], []
    
    neat = load_neat(neat_name)
    if neat is not None: # TODO: Add option to insert new config into NEAT object.
        generation_nums, best_fitnesses, avg_fitnesses, min_fitnesses = read_fitness_file(neat_name)
        from_generation = generation_nums[-1] + 1
        #config_instance = neat.config
    else:
        neat = NEAT(Config())
        neat.initiate_genomes()
        from_generation = 0
    
    generations = (neat.config.generations) if args.n_generations == -1 else args.n_generations

    print(f"Training from generation {from_generation} to generation {from_generation + generations}\n")
    
    try:
        for generation in range(from_generation, from_generation + generations):
            neat.train_genomes()
            collect_fitnesses(neat.genomes, generation, min_fitnesses, avg_fitnesses, best_fitnesses, neat_name)
            
            neat.sort_species(neat.genomes)
            neat.check_population_improvements()
            neat.check_individual_impovements() # Check if the species are improving, remove the ones that are not after 15 generations
            neat.adjust_fitness()

            save_fitness(best_fitnesses, avg_fitnesses, min_fitnesses, neat_name)
            neat.calculate_number_of_children_of_species()
            neat.genomes = [genome for specie in neat.species for genome in neat.generate_offspring(specie)] # Generate offspring in each specie
            
            print(f"new generation size: {len(neat.genomes)}" )
                
            for genome in neat.genomes:
                if not genome.elite:
                    neat.add_mutation(genome)
            save_fitness_graph_file(neat_name)
    except KeyboardInterrupt:
        print("\nProcess interrupted! Saving fitness data...")
    finally:
        # Always save fitness data before exiting, whether interrupted or completed
        save_fitness(best_fitnesses, avg_fitnesses, min_fitnesses, neat_name)
        save_neat(neat, neat_name)
        print("Fitness data saved.")
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime') # Create a stats object to print out profiling results
    stats.print_stats()

    return neat.genomes
    
def command_line_interface():
    parser = argparse.ArgumentParser(description="Train or Test Genomes")
    
    subparsers = parser.add_subparsers(dest="command", help="Choose 'train', 'test', 'graph', or 'play'")
    
    # Global arguments for all functions
    parser.add_argument('-n', '--neat_name', type=str, default='latest', help="The name of the NEAT object to load from 'trained_population/'")

    # Train command (runs main())
    train_parser = subparsers.add_parser('train', help="Run the training process")
    train_parser.add_argument('-g', '--n_generations', type=int, default=-1, help="The number of generations to train for")

    graph_parser = subparsers.add_parser('graph', help="Graph the fitness data")
    
    play_parser = subparsers.add_parser('play', help="Play the best genome from the lastest generation")
    play_parser.add_argument('-g', '--generation', type=int, help="The generation of the genome to play")
    play_parser.add_argument('-f', '--from_gen', type=int, help="The starting genome to test")
    play_parser.add_argument('-t', '--to_gen', type=int, help="The ending genome to test (exclusive)")
    
    args = parser.parse_args()
    
    if args.command == "train":
        main(args) 
    elif args.command == "graph":
        save_fitness_graph_file(args.neat_name, show=True)
    elif args.command == "play":
        play_genome(args)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    command_line_interface()
