from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from src.genetics.genome import Genome
from genetics.create_empty_genomes import create_empty_genomes
import random

def breed_two_genomes(genome1: Genome, genome2: Genome):
        """
        Returns a new genome that is breed by the input genomes
        
        The connections that line up (same inn number) are inherited at random.
        Disjoint and excess are inherited from the more fit parent.
        """
        # Chooses which genome that has priority, should maybe do something different if the firness is the same
        alpha_genome = None
        beta_genome = None
        if genome1.fitness_value >= genome2.fitness_value:
            alpha_genome = genome1
            beta_genome = genome2
        else:
            alpha_genome = genome2
            beta_genome = genome1
        
        new_genome: Genome = create_empty_genomes(1)[0] # create a new genome with the correct input, output and bias nodes
        
        innovation_nums_alpha = [c.innovation_number for c in alpha_genome.connections]
        innovation_nums_beta = [c.innovation_number for c in beta_genome.connections]
        alpha_num_set = set(innovation_nums_alpha)
        beta_num_set = set(innovation_nums_beta)

        max_num_alpha = max(innovation_nums_alpha)
        max_num_beta = max(innovation_nums_beta)
        
        if max_num_alpha > max_num_beta:
            excess = [x for x in innovation_nums_alpha if x > max_num_beta]
        else:
            excess = [x for x in innovation_nums_beta if x > max_num_alpha]

        all_disjoint_and_excess_nums  = alpha_num_set ^ beta_num_set
        equal_nums = alpha_num_set & beta_num_set
        
        
        # Build dictionaries for fast lookups
        alpha_connections_dict = {c.innovation_number: c for c in alpha_genome.connections}
        beta_connections_dict = {c.innovation_number: c for c in beta_genome.connections}
        new_nodes_dict = {node.id: node for node in new_genome.nodes}

        # Iterate over the matching innovation numbers
        for innovation_number in equal_nums:
            if random.random() < 0.5:  # Randomly choose alpha_genome's connection
                connection = alpha_connections_dict.get(innovation_number)

                if connection:
                    in_node_id = connection.in_node.id
                    out_node_id = connection.out_node.id

                    # Get corresponding nodes from new genome or create if not present
                    new_in_node = new_nodes_dict.get(in_node_id)
                    if new_in_node is None:
                        # Create the missing input node
                        new_in_node = Node(connection.in_node.id, connection.in_node.type)  # Adjust "type" if needed
                        new_genome.add_node(new_in_node)
                        new_nodes_dict[in_node_id] = new_in_node  # Update the dictionary to reflect the new node

                    new_out_node = new_nodes_dict.get(out_node_id)
                    if new_out_node is None:
                        # Create the missing output node
                        new_out_node = Node(connection.out_node.id, connection.out_node.type)  # Adjust "type" if needed
                        new_genome.add_node(new_out_node)
                        new_nodes_dict[out_node_id] = new_out_node  # Update the dictionary to reflect the new node

                    # Only create a new connection if both nodes are found
                    if new_in_node and new_out_node:
                        new_connection = ConnectionGene(
                            new_in_node, 
                            new_out_node, 
                            connection.weight, 
                            connection.is_enabled, 
                            innovation_number
                        )
                        new_genome.add_connection(new_connection)
            else:
                connection = beta_connections_dict.get(innovation_number)

                if connection:
                    in_node_id = connection.in_node.id
                    out_node_id = connection.out_node.id

                    # Get corresponding nodes from new genome or create if not present
                    new_in_node = new_nodes_dict.get(in_node_id)
                    if new_in_node is None:
                        # Create the missing input node
                        new_in_node = Node(connection.in_node.id, connection.in_node.type)  # Adjust "type" if needed
                        new_genome.add_node(new_in_node)
                        new_nodes_dict[in_node_id] = new_in_node  # Update the dictionary to reflect the new node

                    new_out_node = new_nodes_dict.get(out_node_id)
                    if new_out_node is None:
                        # Create the missing output node
                        new_out_node = Node(connection.out_node.id, connection.out_node.type)  # Adjust "type" if needed
                        new_genome.add_node(new_out_node)
                        new_nodes_dict[out_node_id] = new_out_node  # Update the dictionary to reflect the new node

                    # Only create a new connection if both nodes are found
                    if new_in_node and new_out_node:
                        new_connection = ConnectionGene(
                            new_in_node, 
                            new_out_node, 
                            connection.weight, 
                            connection.is_enabled, 
                            innovation_number
                        )
                        new_genome.add_connection(new_connection)
        # randomly pick excess and disjoin genes from either parent
        if alpha_genome.fitness_value == beta_genome.fitness_value:
            alpha_disjoint_and_excess_nums = alpha_num_set - beta_num_set  # Disjoint and excess genes from alpha_genome
            beta_disjoint_and_excess_nums = beta_num_set - alpha_num_set  # Disjoint and excess genes from beta_genome
            
            # Step 3: Iterate over all disjoint and excess genes
            for num in all_disjoint_and_excess_nums:
                # Randomly decide whether to include this connection in the new genome
                if random.random() < 0.5:
                    # If the gene comes from alpha_genome (either disjoint or excess)
                    if num in alpha_connections_dict:
                        chosen_connection = alpha_connections_dict[num]
                    # If the gene comes from beta_genome (either disjoint or excess)
                    elif num in beta_connections_dict:
                        chosen_connection = beta_connections_dict[num]
                    else:
                        continue  # Skip if somehow neither parent has this gene (which shouldn't happen)

                    # Step 4: Get the nodes associated with the chosen connection
                    in_node_id = chosen_connection.in_node.id
                    out_node_id = chosen_connection.out_node.id

                    # Get corresponding nodes from new genome or create if not present
                    new_in_node = new_nodes_dict.get(in_node_id)
                    if new_in_node is None:
                        # Create the missing input node
                        new_in_node = Node(chosen_connection.in_node.id, chosen_connection.in_node.type)
                        new_genome.add_node(new_in_node)
                        new_nodes_dict[in_node_id] = new_in_node  # Update the dictionary

                    new_out_node = new_nodes_dict.get(out_node_id)
                    if new_out_node is None:
                        # Create the missing output node
                        new_out_node = Node(chosen_connection.out_node.id, chosen_connection.out_node.type)
                        new_genome.add_node(new_out_node)
                        new_nodes_dict[out_node_id] = new_out_node  # Update the dictionary

                    # Step 5: Create the new connection with the properties from the chosen parent
                    new_connection = ConnectionGene(
                        new_in_node,
                        new_out_node,
                        chosen_connection.weight,
                        chosen_connection.is_enabled,
                        chosen_connection.innovation_number
                    )
                    
                    # Add the new connection to the new genome
                    new_genome.add_connection(new_connection)
        else:
            # Get connections from the most fit parent
            disjoint_and_excess_nums = alpha_num_set - beta_num_set  # This gives you all disjoint and excess genes from alpha_genome
            
            # create a new connection with the same in node, out node and weight as the alpha_nums connection with the correct inn number
            for num in disjoint_and_excess_nums:
                connection = alpha_connections_dict.get(num)
                
                if connection:
                    in_node_id = connection.in_node.id
                    out_node_id = connection.out_node.id

                    # Get corresponding nodes from new genome or create if not present
                    new_in_node = new_nodes_dict.get(in_node_id)
                    if new_in_node is None:
                        # Create the missing input node
                        new_in_node = Node(connection.in_node.id, connection.in_node.type)
                        new_genome.add_node(new_in_node)
                        new_nodes_dict[in_node_id] = new_in_node  # Update the dictionary

                    new_out_node = new_nodes_dict.get(out_node_id)
                    if new_out_node is None:
                        # Create the missing output node
                        new_out_node = Node(connection.out_node.id, connection.out_node.type)
                        new_genome.add_node(new_out_node)
                        new_nodes_dict[out_node_id] = new_out_node  # Update the dictionary

                    # Step 4: Create the new connection with the same properties as in alpha_genome
                    new_connection = ConnectionGene(
                        new_in_node,
                        new_out_node,
                        connection.weight,
                        connection.is_enabled,
                        connection.innovation_number
                    )
                    # Add the new connection to the new genome
                    new_genome.add_connection(new_connection)
        return new_genome