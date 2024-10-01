from src.utils.config import Config
from src.genetics.create_basic_genomes import create_basic_genomes
from src.genetics.genome import Genome
from typing import List


class Species: 
    def __init__(self, config: Config, species_number: int):
        self.species_number = species_number
        self.config = config
        self.genomes: List[Genome] = []

    def add_genome(self, genome: Genome):
        """Add a genome to the species."""
        self.genomes.append(genome)
        
    def get_representative(self):
        """Return a representative genome for the species (can choose the first one)."""
        if self.genomes:
            return self.genomes[0]
        return None

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

    def __repr__(self):
        return (f"Specie number: {self.species_number}, "
                f"Number of genomes: {len(self.genomes)}")