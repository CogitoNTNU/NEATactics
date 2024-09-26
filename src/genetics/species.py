from src.genetics.node import Node
from src.genetics.genome import Genome
from src.utils.config import Config


class Species:  # Made by Copilot
    def __init__(self, config: Config):
        self.members = []
        self.config = config

class Species: # Made by Copilot
    def __init__(self):
        self.genomes = self.initialize_genomes()
        
    def initialize_genomes(self, number_of_genomes=10):
        genomes = []
        for i in range(number_of_genomes):
            genomes.append(Genome(i))
        
        for i in range(number_of_genomes):
            genome = genomes[i]
            
            # Create output nodes
            for i in range(7):
                genome.add_node(Node(i, 'output'))
            
            # Create input nodes
            for i in range(7, 207):
                genome.add_node(Node(i, 'input'))
        
        return genomes

    def add_genome(self, member):
        self.genomes.append(member)

    def genomic_distance(self, genome1: Genome, genome2: Genome):
        connections1 = [c.innovation_number for c in genome1.connections if c.is_enabled]
        connections2 = [c.innovation_number for c in genome2.connections if c.is_enabled]

        excess = None
        # Last element in the list should always be the largest
        connections1_max = connections1[-1]
        connections2_max = connections2[-1]
        n = 0
        if connections1_max > connections2_max:
            excess = len([x for x in connections1 if x > connections2_max])
            n = connections1_max
        else:
            n = connections2_max
            excess = len([x for x in connections2 if x > connections1_max])
        disjoint = set(connections1) ^ set(connections2) - excess

        avg_weight = genome1.get_weight()

        return (
            self.config.c1 * disjoint / n
            + self.config.c2 * excess / n
            + self.config.c3 * avg_weight
        )

    def calculate_fitness(self):
        # Calculate the fitness of each member in the species
        pass

    def adjust_fitness(self):
        # Adjust the fitness of each member in the species based on its compatibility distance
        pass

    def remove_weak_members(self):
        # Remove weak members from the species
        pass

    def reproduce(self):
        # Reproduce and create new members for the next generation
        pass

    def update_representative(self):
        # Update the representative member of the species
        pass
