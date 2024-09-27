from src.genetics.species import Species
from src.genetics.genome import Genome
from src.utils.config import Config
from src.environments.run_env import env_init, run_game
from src.genetics.genomic_distance import *
from src.genetics.create_basic_genomes import create_basic_genomes
from typing import List
import multiprocessing

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.global_innovation_number = 0
        self.species_number = 0
        self.genomes: list[Genome] = []
        self.species: list[Species] = []

    def add_species(self, species: Species):
        self.species.append(species)

    def test_genome(self, genome: Genome):
        env, _ = env_init()
        fitness = run_game(env=env, genome=genome)
        return genome.id, fitness  # Return the genome's ID and its fitness
        
    def test_genomes(self):
        # Create a multiprocessing pool
        with multiprocessing.Pool() as pool:
            # Run `test_genome` in parallel for each genome
            results = pool.map(self.test_genome, self.genomes)
        
        # Update genomes with the returned fitness values
        for genome_id, fitness in results:
            for genome in self.genomes:
                if genome.id == genome_id:  # Match the genome by its ID
                    genome.fitness_value = fitness  # Assign the fitness value
                    break  # Move to the next result once a match is found
        
    def initiate_genomes(self, number_of_genomes: int = 20): 
        # Everyone starts in the same species
        # Initialize random population
        genomes = create_basic_genomes(number_of_genomes)
        for genome in genomes:
            node1 = genome.get_random_node()
            node2 = genome.get_random_node()
            self.global_innovation_number += 1
            while not genome.add_connection_mutation(node1, node2, self.global_innovation_number):
                node1 = genome.get_random_node()
                node2 = genome.get_random_node()
            self.genomes.append(genome)
    
    def create_species(self):
        """Create a new species with a unique species number."""
        self.species_number += 1  # Increment the global species counter
        new_species = Species(self.config, self.species_number)
        return new_species
    
    def sort_species(self, genomes: List[Genome]):
         # Create a list to hold representative genomes from each species
        test_species_genomes = [(specie, specie.genomes[0]) for specie in self.species if specie.genomes]  # List of tuples (species, representative)

        self.species = []  # Reset the species list for the new generation
        
        for specie, _ in test_species_genomes:
            specie.genomes = []

        for genome in genomes:
            found_species = False  # To track if the genome is assigned to a species

            # Compare genome to each species' representative genome
            for specie, representative in test_species_genomes:
                print(genomic_distance(genome, representative, self.config))
                if genomic_distance(genome, representative, self.config) < self.config.genomic_distance_threshold:
                    # If the genome fits, add it to the correct species
                    specie.add_genome(genome)
                    print(f"once, {specie}")
                    found_species = True
                    break  # Stop searching once the genome is added to a species

            # If the genome does not fit into any species, create a new species
            if not found_species:
                new_species = self.create_species()
                new_species.add_genome(genome)
                self.species.append(new_species)  # Add the new species to the species list
                test_species_genomes.append((new_species, genome))  # Use this genome as the representative for the new species
    
    def add_genome(self, genome: Genome):
        self.genomes.append(genome)
        
                
            
    



        
