from dataclasses import dataclass
from typing import Tuple

@dataclass
class Config:
    c1: float = 1.5 # c1, c2, c3 [controls speciation], relatively good
    c2: float = 1.5
    c3: float = 0.4
    genomic_distance_threshold: float = 2.69
    population_size: int = 56 * 10 # 56 cores on IDUN
    generations: int = int(1e6) # A bunch of iterations 

    connection_weight_mutation_chance: float = 0.8

    # if mutate gene:
    connection_weight_perturbance_chance: float = 0.9

    # Chances for each of the possible ways to breed
    genome_mutation_without_crossover_chance: float = 0.25

    small_population_new_node_chance: float = 0.03 # for small populations
    large_population_new_node_chance: float = 0.06 # for big populations (big pop = 150)
    new_connection_chance: float = 0.4
    # Connections should be added way more often than nodes

    num_output_nodes: int = 7
    num_input_nodes: int = 200
    input_shape: Tuple[int, int] = (10, 20)

    # Activation function
    # Paper: 1/(1+exp(-0.49*x))
    activation_func: str = "sigmoid"
    
    elitism_rate: float = 0.02 # percentage of the best genomes are copied to the next generation
    remove_worst_percentage: float = 0.4 # percentage of the worst genomes are removed from the population when breeding

    SHOULD_PROFILE: bool = False
