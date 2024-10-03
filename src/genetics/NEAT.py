from src.genetics.species import Species
from src.genetics.genome import Genome
from src.utils.config import Config
from src.environments.run_env import env_init, run_game
from src.genetics.genomic_distance import *
from src.genetics.create_basic_genomes import create_basic_genomes
from src.genetics.connection_gene import ConnectionGene
from typing import List
import multiprocessing
import math
import random

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.global_innovation_number = 0 # When 
        self.species_number = 0
        self.genomes: list[Genome] = []
        self.species: list[Species] = []
        self.connections: list[ConnectionGene] = []
        
    def save_genomes(self):
        raise NotImplementedError()
    
    def load_genomes(self):
        raise NotImplementedError()
        
    def start_training(self):
        self.initiate_genomes()

        for i in range(self.config.n_generations):
            print(f"Generation {i} starts gaming!")
            self.test_genomes()
            # TODO: Breed and destroy old generation
            for genome in self.genomes:
                rand_num = random.uniform(0, 1)
                if rand_num < self.config.probability_node_mut:
                    genome.add_node_mutation()
                rand_num = random.uniform(0, 1)
                if rand_num < self.config.probability_weight_mut:
                    genome.weight_mutation()
                rand_num = random.uniform(0, 1)
                if rand_num < self.config.probability_connection_mut:
                    genome.add_connection_mutation()
        
    def check_existing_connections(self, node1: int, node2: int):
        for connection in self.connections:
            if connection.in_node.id == node1 and connection.out_node.id == node2:
                return connection.innovation_number
        return -1
            
    def add_species(self, species: Species):
        self.species.append(species)

    def breeder(self, species: Species):
        temp_genomes = []
        ordered_list = sorted(species.genomes, key=lambda x: x.fitness_value, reverse=True)[:int(math.floor((len(species.genomes))/2))]
        if(len(ordered_list)%2==1):
            ordered_list.pop()
        while len(ordered_list) != 0:
            random_next = random.randint(1, len(ordered_list)-1)
            new_genome = self.breed_two_genomes(ordered_list[random_next], ordered_list[0])
            temp_genomes.append(new_genome)
            ordered_list.pop(0)
            ordered_list.pop(random_next)
        # orderd_list[0] har den mest fit genomen i specien 
        self.genomes = temp_genomes

    def breed_two_genomes(self, genome1: Genome, genome2: Genome):
        """
        Returns a new genome that is breeded by the input genomes
        """
        # Chooses which genome that has priority, should maybe do something different if the firness is the same
        if genome1.fitness_value >= genome2.fitness_value:
            alfa_genome = genome1
            beta_genome = genome2
        else:
            alfa_genome = genome2
            beta_genome = genome1
        
        new_genome = Genome(id=len(self.genomes))
        for i_number in range(self.global_innovation_number): #the innovation numbers are in order and such we only need one loop
            alfa_connected = False
            for connection in alfa_genome.connections:
                if connection.innovation_number == i_number:
                    new_genome.add_connection(alfa_genome.connections[i_number])
                    new_genome.add_node(alfa_genome.connections[i_number].in_node)
                    alfa_connected = True
                    break
            if not alfa_connected:
                for connection in beta_genome.connections:
                    if connection.innovation_number == i_number:
                        new_genome.add_connection(alfa_genome.connections[i_number])
                        break
        return new_genome

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
            self.add_mutation_connection(genome)
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
    
    def add_mutation_connection(self, genome: Genome):
        node1 = genome.get_random_node()
        node2 = genome.get_random_node()
        innovation_number = self.check_existing_connections(node1.id, node2.id)
        if (innovation_number !=-1):
            genome.add_connection_mutation(node1, node2, innovation_number)
        else:
            while not genome.is_valid_connection(node1, node2):
                node1 = genome.get_random_node()
                node2 = genome.get_random_node()
    
            connection = genome.add_connection_mutation(node1, node2, self.global_innovation_number)
            self.global_innovation_number += 1
            self.connections.append(connection)
    
    def cull_species(self):
        pass
    
    def add_genome(self, genome: Genome): # only for test.py
        self.genomes.append(genome)