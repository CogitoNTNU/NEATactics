from dataclasses import dataclass

@dataclass
class Config:
    c1: float = 1.
    c2: float = 1.
    c3: float = 0.4
    genomic_distance_threshold: float = 1
    population_size: int = 8
    generations: int = 2

    connection_weight_mutation_chance: float = 0.8
    # if mutate gene:
    connection_weight_perturbance_chance: float = 0.9
    connection_weight_random_value_chance: float = 1-connection_weight_perturbance_chance

    connection_disable_if_one_parent_disable_chance: float = 0.75

    # Chances for each of the possible ways to breed
    genome_mutation_without_crossover_chance: float = 0.25
    genome_interspecies_mating_chance: float = 0.001
    genome_mutatuin_mating_chance: float = 1-genome_mutation_without_crossover_chance-genome_interspecies_mating_chance

    new_node_small_pop_chance: float = 0.03 # for small populations
    new_node_small_big_chance: float = 0.3 # for big populations
    new_connection_chance: float = 0.05
    # Connections should be added way more often than nodes

    num_output_nodes: int = 7
    num_input_nodes: int = 200 

    # Activation function
    # What we use: ReLU
    # Paper: 1/(1+exp(-0.49*x))
    
    elitism_rate: float = 0.05 # percentage of the best genomes are copied to the next generation
    remove_worst_percentage: float = 0.05 # percentage of the worst genomes are removed from the population when breeding


    # Paper said that the max differnce in weights was about 3.0
    max_weight_difference: float = 3.0




