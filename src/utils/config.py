from dataclasses import dataclass

@dataclass
class Config:
    c1: float = 1.
    c2: float = 1.
    c3: float = 0.4

    genomic_distance_threshold: float = 3.0

    population_size: int = 150      # Number of genomes in each generation
    n_generations: int = 10         # Number of traning generations.
    termination_rate: float = 0.5   # Remove half of the population before breeding

    # Probability of each mutation
    probability_weight_mut: float = 0.8
    probability_node_mut: float = 0.01
    probability_connection_mut: float = 0.05

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

    # Only change these values while testing! They are set automatically when training.
    num_output_nodes: int = 7
    num_input_nodes: int = 200 

    ## Activation function
    # What we use: ReLU
    # Paper: 1/(1+exp(-0.49*x))
    max_weight_difference: float = 3.0

    def __post_init__(self):
        if self.probability_connection_mut < 0 or self.probability_connection_mut > 1:
            raise Exception("Illegal value")
        if self.probability_node_mut < 0 or self.probability_node_mut > 1:
            raise Exception("Illegal value")
        if self.probability_weight_mut< 0 or self.probability_weight_mut> 1:
            raise Exception("Illegal value")