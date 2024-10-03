from src.genetics.genome import Genome
from src.genetics.node import Node
from src.utils.config import Config
from src.genetics.NEAT import NEAT

def create_emty_genomes(number_of_genomes=20) -> list:
        """
        Empty genomes are created with no hidden layer adn only input and output nodes.
        """
        config = Config()
        num_input_nodes = config.num_input_nodes
        num_output_nodes = config.num_output_nodes
        genomes: list[Genome] = []
        
        for i in range(number_of_genomes):
            genomes.append(Genome(i))
        
        for i in range(number_of_genomes):
            genome = genomes[i]
            
            # Create output nodes
            for i in range(num_output_nodes):
                genome.add_node(Node(i, 'output'))
            
            # Create input nodes
            for i in range(num_input_nodes, num_output_nodes + num_input_nodes):
                genome.add_node(Node(i, 'input'))
        
        return genomes