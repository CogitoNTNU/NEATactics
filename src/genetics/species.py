from src.genetics.node import Node
from src.genetics.genome import Genome
from src.utils.config import Config


class Species: 
    def __init__(self, config: Config, species_number: int):
        self.members = []
        self.species_number = species_number
        self.config = config
        self.genomes = self.initialize_genomes(config.population_size)
        
    def initialize_genomes(self, number_of_genomes: int):
        genomes: list[Genome] = []
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
