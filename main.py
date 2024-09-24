import argparse
from src.environments.env import init, test_gym_environment

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
    test_gym_environment(env)


