from src.genetics.genome import Genome
from src.utils.config import Config
import numpy as np

def genomic_distance(genome1: Genome, genome2: Genome, config: Config):
    # Collect innovation numbers of enabled connections for both genomes
    innovation_numbers1 = {c.innovation_number: c for c in genome1.connections if c.is_enabled}
    innovation_numbers2 = {c.innovation_number: c for c in genome2.connections if c.is_enabled}

    # Find the excess genes
    max_innovation1 = max(innovation_numbers1, default=0)
    max_innovation2 = max(innovation_numbers2, default=0)
    
    if max_innovation1 > max_innovation2:
        excess = len([x for x in innovation_numbers1 if x > max_innovation2])
    else:
        excess = len([x for x in innovation_numbers2 if x > max_innovation1])

    # Find the disjoint genes (innovation numbers that are in one genome but not the other)
    disjoint = len(set(innovation_numbers1.keys()) ^ set(innovation_numbers2.keys())) - excess

    # Find the matching genes and calculate the average weight difference
    matching_genes = set(innovation_numbers1.keys()) & set(innovation_numbers2.keys())
    if matching_genes:
        total_weight_diff = sum(abs(innovation_numbers1[num].weight - innovation_numbers2[num].weight) for num in matching_genes)
        avg_weight_diff = total_weight_diff / len(matching_genes)
    else:
        avg_weight_diff = 0

    # Calculate normalization factor n (number of genes in the larger genome)
    n = max(len(innovation_numbers1), len(innovation_numbers2), 1)  # Avoid division by 0

    # Return the genomic distance using the NEAT formula
    return (
        config.c1 * disjoint / (1+np.log(n))
        + config.c2 * excess / (1+np.log(n))
        + config.c3 * avg_weight_diff
    )