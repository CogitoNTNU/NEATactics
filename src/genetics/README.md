# Genetics

- [Genetics](#genetics)
  - [Purpose](#purpose)
  - [Key Components](#key-components)
    - [`NEAT.py`](#neatpy)
    - [`genome.py`](#genomepy)
    - [`node.py`](#nodepy)
    - [`connection_gene.py`](#connection_genepy)
    - [`species.py`](#speciespy)
    - [`traverse.py`](#traversepy)
    - [`breed_two_genomes.py`](#breed_two_genomespy)
    - [`create_base_genomes.py`](#create_base_genomespy)
    - [`genomic_distance.py`](#genomic_distancepy)
  - [Usage](#usage)
    - [Initializing NEAT](#initializing-neat)
    - [Training Genomes](#training-genomes)
    - [Evolving the Population](#evolving-the-population)
  - [Note](#note)

## Purpose

The `genetics` folder contains the core implementation of the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. NEAT is an evolutionary algorithm that evolves neural networks over generations, optimizing both the weights and the topology of the networks. This folder includes classes and functions that manage genomes, species, mutations, crossover, and fitness evaluations, providing the necessary tools to evolve neural networks for tasks such as playing Super Mario Bros.

Structure

```zsh
genetics/
├── breed_two_genomes.py
├── connection_gene.py
├── create_base_genomes.py
├── genome.py
├── genomic_distance.py
├── NEAT.py
├── node.py
├── species.py
├── traverse.py
└── README.md
```

## Key Components

### `NEAT.py`

This is the main class that orchestrates the NEAT algorithm. It manages the population of genomes, speciation, fitness evaluation, and the evolutionary loop.

- Class NEAT:

  - Attributes:
    - config: Configuration parameters for NEAT.
    - global_innovation_number: Tracks innovation numbers for new connections.
    - species_number: Counts the number of species.
    - genome_id: Assigns unique IDs to genomes.
    - node_id: Assigns unique IDs to nodes.
    - genomes: List of all genomes in the population.
    - species: List of all species.
    - connections: List of all connections that have been created.
    - connections_with_node_mutations: Keeps track of connections that have had node mutations.

  - Methods:
    - generate_offspring(specie): Breeds genomes within a species to create offspring.
    - train_genome(genome): Evaluates the fitness of a genome.
    - train_genomes(): Evaluates all genomes in the population.
    - sort_species(genomes): Assigns genomes to species based on genomic distance.
    - adjust_fitness(): Adjusts fitness values to encourage diversity.
    - calculate_number_of_children_of_species(): Determines how many offspring each species should produce.
    - add_mutation(genome): Introduces mutations into a genome.
    - add_connection_mutation(genome): Adds a new connection between nodes in a genome.
    - add_node_mutation(genome): Adds a new node to a genome by splitting an existing connection.
    - initiate_genomes(num_genomes): Initializes the population with base genomes.

### `genome.py`

Represents an individual neural network in the population.

- Class Genome:
  - Attributes:
    - id: Unique identifier.
    - input_nodes, output_nodes, hidden_nodes: Lists of nodes in the genome.
    - connections: List of ConnectionGene instances.
    - fitness_value: The fitness score of the genome.
  - Methods:
    - add_node(node): Adds a node to the genome.
    - add_connection(connection): Adds a connection to the genome.
    - add_node_mutation(connection, node_id, innovation_numbers): Performs a node mutation.
    - add_connection_mutation(node1, node2, innovation_number): Adds a new connection mutation.
    - get_random_in_node(): Retrieves a random input or hidden node.
    - get_random_out_node(): Retrieves a random output or hidden node.
    - nodes: Property that returns all nodes in the genome.

### `node.py`

Defines the nodes (neurons) in the neural networks.

- Class `Node`:
  - Attributes:
    - id: Unique identifier.
    - type: Type of node (input, hidden, output, or bias).
    - value: The activation value of the node.
    - connected_nodes: List of node IDs this node is connected to.
    - connections_to_output: List of outgoing connections.
  - Methods:
    - set_value(value): Sets the value for input nodes.
    - add_node_connection(nodeId): Records a connection to another node.
    - add_outgoing_connection(connection): Adds an outgoing connection.

### `connection_gene.py`

Represents the connections (synapses) between nodes.

- Class ConnectionGene:
  - Attributes:
    - in_node: The input node.
    - out_node: The output node.
    - weight: Weight of the connection.
    - is_enabled: Whether the connection is active.
    - innovation_number: Unique identifier for tracking during crossover.

### `species.py`

Manages groups of similar genomes to encourage diversity.

- Class Species:
  - Attributes:
    - species_number: Unique identifier.
    - fitness_value: Total adjusted fitness of the species.
    - new_population_size: Number of offspring to produce.
    - genomes: List of genomes in the species.
  - Methods:
    - add_genome(genome): Adds a genome to the species.
    - adjust_total_fitness(add_fitness): Adjusts the total fitness.
    - set_new_population_size(size): Sets the number of offspring.

### `traverse.py`

Handles the activation and traversal of genomes to produce outputs.

- Class Traverse:
  - Attributes:
    - genome: The genome to traverse.
    - activation_function: The activation function to use (sigmoid or relu).
  - Methods:
    - traverse(): Performs topological traversal using Kahn's algorithm.
    - kahns_algorithm(): Computes a topological sort of the nodes.
    - output(): Determines the action based on output node values.
    - calculate_weighted_input(connection): Calculates weighted input.
    - update_out_node_value(connection): Updates the value of the output node.

### `breed_two_genomes.py`

Implements the crossover (mating) between two genomes.

- Function breed_two_genomes(genome1, genome2, genome_id):
- Breeds two genomes to produce an offspring.
- Handles matching genes, disjoint genes, and excess genes according to NEAT's rules.
- Ensures that only necessary nodes are created.

### `create_base_genomes.py`

Initializes the starting population of genomes.

- Function create_base_genomes(number_of_genomes):
  - Creates base genomes with input, output, and bias nodes.
  - Adds initial connections from the bias node to output nodes.

### `genomic_distance.py`

Calculates the distance between two genomes for speciation.

- Function genomic_distance(genome1, genome2, config):
  - Computes the distance using the NEAT formula considering excess genes, disjoint genes, and average weight differences.

## Usage

### Initializing NEAT

To start using NEAT, initialize it with a configuration:

```python
from genetics.NEAT import NEAT
from utils.config import Config

config = Config()
neat = NEAT(config)
```

### Training Genomes

Train all genomes in the current population:

```python
neat.train_genomes()
```

This function evaluates each genome's fitness by running it in the environment.

### Evolving the Population

To evolve the population over generations:

```python
for generation in range(config.generations):
    neat.train_genomes()
    neat.adjust_fitness()
    neat.calculate_number_of_children_of_species()
    new_genomes = []
    for species in neat.species:
        offspring = neat.generate_offspring(species)
        new_genomes.extend(offspring)
    neat.genomes = new_genomes
    neat.sort_species(neat.genomes)
```

This loop:

- Trains genomes and evaluates fitness.
- Adjusts fitness to encourage diversity.
- Determines offspring counts for species.
- Generates offspring through crossover and mutation.
- Updates the population and reassigns genomes to species.

## Note

- Dependencies: Ensure that all custom modules (e.g., src.utils.config, src.environments.train_env) are accessible and properly implemented.
- Configuration: The behavior of the NEAT algorithm can be adjusted via the Config class, which contains parameters like mutation rates, compatibility thresholds, and population size.
- Parallel Processing: The train_genomes method uses multiprocessing to evaluate genomes in parallel, speeding up the fitness evaluation phase.
- Activation Functions: The Traverse class supports different activation functions (sigmoid and relu), configurable via the Config class.

---

By utilizing the classes and functions within the genetics folder, you can implement the NEAT algorithm to evolve neural networks for complex tasks. The modular design allows for customization and extension to suit different applications and environments.
