from src.utils.config import Config
from src.genetics.genome import Genome
from typing import List


class Species: 
    def __init__(self, config: Config, species_number: int):
        self.species_number = species_number
        self.fitness_value = 0  # Fitness value of the species
        self.new_population_size = 1 # The number of children the species should have
        self.config = config
        self.genomes: List[Genome] = []
        # TODO may need to reset the fitness of each specie to 0 after a generation

    def add_genome(self, genome: Genome):
        """Add a genome to the species."""
        self.genomes.append(genome)
        
    def get_representative(self):
        """Return a representative genome for the species (can choose the first one)."""
        if self.genomes:
            return self.genomes[0]
        return None
    
    def adjust_total_fitness(self, add_fitness):
        """Add fitness to the specie"""
        self.fitness_value += add_fitness
    
    def set_new_population_size(self, new_population_size):
        """Sets the number of children the species should make for the next genereation"""
        self.new_population_size = new_population_size

    def adjust_new_population_size(self, add_member):
        self.new_population_size += add_member

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