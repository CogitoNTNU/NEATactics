# Environments

- [Environments](#environments)
  - [Purpose](#purpose)
  - [Structure](#structure)
  - [Usage](#usage)
    - [Initializing the Environment](#initializing-the-environment)
    - [Running the Game for Training](#running-the-game-for-training)
    - [Running the Game for Debugging](#running-the-game-for-debugging)
    - [Fitness Calculation](#fitness-calculation)
  - [Customizing the Environment](#customizing-the-environment)

## Purpose

The `environments` folder contains modules essential for setting up, interacting with, and evaluating genomes within the Super Mario Bros environment. It includes functionalities for initializing the game environment, running simulations with or without rendering (useful for both training and debugging), and calculating the fitness of genomes based on their performance in the game.

## Structure

`mario_env.py`: Defines the `MarioJoypadSpace` class, a custom environment wrapper that preprocesses game states (e.g., converting to grayscale, downsampling) and provides a custom `step` function returning a `StepResult` named tuple with detailed game information.

`fitness_function.py`: Contains the `Fitness` class, which calculates the fitness of a genome based on various game metrics such as distance traveled, coins collected, lives lost, and actions taken.

`train_env.py`: Provides functions to initialize the environment (`env_init`) and run the game without rendering (`run_game`), which is optimized for training genomes efficiently without the overhead of graphical rendering.

`debug_env.py`: Similar to `train_env.py` but includes rendering and visualization capabilities. It allows for step-by-step debugging by rendering the game, saving state images, and visualizing the genome's neural network structure during gameplay.

`README.md`: Documentation for the `environments` folder (this file).

## Usage

### Initializing the Environment

To initialize the Super Mario Bros environment, use the `env_init` function from `train_env.py`:

```python
from environments.train_env import env_init

env, initial_state = env_init()
```

This sets up the environment with the specified game version and action space, and returns the environment object along with the initial processed state.

### Running the Game for Training

To run the game without rendering (useful for training genomes), use the `run_game` function:

```python
from environments.train_env import run_game
from src.genetics.genome import Genome

fitness_score = run_game(env, initial_state, genome)
```

This function takes the environment, initial state, and a `Genome` object as inputs, and returns the fitness score calculated based on the genome's performance.

### Running the Game for Debugging

For debugging purposes with rendering and visualization, use the `debug_env.py` module:

```python
from environments.debug_env import env_debug_init, run_game_debug

env, initial_state = env_debug_init()
fitness_score = run_game_debug(env, initial_state, genome, num=1)
```

This will render the game window, save state images, and visualize the genome's neural network at each step, which is helpful for debugging and understanding how the genome interacts with the environment.

### Fitness Calculation

The `Fitness` class in `fitness_function.py` is responsible for calculating the fitness score of a genome:

```python
from environments.fitness_function import Fitness

fitness = Fitness()
fitness.calculate_fitness(info, action)
total_fitness = fitness.get_fitness()
```

The fitness calculation takes into account various factors such as:

- **Positive Rewards**:

  - Distance traveled (`move_forward`)
  - Coins collected (`coins`)
  - Winning the game (`win`)

- **Negative Penalties**:
  - Losing a life (`lose_life`)
  - Moving backward (`move_backward`)
  - Standing still (`dont_move_forward`)

## Customizing the Environment

You can customize the preprocessing of game states or the action space by modifying `mario_env.py`. The `MarioJoypadSpace` class handles state interpretation and action mapping:

```python
from environments.mario_env import MarioJoypadSpace

# Example: Custom state interpretation
class CustomMarioJoypadSpace(MarioJoypadSpace):
    def interpret_state(self, state):
        # Custom preprocessing logic
        pass
```

---

By utilizing the modules within the `environments` folder, you can efficiently train and evaluate genomes in the Super Mario Bros environment, with the flexibility to debug and customize as needed.
