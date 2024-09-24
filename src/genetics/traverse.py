from src.genetics.genome import Genome
from src.genetics.node import Node
from src.genetics.connection_gene import ConnectionGene
from typing import List

class Traverse:
    def __init__(self, genome: Genome) -> None:
        self.genome = genome
    
    
    def traverse(self) -> None:
        """
        Traverse through the genome and returns an action
        Using Kahns alorithm to traverse through the genome 
        and insuring that the node that is being traversed has 
        all its incoming connections traversed before it.
        """
        order_of_traversal = self.kahns_algorithm()
        # print(order_of_traversal)
        if not order_of_traversal:
            return None
        for node in order_of_traversal:
            for connection in node.connections_to_output:
                if connection.is_enabled:
                    self.update_out_node_value(connection)
        action = self.output()
        return action
    
    def kahns_algorithm(self) -> List[Node]:
        """
        Kahns algorithm for topological sorting of the genome

        Returns a list with nodes.
        """
        order_of_traversal = []
        in_degree = {} # How many connections are coming into the node
        for node in self.genome.nodes:
            in_degree[node.id] = 0
        for connection in self.genome.connections:
            if connection.is_enabled:
                in_degree[connection.out_node.id] += 1
        queue = []
        for node in self.genome.nodes:
            if in_degree[node.id] == 0:
                queue.append(node)
                
        while queue:
            current_node = queue.pop(0)
            order_of_traversal.append(current_node)

            for connection in current_node.connections_to_output:
                if connection.is_enabled:
                    in_degree[connection.out_node.id] -= 1
                    if in_degree[connection.out_node.id] == 0:
                        queue.append(connection.out_node)
        
            # If the topological sort includes all nodes, return it
        if len(order_of_traversal) == len(self.genome.nodes):
            return order_of_traversal
        else:
            # If not all nodes are processed, there's a cycle
            return []
        
        
    
    def output(self) -> int:
        """
        Returns the output-node with the highest value after the traversal is done
        """
        output = -1
        highest_value = 0
        for node in self.genome.output_nodes:
            if node.value > highest_value:
                highest_value = node.value
                output = node.id
    
        return output
    

    def calculate_weighted_input(self, connection: ConnectionGene) -> float:
        """
        Calculate the weighted input value from the in_node of the connection.
        
        Returns:
            float: The weighted input value for the out_node.
        """
        return connection.in_node.value * connection.weight


    def update_out_node_value(self, connection: ConnectionGene) -> None:
        """
        Update the out_node's value in the connection by adding the weighted input
        and applying the activation function.
        
        Args:
            connection (nodes.ConnectionGene): The connection gene containing in_node, out_node, and weight.
        """
        weighted_input = self.calculate_weighted_input(connection)
        connection.out_node.value += weighted_input
        connection.out_node.value = self.activation_function(connection.out_node.value)


        
    def activation_function(self, value: float) -> float:
        """
        Applies the ReLU activation function to the value
        """
        if value < 0:
            return 0
        return value 
