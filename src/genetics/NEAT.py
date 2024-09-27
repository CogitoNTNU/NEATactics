from species import Species
from src.genetics.genome import Genome
from src.utils.config import Config
from src.environments.run_env import env_init, run_game
from typing import List

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.global_innovation_number = 0
        self.species_number = 0
        self.species: list[Species] = []

    def add_species(self, species: Species):
        self.species.append(species)

    def test_genome(genome: Genome):
        env, _ = env_init()
        fitness = run_game(env=env, genome=genome)
        genome.add_fitnessvalue(fitness)

    def genomic_distance(self, genome1: Genome, genome2: Genome):
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
            self.config.c1 * disjoint / n
            + self.config.c2 * excess / n
            + self.config.c3 * avg_weight
        )
        
    def initiate_genomes(self): 
        # Everyone starts in the same species
        # Initialize random population
        specie = Species(self.config, 0)
        genomes = specie.genomes
        for genome in genomes:
            node1 = genome.get_random_node()
            node2 = genome.get_random_node()
            self.global_innovation_number += 1
            while not genome.add_connection_mutation(node1, node2, self.global_innovation_number):
                node1 = genome.get_random_node()
                node2 = genome.get_random_node()

        self.species.append(specie)
        
    def sort_species(self, genomes: List[Genome]):
        # put each genome in its own species
        test_species_genomes = [] # List with each species from the last generation with one random genome from the last generation
        for specie in self.species:
            if not specie.genomes:
                test_species_genomes.append([specie.genomes[0]])
            
        self.species = []
        genomic_distance_treshold = 1

        for genome1 in genomes:
            counter = 0
            for genome2 in test_species_genomes:
                if self.genomic_distance(genome1, genome2) < genomic_distance_treshold:
                    specie.add_genome(genome1) 
                    break
                    # When we add a new species we need the later genomes to check if 
                    # they fit in the newly added species before we make a new species
  
                else:
                    counter += 1
                if(counter>=len(test_species_genomes)):
                    self.add_species(Species())
                    pass #create new species
            

                
                
            
    



        
