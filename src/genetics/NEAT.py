from src.genetics.species import Species
from src.genetics.genome import Genome
from src.utils.config import Config
from src.environments.train_env import env_init, run_game
from src.genetics.genomic_distance import *
from src.genetics.create_base_genomes  import create_base_genomes 
from src.genetics.connection_gene import ConnectionGene
from src.genetics.breed_two_genomes import breed_two_genomes
from typing import List, Tuple
import multiprocessing
import warnings
import random
import copy

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.global_innovation_number = 7 # Because we innitialize 7 connections from the bias node
        self.species_number = 0
        self.genome_id = 0 
        self.node_id = 208 # Because we innitialize 208 nodes
        self.genomes: list[Genome] = []
        self.species: list[Species] = []
        self.connections: list[ConnectionGene] = []
        self.connections_with_node_mutations: dict[ConnectionGene, Tuple[int, int]] = {} # To keep track of connections that have had a node mutation
        self.highest_found_fitness = 0.0
        self.improvement_counter = 0
        
    def generate_offspring(self, specie: Species):
        """
        Breeds the genomes in a species to create a new generation of genomes.
        
        Removes a certain percentage of the worst performing genomes, and reproduce from the rest.
        
        If the number of genomes to reproduce is higher than twice the number of 
        genomes in the species, some elite genomes will be added to the new generation.
        
        returns: 
        :list[Genome]: List of new genomes for the next generation.
        """
        new_generation_genomes = []
        elites = []
                
        print(f"Number of offspring: {specie.new_population_size}")
        
        breeding_pool = sorted(specie.genomes, key=lambda x: x.fitness_value, reverse=True)
        
        # Select a percentage of the top genomes as elites (at least one elite survives)
        num_elites = min(max(1, int(self.config.elitism_rate * len(breeding_pool))), specie.new_population_size)
        if num_elites < len(breeding_pool):
            elites = breeding_pool[:num_elites]  # Get the top elites
        
        # create new genomes from elites
        for elite in elites:
            cloned_elite = copy.deepcopy(elite)  # Create an exact copy of the elite genome
            cloned_elite.id = self.genome_id 
            cloned_elite.elite = True
            self.genome_id += 1
            new_generation_genomes.append(cloned_elite)  # Add the cloned genome to the new generation

        # Remove a percentage of the worst-performing genomes from the breeding pool
        breeding_pool = self.select_breeding_pool(breeding_pool)
        
        # Reset the elite status of all genomes
        for genome in breeding_pool:
            genome.elite = False 
            
        while len(new_generation_genomes) < specie.new_population_size:
            if len(breeding_pool) == 0:
                print("breeding pool is empty - error NEAT line 63")
                return new_generation_genomes
            parent1 = self.select_parent(breeding_pool)
            parent2 = self.select_parent(breeding_pool)
                
            # Generate two offspring from each pair to maintain population size
            new_genome = breed_two_genomes(parent1, parent2, self.genome_id)
            self.genome_id += 1
            new_generation_genomes.append(new_genome)
        return new_generation_genomes

    def select_parent(self, breeding_pool: List[Genome]) -> Genome:
        """
        Selects a parent from the sorted breeding pool, where genomes at the top of the pool
        have a higher chance of being chosen, and the chance lowers as you go down the list.
        
        The breeding_pool is sorted from best to worst.
        
        :param breeding_pool: List of genomes, sorted by fitness from best to worst.
        :return: Selected parent genome.
        """
        # Create a weight list where the first genome has the highest weight and it decreases linearly
        #weights = [len(breeding_pool) - i for i in range(len(breeding_pool))]
        total_fitness = 0
        for genome in breeding_pool:
           total_fitness += genome.fitness_value
        weights = [genome.fitness_value/total_fitness for genome in breeding_pool]
        return random.choices(breeding_pool, weights=weights)[0]

    def train_genome(self, genome: Genome):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, message=".*Gym version v0.24.")
            env, state = env_init()
            fitness = run_game(env, state, genome)
            return genome.id, fitness  # Return the genome's ID and its fitness
        
    def rank_species(self, specie: Species) -> float:
        """Combine best genome fitness and average fitness to rank species."""
        best_genome_fitness = max(genome.fitness_value for genome in specie.genomes)
        average_fitness = sum(genome.fitness_value for genome in specie.genomes) / len(specie.genomes)
        
        weighted_score = 0.7 * best_genome_fitness + 0.3 * average_fitness
        return weighted_score

    def train_genomes(self):
        """ Train all the genomes in the population in the environment. """
        # Create a multiprocessing pool
        with multiprocessing.Pool() as pool:
            # Run `test_genome` in parallel for each genome
            results = pool.map(self.train_genome, self.genomes)
        
        # Update genomes with the returned fitness values
        for genome_id, fitness in results:
            for genome in self.genomes:
               if genome.id == genome_id:  # Match the genome by its ID
                    genome.fitness_value = fitness  # Assign the fitness value
                    break  # Move to the next result once a match is found
    
    def sort_species(self, genomes: List[Genome]):
        """
        Sort genomes into species based on genomic distance.
        
        returns:
        - list[Species]: List of species with genomes assigned to each.
        """
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
                    if not specie in new_species_list:
                        new_species_list.append(specie)
                    break  # Stop searching once the genome is added to a species

            # If the genome does not fit into any existing species, create a new one
            if not found_species:
                new_species = self.create_species()
                new_species.add_genome(genome)
                new_species_list.append(new_species)  # Track new species
                test_species_genomes.append((new_species, genome))  # Use this genome as the representative for the new species


        # After processing all genomes, update self.species
        self.species = new_species_list  # swap with the new generation of species
        
    def check_population_improvements(self):
        """ Check if there have been improvements overall in the population."""
        for specie in self.species:
            if specie.best_genome_fitness > self.highest_found_fitness:
                self.highest_found_fitness = specie.best_genome_fitness
                self.improvement_counter = 0
                print(f"New highest fitness: {self.highest_found_fitness}")
                return
        self.improvement_counter += 1
        print(f"Improvement counter: {self.improvement_counter}")
        if self.improvement_counter > 20:
            print("No improvements in 20 generations - RIP")
            self.species.sort(key=lambda x: self.rank_species(x), reverse=True)
            if len(self.species) > 2:
                self.species = self.species[:2]  # Keep the top two species
            self.improvement_counter = 0
            for specie in self.species:
                specie.improvement_counter = 0
            
        
    def check_individual_impovements(self):
        """ Check each species if they are improving, remove the ones that are not after 15 generations"""
        for specie in self.species:
            specie.genomes.sort(key=lambda x: x.fitness_value, reverse=True)
            if specie.best_genome_fitness < specie.genomes[0].fitness_value:
                specie.best_genome_fitness = specie.genomes[0].fitness_value
                specie.improvement_counter = 0
            else: 
                specie.improvement_counter += 1
        for specie in self.species:
            print(f"Specie number: {specie.species_number}, Best fitness: {specie.best_genome_fitness}, Improvement counter: {specie.improvement_counter}")
            if specie.improvement_counter > 20:
                if len(self.species) > 2:
                    self.species.remove(specie)
                else:
                    # if there are only two species left, reset their imrovement counters
                    self.improvement_counter = 0
                    for specie in self.species:
                        specie.improvement_counter = 0
        if self.species == []:
            print("All species have been removed - RIP")
            self.initiate_genomes()

    def create_species(self):
        """ Helper function to create a new species."""
        new_species = Species(self.config, self.species_number)
        self.species_number += 1  # Increment the global species counter
        return new_species
        
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
            else:
                print("specie size bug - in adjust_fitness")

    def calculate_number_of_children_of_species(self):
        """Takes in all species and sets the number of children it should have"""
        config = Config()
        
        mean_total_adjusted_fitness = sum([specie.fitness_value for specie in self.species])/config.population_size
        
        for specie in self.species:
            num_new_population = round((specie.fitness_value)/(mean_total_adjusted_fitness))
            specie.set_new_population_size(num_new_population)
        
        # Ensures that the total sum of new genomes is the total population_size
        num_new_for_each_specie = []
        for specie in self.species:
            num_new_for_each_specie.append(specie.new_population_size)
            
        print(f"The old popultaion sizes for each specie:{num_new_for_each_specie}, The old sum: {sum(num_new_for_each_specie)}, Total population: {config.population_size}")
        
        self.species.sort(key=lambda x: x.new_population_size, reverse=True)

        current_sum = sum(specie.new_population_size for specie in self.species)

        while current_sum != config.population_size:
            if current_sum > config.population_size:
                # Remove from the species with the largest population
                self.species[0].new_population_size -= 1
                current_sum -= 1
            elif current_sum < config.population_size:
                # Add to the species with the largest population
                self.species[0].new_population_size += 1
                current_sum += 1
    
            self.species.sort(key=lambda x: x.new_population_size, reverse=True)
        
        num_new_for_each_specie = []
        for specie in self.species:
            num_new_for_each_specie.append(specie.new_population_size)

    def add_mutation(self, genome: Genome):
        """
        Adds a random mutation to the genome.
        """
        # 1. Connection Weight Mutation
        connection = random.choice(genome.connections)
        if random.random() < self.config.connection_weight_mutation_chance:
            # Determine if we should perturb or assign a new random value
            if random.random() < self.config.connection_weight_perturbance_chance:
                # Perturb the weight slightly
                perturbation = random.uniform(0, 1.)*random.uniform(-1, 1)  # Adjust the range as needed
                connection.weight += perturbation
            else:
                # Assign a new random weight
                connection.weight = random.uniform(-1, 1)  # Adjust the range as needed
        
        # 2. Disable connection if one parent has it disabled
        if not connection.is_enabled and random.random() < self.config.connection_disable_if_one_parent_disable_chance:
            connection.is_enabled = False
        else:
            connection.is_enabled = True

        # 3. Determine whether to add a node mutation (based on population size)
        if self.config.population_size <= 150:  # This threshold is adjustable based on your problem's requirements
            node_mutation_chance = self.config.new_node_small_pop_chance
        else:
            node_mutation_chance = self.config.new_node_big_pop_chance

        if random.random() < node_mutation_chance:
            self.add_node_mutation(genome)

        # 4. Add Connection Mutation
        if random.random() < self.config.new_connection_chance:
            self.add_connection_mutation(genome)

        return genome

    def add_connection_mutation(self, genome: Genome):
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
    
    def add_node_mutation(self, genome: Genome):
        """
        Adds a new node mutation to the genome.
        """
        connection = random.choice(genome.connections)
        
        # need to check if there has been a node mutation on this connection before
        innovation_numbers = self.check_existing_node_mutations(connection)
        
        if innovation_numbers != None:
            genome.add_node_mutation(connection, self.node_id, innovation_numbers)
        else:
            innovation_numbers = (self.global_innovation_number, self.global_innovation_number + 1)
            self.connections_with_node_mutations[connection] = innovation_numbers # Keep track of the connection that has been mutated
            self.global_innovation_number += 2
            
            in_to_new_connection, new_to_out_connection = genome.add_node_mutation(connection, self.node_id, innovation_numbers)
            
            self.node_id += 1
            self.connections.append(in_to_new_connection)
            self.connections.append(new_to_out_connection)
    
    def adjust_perturbance_weight_mutation(self, genome: Genome):
        """
        Mutation: Adjust the weight of a random connection.
        
        The weight is adjusted by a random value between -0.5 and 0.5.
        """
        connection = random.choice(genome.connections)
        connection.weight += random.uniform(-0.5, 0.5)
    
    def random_weight_mutation(self, genome: Genome):
        """
        Mutation: Adjust the weight of a random connection.
        
        The weight is adjusted by a random value between -1 and 1.
        """
        connection = random.choice(genome.connections)
        connection.weight = random.uniform(-1, 1)
    
    def check_existing_connections(self, node1: int, node2: int):
        """ 
        Check if a connection already exists between two nodes.
        
        returns:
        - int: The innovation number of the connection if it exists, -1 otherwise
        """
        for connection in self.connections:
            if connection.in_node.id == node1 and connection.out_node.id == node2:
                return connection.innovation_number
        return -1
    
    
    def check_existing_node_mutations(self, connection: ConnectionGene):
        """
        Check if a connection has already had a node mutation.
        
        returns:
        - tuple[int, int]: The innovation numbers of the new connections if the connection has been mutated, None otherwise.
        """
        for existing_connection in self.connections_with_node_mutations:
            if existing_connection.innovation_number == connection.innovation_number:
                return self.connections_with_node_mutations[existing_connection]
        return None

    def select_breeding_pool(self, breeding_pool: List[Genome]) -> List[Genome]:
        """
        Selects genomes for breeding by removing a percentage of the worst-performing genomes.
        
        :param breeding_pool: List of genomes sorted by performance (best to worst).
        
        :return: List of genomes that will be used for breeding.
        """
        # Calculate how many genomes to remove
        num_to_remove = int(len(breeding_pool) * self.config.remove_worst_percentage)
            
        # Remove the worst-performing genomes by slicing the ordered list
        breeding_pool = breeding_pool[:-num_to_remove] if num_to_remove > 0 else breeding_pool
        
        if (len(breeding_pool) % 2 == 1 and len(breeding_pool) > 1):
            breeding_pool.pop()
        
        return breeding_pool

    def initiate_genomes(self, num_genomes=None): 
        """ Initialize random population of genomes, with one connection mutation each. """
        genomes = create_base_genomes(num_genomes)
        for genome in genomes:
            self.add_connection_mutation(genome)
            self.genomes.append(genome)