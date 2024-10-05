from src.genetics.species import Species
from src.genetics.genome import Genome
from src.utils.config import Config
from src.environments.run_env import env_init, run_game
from src.genetics.genomic_distance import *
from src.genetics.create_empty_genomes import create_empty_genomes
from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from src.genetics.breed_two_genomes import breed_two_genomes
from typing import List
import multiprocessing
import math
import random
import copy

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.global_innovation_number = 7 # When 
        self.species_number = 0
        self.genome_id = 0
        self.genomes: list[Genome] = []
        self.species: list[Species] = []
        self.connections: list[ConnectionGene] = []
        
    def check_existing_connections(self, node1: int, node2: int):
        for connection in self.connections:
            if connection.in_node.id == node1 and connection.out_node.id == node2:
                return connection.innovation_number
        return -1
            
    def add_species(self, species: Species):
        self.species.append(species)

    def breeder(self, specie: Species):
        """
        Breeds the genomes in a species to create a new generation of genomes.
        
        Uses the top half of the genomes in the species to create offspring, and 
        randomly chooses two parents from the top half to create a new genome.
        
        If the number of genomes to reproduce is higher than twice the number of 
        genomes in the species, some elite genomes will be added to the new generation.
        """
        temp_genomes = []
        
        # Sort genomes by fitness (descending order)
        ordered_list = sorted(specie.genomes, key=lambda x: x.fitness_value, reverse=True)
        
        # Select a percentage of the top genomes as elites (at least one elite survives)
        num_elites = min(max(1, int(self.config.elitism_rate * len(ordered_list))), specie.new_population_size)
        elites = ordered_list[:num_elites]  # Get the top elites
        
        # create new genomes from elites
        for elite in elites:
            cloned_elite = copy.deepcopy(elite)  # Create an exact copy of the elite genome
            cloned_elite.id = self.genome_id 
            self.genome_id += 1
            temp_genomes.append(cloned_elite)  # Add the cloned genome to the new generation
        
        # Remaining genomes to breed
        top_half = [genome for genome in ordered_list[:len(ordered_list) // 2]]
        
        if(len(top_half)%2==1):
            ordered_list.pop()
            
        for genome in top_half:
            print(f"top half fitness values: {genome.fitness_value}, genome id: {genome.id}")
        
        while len(temp_genomes) < specie.new_population_size:
            parent1 = random.choice(top_half)
            parent2 = random.choice(top_half)
            
            # Generate two offspring from each pair to maintain population size
            new_genome1 = breed_two_genomes(parent1, parent2, self.genome_id)
            self.genome_id += 1
            temp_genomes.append(new_genome1) 
        return temp_genomes

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
    
    def initiate_genomes(self, num_genomes=None): 
        # Everyone starts in the same species
        # Initialize random population
        genomes = create_empty_genomes(num_genomes)
        for genome in genomes:
            self.add_mutation_connection(genome)
            self.genomes.append(genome)
    
    def create_species(self):
        """Create a new species with a unique species number."""
        new_species = Species(self.config, self.species_number)
        self.species_number += 1  # Increment the global species counter
        return new_species
    
    def sort_species(self, genomes: List[Genome]):
        # Create a list to hold representative genomes from each species
        if not self.species:
            new_species = self.create_species()
            new_species.add_genome(genomes[0])
            self.species.append(new_species)
            test_species_genomes = [(new_species, genomes[0])]
        else:
            # Create a list to hold representative genomes from each species if species exist
            test_species_genomes = [(specie, specie.genomes[0]) for specie in self.species if specie.genomes]

        new_species_list = []  # Temporary list to hold the new species structure

        # Reset the genomes in each species (prepare for the new generation)
        for specie, _ in test_species_genomes:
            specie.genomes = []  # Clear genomes from previous generation
            specie.fitness_value = 0  # Reset the fitness value

        for genome in genomes:
            found_species = False  # Track if the genome is assigned to a species

            # Compare genome to each species' representative genome
            for specie, representative in test_species_genomes:
                if genomic_distance(genome, representative, self.config) < self.config.genomic_distance_threshold:
                    # If the genome fits, add it to the correct species
                    specie.add_genome(genome)
                    found_species = True
                    break  # Stop searching once the genome is added to a species

            # If the genome does not fit into any existing species, create a new one
            if not found_species:
                new_species = self.create_species()
                new_species.add_genome(genome)
                new_species_list.append(new_species)  # Track new species
                test_species_genomes.append((new_species, genome))  # Use this genome as the representative for the new species

        # After processing all genomes, update self.species
        self.species = [specie for specie, _ in test_species_genomes if specie.genomes]  # Remove empty species
        self.species.extend(new_species_list)  # Add newly created species

        
    def adjust_fitness(self):
        """
        Encourage diversity by adjusting the fitness values of genomes.
        Larger species get penalized slightly by dividing the fitness of 
        each genome by the species size, giving smaller species a chance 
        to survive and evolve.
        """
        for specie in self.species:
            specie_size = len(specie.genomes)
            
            if specie_size > 0:
                for genome in specie.genomes:
                    genome.fitness_value = genome.fitness_value / specie_size
                    specie.adjust_total_fitness(genome.fitness_value)  # Adjusts the total fitness of the specie
    
    def calculate_number_of_children_of_species(self):
        """Takes in all species and sets the number of children it should have"""
        config = Config()
        
        # Check if config.population_size is greater than 0
        if config.population_size <= 0:
            raise ValueError("Population size must be greater than zero.")
        
        mean_total_adjusted_fitness = sum([specie.fitness_value for specie in self.species])/config.population_size
        
        for specie in self.species:
            num_new_population = round((specie.fitness_value)/(mean_total_adjusted_fitness))
            specie.set_new_population_size(num_new_population)
            print(specie.fitness_value)
        
         # Ensures that the total sum of new genomes is the total population_size
        num_new_for_each_specie = []
        for specie in self.species:
            num_new_for_each_specie.append(specie.new_population_size)

        print(f"The new popultaion sizes for each specie:{num_new_for_each_specie}, The sum: {sum(num_new_for_each_specie)}, Total population: {config.population_size}")
        difference_between_desired_and_real = config.population_size - sum(num_new_for_each_specie)
        idx_of_species_w_most_genomes = num_new_for_each_specie.index((max(num_new_for_each_specie)))

        self.species[idx_of_species_w_most_genomes].adjust_new_population_size(difference_between_desired_and_real)

        # TODO Delete this, only for debug
        num_new_for_each_specie = []
        for specie in self.species:
            num_new_for_each_specie.append(specie.new_population_size)    
        print(f"The new popultaion sizes for each specie:{num_new_for_each_specie}, The sum: {sum(num_new_for_each_specie)}, Total population: {config.population_size}")


    def add_mutation_connection(self, genome: Genome):
        """
        Adds a new connection mutation to the genome.
        """
        # Need to see if the connection already exists in the genome
        node1 = genome.get_random_in_node()
        node2 = genome.get_random_out_node()
        
        innovation_number = self.check_existing_connections(node1.id, node2.id)
        
        if (innovation_number != -1):
            connection = genome.add_connection_mutation(node1, node2, innovation_number) # If connection exists in genome, update its value
            self.connections.append(connection)
        else:
            while node1.id == node2.id:
                node1 = genome.get_random_in_node()
                node2 = genome.get_random_out_node()
    
            connection = genome.add_connection_mutation(node1, node2, self.global_innovation_number)
            self.global_innovation_number += 1
            self.connections.append(connection)
    
    def cull_species(self):
        pass
    
    def add_genome(self, genome: Genome): # only for test.py
        self.genomes.append(genome)