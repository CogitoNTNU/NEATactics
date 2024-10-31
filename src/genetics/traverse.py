from src.genetics.genome import Genome
from src.genetics.node import Node
from src.genetics.connection_gene import ConnectionGene
from src.utils.config import Config
from typing import List, Deque, DefaultDict
import numpy as np
from collections import defaultdict, deque

class Traverse:
    def __init__(self, genome: Genome) -> None:
        self.genome = genome
        if not genome.order_of_traversal:
            genome.order_of_traversal = self.kahns_algorithm()
        self.config = Config()
        a_func = self.config.activation_func.lower() 
        if a_func == "relu":
            self.activation_function = self.relu
        elif a_func == "sigmoid":
            self.activation_function = self.sigmoid
        elif a_func == "tanh":
            self.activation_function = self.tanh
        else:
            raise NotImplementedError(f"We have not implemented {self.config.activation_func}")
    
    def traverse(self) -> int:
        """
        Traverse through the genome and returns an action
        Using Kahns alorithm to traverse through the genome 
        and ensuring that the node that is being traversed has 
        all its incoming connections traversed before it.
        """
        order_of_traversal = self.genome.order_of_traversal
        if not order_of_traversal:
            return 6 # if it finds a loop, choose to go left to get minimal fitness value
        for node in order_of_traversal:
            if node.type != "input":
                node.value = self.activation_function(node.value)
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
        in_degree: DefaultDict[int, int] = defaultdict(int) # How many connections are coming into the node

        for connection in self.genome.connections:
            if connection.is_enabled:
                in_degree[connection.out_node.id] += 1

        queue: Deque[Node] = deque([node for node in self.genome.nodes if in_degree[node.id] == 0])
                
        while queue:
            current_node = queue.popleft()
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
            # print("loop")
            return []
        
        
    
    def output(self) -> int:
        """
        Returns the output-node with the highest value after the traversal is done
        """
        output = 0
        highest_value = -1000.0
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


    def relu(self, value: float) -> float:
        if value < 0:
            return 0.0
        return value 

    def sigmoid(self, value: float) -> float:
        return 1/(1 + np.exp(-0.49 * value))
        
    def tanh(self, value: float) -> float:
        return np.tanh(value)