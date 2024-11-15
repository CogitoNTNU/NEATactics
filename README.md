# NEATtactics

<div align="center">

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/NEATtactics/ci.yml)
![GitHub top language](https://img.shields.io/github/languages/top/CogitoNTNU/NEATtactics)
![GitHub language count](https://img.shields.io/github/languages/count/CogitoNTNU/NEATtactics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)

<img src="docs/images/logo.png" width="50%" alt="Cogito Project Logo" style="display: block; margin-left: auto; margin-right: auto;">
</div>

<details> 
<summary><b>📋 Table of contents </b></summary>

- [NEATtactics](#neattactics)
  - [Watch Mario Clear the First Level](#watch-mario-clear-the-first-level)
  - [Description](#description)
  - [Getting started](#getting-started)
    - [Note on venv](#note-on-venv)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Basic Command](#basic-command)
    - [Example Commands](#example-commands)
    - [Command Descriptions](#command-descriptions)
      - [Train](#train)
      - [Test](#test)
      - [Graph](#graph)
      - [Play](#play)
  - [Testing](#testing)
    - [Test execution environment](#test-execution-environment)
  - [Team](#team)
    - [License](#license)

</details>

## Watch Mario Clear the First Level

<div align="center">
  <img src="docs/images/mario-clears-first-level.gif" width="80%" alt="Mario clears the first level">
</div>

## Description

NEATtactics is a project that aims to implement the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train a neural network to play a classic platformer game inspired by Super Mario. The idea is to evolve a neural network using NEAT, allowing an AI agent to learn and improve its gameplay strategies over time, starting from scratch and evolving through generations.

Our project takes inspiration from SethBling's MarI/O video, where he demonstrates a neural network learning to play Super Mario World using the NEAT algorithm. You can watch the video [here](https://www.youtube.com/watch?v=qv6UVOQ0F44) [here] (https://www.youtube.com/watch?v=CI3FRsSAa_U&t=468s) to get a better understanding of the principles behind our approach.

To implement this, we are basing our work on the [research paper](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf) "Evolving Neural Networks through Augmenting Topologies" by Kenneth O. Stanley and Risto Miikkulainen. This paper introduces the NEAT algorithm, which evolves neural network topologies along with weights to create more efficient and sophisticated solutions.

In this project, we will:

- Implement the NEAT algorithm from scratch, following the guidelines from the original research paper.
- Use a simulation environment based on a classic Super Mario platformer where our AI agent will learn to navigate and play the game.
- Continuously evolve the agent's neural network to enhance its performance, aiming for progressively better gameplay as it learns from experience.

Join us in exploring the fascinating world of neuroevolution and AI-driven gameplay!

## Getting started

Start off by cloning the repository to your local machine.

```bash
git clone https://github.com/CogitoNTNU/NEATactics
```

Next, navigate to the project directory:

```bash
cd NEATtactics
```

Create a virtual environment to manage the project dependencies:

```bash
python -m venv venv
```

Activate the virtual environment on Mac/Linux:

```bash
source venv/bin/activate
```

Alternatively use this command on windows:

```bash
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Now you are ready to run the project!

### Note on venv

You will need to activate the virtual environment for each new shell session.
If you want to deactivate the virtual environment, you can do so by either closing the terminal or
running the following command:

```bash
deactivate
```

### Prerequisites

- Ensure that git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- Ensure that you are using python version==3.8.x. [Download Python](https://www.python.org/downloads/)

## Usage

The project can be run from the command line using the `main.py` script. The script supports several commands, including training and testing genomes, visualizing fitness data, and playing a trained genome.

### Basic Command

```zsh
python main.py <command> [options]
```

### Example Commands

- Train genomes:

```zsh
python main.py train --neat_name my_saved_neat --extra_number 100
```

- Test genomes:

```zsh
python main.py test 0 10
```

- Graph fitness data:

```zsh
python main.py graph
```

Play the best genome:

```zsh
python main.py play --best
```

### Command Descriptions

#### Train

The `train` command initializes and trains genomes using the NEAT algorithm. It supports the following options:

- `--neat_name`: The name of a previously trained NEAT object located in the `trained_population` directory (default: empty string).
- `extra_number`: An optional parameter specifying the number of generations for training (default: 0). If not specified, the configuration’s default number of generations will be used.

Example:

```zsh
python main.py train --neat_name my_neat_population --extra_number 50
```

#### Test

The `test` command tests a range of genomes in the environment. The command accepts:

- `from_gen`: The starting generation number.
- `to_gen`: The ending generation number (inclusive).

Example:

```zsh
python main.py test 0 5
```

This will test genomes from generation 0 up to generation 5.

#### Graph

The `graph` command visualizes the fitness data accumulated during training. When executed, it reads the fitness data from the `data/fitness/fitness_values.txt` file and plots the best, average, and minimum fitness values for each generation. The generated plot is saved as `fitness_plot.png` in the `data/fitness` directory.

- The fitness values are extracted from `fitness_values.txt` using the `read_fitness_file` function.
- A line graph is generated where:
  - The x-axis represents generations.
  - The y-axis represents fitness values (Best, Average, Min).
- The plot is displayed and saved automatically.

Example:

```zsh
python main.py graph
```

Ensure that `fitness_values.txt` exists in the `data/fitness` directory before running this command, as it is the source file for generating the graph.

#### Play

The `play` command runs the environment using the best genome from the most recent training session. It has two optional arguments:

`-g` or `--generation`: Specifies the generation of the genome you want to play. If not provided, the latest genome will be used.
`-b` or `--best`: This flag indicates that the best genome from the specified generation (or the latest generation if `-g` is not provided) should be played.

**Examples**:

- To play the best genome from the latest generation:

```zsh
python main.py play --best
```

- To play the genome from a specific generation (e.g., generation 10):

```zsh
python main.py play --generation 10
```

- To play the best genome from generation 10:

```zsh
python main.py play --generation 10 --best
```

This flexibility allows you to test and visualize the performance of genomes from different stages of evolution.

## Testing

To run the test suite, run the following command from the root directory of the project:

```bash
pytest
```

To get a detailed report of the test coverage, run the following commands:

```bash
coverage run --source=src -m pytest
coverage html
```

Next, open the `htmlcov/index.html` file in your browser to view the
detailed coverage report. In linux and Mac, you can use the following command:

```bash
open htmlcov/index.html
```

You might want to clean up the coverage files before running the tests again. To do this, run the following commands:

```bash
coverage erase
rm -rf htmlcov
```

### Test execution environment

When first installing the project, it is advised to run the following tests:

```bash
pytest -m "environment"
```

Which will check for CUDA compatibility and the current OS.
Specifically, if you are running on Windows, you might have troubles installing the `gym_super_mario_bros` package.

## Team

This project would not have been possible without the hard work and dedication of all of the contributors. Thank you for the time and effort you have put into making this project a reality.

<table align="center">
    <tr>
        <td align="center">
            <a href="https://github.com/ChristianFredrikJohnsen">
              <img src="./docs/images/team/christian.jpg" width="100px;" alt="Christian Fredrik"/><br />
              <sub><b>Christian Fredrik</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/BrageHK">
              <img src="./docs/images/team/brage.jpg" width="100px;" alt="Brage"/><br />
              <sub><b>Brage</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/kristiancarlenius">
              <img src="./docs/images/team/kristian.jpg" width="100px;" alt="Kristian"/><br />
              <sub><b>Kristian</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/ludvigovrevik">
              <img src="./docs/images/team/ludvig.jpg" width="100px;" alt="Ludvig"/><br />
              <sub><b>Ludvig</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/kapi0okapi">
              <img src="./docs/images/team/generic1.png" width="100px;" alt="Kacper"/><br />
              <sub><b>Kacper</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/Vetlets05">
              <img src="./docs/images/team/generic2.png" width="100px;" alt="Vetle"/><br />
              <sub><b>Vetle</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/Hako2807">
              <img src="./docs/images/team/generic3.png" width="100px;" alt="Håkon"/><br />
              <sub><b>Håkon</b></sub>
            </a>
        </td>
    </tr>
</table>

![Group picture](docs/images/team/team.png)

### License

------
Distributed under the MIT License. See `LICENSE` for more information.
