from src.genetics.genome import Genome
from src.utils.config import Config

def genomic_distance(genome1: Genome, genome2: Genome, config: Config):
        innovation_numbers1 = [c.innovation_number for c in genome1.connections if c.is_enabled]
        innovation_numbers2 = [c.innovation_number for c in genome2.connections if c.is_enabled]

        excess = None
        # Last element in the list should always be the largest
        connections1_max = innovation_numbers1[-1]
        connections2_max = innovation_numbers2[-1]
        n = 0
        if connections1_max > connections2_max:
            excess = len([x for x in innovation_numbers1 if x > connections2_max])
            n = connections1_max
        else:
            n = connections2_max
            excess = len([x for x in innovation_numbers2 if x > connections1_max])

        disjoint_set = set(innovation_numbers1) ^ set(innovation_numbers2) # XOR to find disjoint
        disjoint = len(disjoint_set) - excess

        weight_1, amount_1 = genome1.get_total_weight()
        weight_2, amount_2 = genome2.get_total_weight()
        avg_weight = (weight_1+weight_2)/(amount_1+amount_2)

        return (
            config.c1 * disjoint / n
            + config.c2 * excess / n
            + config.c3 * avg_weight
        )