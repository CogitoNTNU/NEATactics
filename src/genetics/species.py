from src.utils.config import Config
from src.genetics.genome import Genome
import random
from typing import List


class Species: 
    def __init__(self, config: Config, species_number: int):
        self.species_number = species_number
        self.fitness_value = 0  # Fitness value of the species
        self.new_population_size = 1 # The number of children the species should have
        self.config = config
        self.genomes: List[Genome] = []

    def add_genome(self, genome: Genome):
        """Add a genome to the species."""
        self.genomes.append(genome)
        
    def get_representative(self):
        """Return a representative genome for the species. """
        if self.genomes:
            return random.choice(self.genomes)
        return None
    
    def adjust_total_fitness(self, add_fitness):
        """Add fitness to the specie"""
        self.fitness_value += add_fitness
    
    def set_new_population_size(self, new_population_size):
        """Sets the number of children the species should make for the next genereation"""
        self.new_population_size = new_population_size

    def adjust_new_population_size(self, add_member):
        self.new_population_size += add_member

    def __repr__(self):
        return (f"Specie number: {self.species_number}, "
                f"Number of genomes: {len(self.genomes)}")