from src.genetics.genome import Genome
from src.genetics.node import Node
from src.utils.config import Config
from typing import List

def create_base_genomes(number_of_genomes=None) -> List[Genome]:
        """
        Empty genomes are created with no hidden layer adn only input and output nodes.
        """
        config = Config()
        num_input_nodes = config.num_input_nodes
        num_output_nodes = config.num_output_nodes
        genomes: List[Genome] = []
        
        if number_of_genomes is None:
            number_of_genomes = config.population_size
        
        for i in range(number_of_genomes):
            genomes.append(Genome(i))
        
        for i in range(number_of_genomes):
            genome = genomes[i]
            
            # Create output nodes
            for i in range(num_output_nodes):
                genome.add_node(Node(i, 'output'))
            
            # Create input nodes
            for i in range(num_output_nodes, num_output_nodes + num_input_nodes):
                genome.add_node(Node(i, 'input'))
                
            # Create bias node with connections to all output nodes
            bias_node = Node(num_output_nodes + num_input_nodes, 'input', 1.0)
            genome.add_node(bias_node)
            for output_node in genome.output_nodes:
                genome.add_connection_mutation(bias_node, output_node, output_node.id)
    
        return genomes