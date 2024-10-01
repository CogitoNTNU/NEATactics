from dataclasses import dataclass

@dataclass
class Config:
    c1: float = 1.
    c2: float = 1.
    c3: float = 0.4
    genomic_distance_threshold: float = 3.0
    population_size: int = 150
    n_generations: int = 10
    min_weight: float = -1.
    max_weight: float = 1. 
    probability_weight_mut: float = 0.8
    probability_node_mut: float = 0.01
    probability_connection_mut: float = 0.05
    termination_rate: float = 0.5 # Remove half of the population before breeding

    def __post_init__(self):
        if self.probability_connection_mut < 0 or self.probability_connection_mut > 1:
            raise Exception("Illegal value")
        if self.probability_node_mut < 0 or self.probability_node_mut > 1:
            raise Exception("Illegal value")
        if self.probability_weight_mut< 0 or self.probability_weight_mut> 1:
            raise Exception("Illegal value")