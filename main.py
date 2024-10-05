import argparse
from src.environments.env import init, test_gym_environment, get_state_from_environment
from src.environments.run_env import run_game
from test.visualization.visualize_genome_test import get_genome_from_NEAT
from neat_test_file import test

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
    env, state = init()
    genome = get_genome_from_NEAT()
    test(genome, 1)
    run_game(env, genome, debug = True)

    # env, state = init()
    # get_state_from_environment(env) # Will save state 150 in the root folder as pkl, will also save corresponding png in mario_frames.



