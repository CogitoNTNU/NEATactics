import random
from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.genetics.node import Node


class Genome:
    """
    Represents some neural network.
    It has a unique id, and contains a set of nodes and connections. 
    """
    def __init__(self, id: int):
        self.id = id
        self.input_nodes: list[Node] = []
        self.output_nodes: list[Node] = []
        self.hidden_nodes: list[Node] = []
        self.connections: list[ConnectionGene] = []
        self.fitness_value: float = 0.0

    def add_node(self, node: Node):
        if node.type == 'input':
            self.input_nodes.append(node)
        elif node.type == 'output':
            self.output_nodes.append(node)
        elif node.type == 'hidden':
            self.hidden_nodes.append(node)

    def add_connection(self, connection: ConnectionGene):
        """ Adds a connection to the genome. """
        self.connections.append(connection)
        
    def disable_connection(self, connection: ConnectionGene):
        """ Disables a connection. """
        connection.is_enabled = False
    
    def add_node_mutation(self, connection: ConnectionGene, node_id: int, innovation_number: int) -> int:
        """
        Mutation: add a new node to the network. 
        The new node is placed between the two nodes of the connection.
        
        The connection is disabled and two new connections are added, one from the input node to the new node
        and one from the new node to the output node. The new node is added to the network and the innovation
        number is updated.
        """
        node1 = connection.in_node
        node2 = connection.out_node
        new_node = Node(node_id, 'hidden')
        self.add_node(new_node)
        
        connection1 = ConnectionGene(node1, new_node, 1, True, innovation_number) # First connections weight is set to 1
        innovation_number += 1 #Hvordan funker innovation number? Skal de to nye connections ha ulike innovation numbers?
        connection2 = ConnectionGene(new_node, node2, connection.weight, True, innovation_number)
        innovation_number += 1
        self.disable_connection(connection)
        self.add_connection(connection1)    
        self.add_connection(connection2)
        node2.add_node_connection(new_node.id)
        node1.add_node_connection(new_node.id)
        new_node.add_node_connection(node1.id)
        new_node.add_node_connection(node2.id)
        new_node.add_outgoing_connection(connection2)
        node1.add_outgoing_connection(connection1)
        return innovation_number
    

    def add_connection_mutation(self, node1: Node, node2: Node, global_innovation_number: int): 
        """
        Attempts to create a new connection between two nodes (node1 and node2).
        
        The method checks if the connection is valid, assigns it a random weight, 
        and adds it to the network if valid. The connection is marked with a unique 
        global innovation number and enabled by default.

        Parameters:
        - node1 (Node): Starting node of the connection. Pick from Genomes nodes list
        - node2 (Node): Target node of the connection. Pick from Genomes nodes list

        Returns:
        - bool: True if the connection was successfully added, False otherwise.
        """
        weight = self.create_weight()
        excisting_connection = self.check_existing_connection(node1, node2) # check if connection already exists
        if excisting_connection:
            excisting_connection.is_enabled = True
            self.weight_mutation(excisting_connection)
            return excisting_connection
        
        connection = ConnectionGene(node1, node2, weight, True, global_innovation_number)
        self.add_connection(connection)
        node2.add_node_connection(node1.id)
        node1.add_node_connection(node2.id)
        node1.add_outgoing_connection(connection)
        return connection
    
    def weight_mutation(self, connection: 'ConnectionGene'):
        connection.weight = self.create_weight() 
    
    def create_weight(self):
        """
        A helper function to create a random weight for a connection.
        
        Weights are initialized to a random value between -1 and 1. (could be changed)

        Returns:
        - float: A random weight value between -1 and 1.
        """
        return 2*random.random()-1  #TODO Make this better. Chooses a random value between -1 and 1 for the new weight
    
    def get_random_in_node(self):
        """ Returns a random input or hidden node from the genome. """
        combined_nodes = self.input_nodes + self.hidden_nodes
        return random.choice(combined_nodes)
        

    def get_random_out_node(self):
        """ Returns a random output or hidden node from the genome. """
        combined_nodes = self.output_nodes + self.hidden_nodes
        return random.choice(combined_nodes)

    def add_fitnessvalue(self, fitness: float):
        """
        
        """
        self.fitness_value = fitness

    def get_total_weight(self):
        """ Calculate the total weight of all connections in the genome. """
        total_weight = 0
        count = 0
        for connection in self.connections:
            count += 1
            total_weight += connection.get_connection_weight()
        return total_weight, count
    
    def check_existing_connection(self, node1: Node, node2: Node):
        """
        Check if a connection between two nodes already exists in the genome.
        
        Returns:
        - ConnectionGene: The existing connection if it exists, None otherwise
        """
        for connection in self.connections:
            if connection.in_node == node1 and connection.out_node == node2:
                return connection
        return None
    
    @property
    def nodes(self) -> List[Node]:
        # Combine all nodes into one list when accessing .nodes
        return self.output_nodes + self.input_nodes + self.hidden_nodes
    
    def __repr__(self):
        return (f"Genome(id={self.id}, hidden nodes={[node.id for node in self.hidden_nodes]}, "
                f"connections={[connection for connection in self.connections]}, fitness_value={self.fitness_value})")

