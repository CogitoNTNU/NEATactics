from src.genetics.genome import Genome
from src.genetics.node import Node

def create_basic_genomes(number_of_genomes=20):
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