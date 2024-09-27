from dataclasses import dataclass

@dataclass
class Config:
    c1: float = 1.
    c2: float = 1.
    c3: float = 0.4
    genomic_distance_threshold: float = 3.0
    population_size: int = 150