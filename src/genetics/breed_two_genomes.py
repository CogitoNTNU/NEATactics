from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from src.genetics.genome import Genome
from src.genetics.create_base_genomes import create_base_genomes
import random

def add_connection_to_new_genome(new_genome, new_nodes_dict, connection):
        """
        Helper function to add a connection to the new genome.
        This will handle creating missing nodes if they don't exist.
        """
        in_node_id = connection.in_node.id
        out_node_id = connection.out_node.id

        # Get corresponding nodes from new genome or create if not present
        new_in_node = new_nodes_dict.get(in_node_id)
        if new_in_node is None:
            # Create the missing input node
            new_in_node = Node(connection.in_node.id, connection.in_node.type)
            new_genome.add_node(new_in_node)
            new_nodes_dict[in_node_id] = new_in_node  # Update the dictionary to reflect the new node

        new_out_node = new_nodes_dict.get(out_node_id)
        if new_out_node is None:
            # Create the missing output node
            new_out_node = Node(connection.out_node.id, connection.out_node.type)
            new_genome.add_node(new_out_node)
            new_nodes_dict[out_node_id] = new_out_node  # Update the dictionary to reflect the new node

        # Only create a new connection if both nodes are found/created
        new_connection = ConnectionGene(
            new_in_node, 
            new_out_node, 
            connection.weight, 
            connection.is_enabled, 
            connection.innovation_number
        )
        new_genome.add_connection(new_connection)
        new_in_node.add_outgoing_connection(new_connection) # The list this is added to is used in Kahns algorithm

def breed_two_genomes(genome1: Genome, genome2: Genome, genome_id: int) -> Genome:
    """
    Returns a new genome that is bred from the parameter genomes.

    The connections that line up (same innovation number) are inherited at random.
    Disjoint and excess connections are inherited from the more fit parent.
    If the parents have the same fitness, disjoint and excess connections are inherited at random.
    
    A node is only created if it is required by an inherited connection.
    """
    # print(f"Breeding genome: {genome1}")
    # print(f"with genome2: {genome2}")
    
    # Determine which genome is alpha (more fit) and beta (less fit)
    if genome1.fitness_value >= genome2.fitness_value:
        alpha_genome = genome1
        beta_genome = genome2
    else:
        alpha_genome = genome2
        beta_genome = genome1

    # Create a new genome with the correct input, output, and bias nodes
    new_genome: Genome = create_base_genomes(1)[0]  # Assuming a function to create an empty genome
    new_genome.id = genome_id
    new_nodes_dict = {node.id: node for node in new_genome.nodes}  # Fast lookup for nodes in the new genome

    # Step 1: Build dictionaries for fast connection lookups
    alpha_connections_dict = {c.innovation_number: c for c in alpha_genome.connections}
    beta_connections_dict = {c.innovation_number: c for c in beta_genome.connections}

    # Get the innovation numbers of the connections from both genomes
    alpha_num_set = set(alpha_connections_dict.keys())
    beta_num_set = set(beta_connections_dict.keys())

    # Matching innovation numbers (inherit at random)
    equal_nums = alpha_num_set & beta_num_set

    # Step 2: Inherit matching connections at random
    for innovation_number in equal_nums:
        if random.random() < 0.5:
            connection = alpha_connections_dict[innovation_number]
        else:
            connection = beta_connections_dict[innovation_number]

        # Add the selected connection to the new genome
        add_connection_to_new_genome(new_genome, new_nodes_dict, connection)

    # Step 3: Handle disjoint and excess connections
    if alpha_genome.fitness_value == beta_genome.fitness_value:
        # Randomly inherit disjoint and excess genes from either genome
        all_disjoint_and_excess_nums = alpha_num_set ^ beta_num_set
        for num in all_disjoint_and_excess_nums:
            if random.random() < 0.5:
                if num in alpha_connections_dict:
                    connection = alpha_connections_dict[num]
                else:
                    connection = beta_connections_dict[num]

                # Add the chosen connection to the new genome
                add_connection_to_new_genome(new_genome, new_nodes_dict, connection)
    else:
        # Inherit disjoint and excess genes from the more fit parent (alpha_genome)
        unique_alpha_nums = alpha_num_set - beta_num_set
        for num in unique_alpha_nums:
            connection = alpha_connections_dict[num]
            # Add the connection to the new genome
            add_connection_to_new_genome(new_genome, new_nodes_dict, connection)
    # print(f"new genome: {new_genome}")
    return new_genome
