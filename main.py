import argparse
from src.environments.train_env import env_init, run_game
from environments.train_env import run_game
from test.visualization.visualize_genome_test import get_genome_from_NEAT
from neat_test_file import create_a_genome_for_visualization
import pickle

def main():

    parser = argparse.ArgumentParser(description="A fun Python script with a secret feature!")
    
    parser.add_argument('--hello', action='store_true', help='Print a funny message')

    args = parser.parse_args()

    if args.hello:
        print("Mario: 'Why did I stop chasing Peach around the castle? Because she politely told me to respect her boundaries, and a true hero always listens!'")
    else:
        print("Run this script with --hello for a special surprise!")

if __name__ == "__main__":
    # main()
    env, state = env_init()
    genome, neat = get_genome_from_NEAT()
    num_mutations = 10
    create_a_genome_for_visualization(genome, num_mutations, neat)
    run_game(env, state, genome)

    # env, state = init()
    # get_state_from_environment(env) # Will save state 150 in the root folder as pkl, will also save corresponding png in mario_frames.



