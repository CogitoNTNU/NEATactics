import random
from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from src.genetics.node import Node


class Genome:
    """
    Represents some neural network.
    It has a unique id, and contains a set of nodes and connections. 
    """
    def __init__(self, id: int):
        self.id = id
        
        self.input_nodes: List[Node] = []
        self.output_nodes: List[Node] = []
        self.hidden_nodes: List[Node] = []
        
        self.connections: List[ConnectionGene] = []
        self.order_of_traversal: List[Node] = []
        self.fitness_value: float = 0.0
        self.elite = False

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
    
    def add_node_mutation(self, connection: ConnectionGene, node_id: int, innovation_numbers: Tuple[int, int]):
        """
        Mutation: add a new node to the network. 
        The new node is placed between the two nodes of the connection.
        
        The connection is disabled and two new connections are added, one from the input node to the new node
        and one from the new node to the output node. The new node is added to the network and the innovation
        number is updated.
        
        returns:
        - ConnectionGene: The new connection from the input node to the new node.
        - ConnectionGene: The new connection from the new node to the output node.
        - Node: The new node that was added to the network.
        """
        new_node = Node(node_id, 'hidden')
        self.add_node(new_node)
        
        in_node = connection.in_node
        out_node = connection.out_node
        
        # Create two new connections, 
        connection1 = ConnectionGene(in_node, new_node, 1, True, innovation_numbers[0])
        connection2 = ConnectionGene(new_node, out_node, connection.weight, True, innovation_numbers[1])

        self.disable_connection(connection)
        self.add_connection(connection1)    
        self.add_connection(connection2)
        
        # The genome has to keep track of outgoing connections for each node for Kahns algorithm
        new_node.add_outgoing_connection(connection2) 
        in_node.add_outgoing_connection(connection1)
        
        return connection1, connection2
    

    def add_connection_mutation(self, node1: Node, node2: Node, global_innovation_number: int): 
        """
        Mutation: add a new connection to the network.
        
        If the connection already exists, it is enabled and assigned a new weight.
        Otherwise, a new connection is created and added to the genome.
        
        Returns:
            ConnectionGene: The new connection that was added to the genome.
        """
        
        excisting_connection = self.check_existing_connection(node1, node2)
        
        # If the connection is already a in the genome, make sure it's enabled and assign it a new weight
        if excisting_connection:
            excisting_connection.is_enabled = True
            excisting_connection.weight = self.random_weight_mutation()
            return excisting_connection
        
        connection = ConnectionGene(node1, node2, self.random_weight_mutation(), True, global_innovation_number)
        
        self.add_connection(connection)
        node1.add_outgoing_connection(connection) # The genome needs a list of outgoing connections for Kahns algorithm
        return connection
    
    def random_weight_mutation(self):
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
        """ Returns all nodes in the genome. """
        return self.output_nodes + self.input_nodes + self.hidden_nodes
    
    def __repr__(self):
        return (f"Genome(id={self.id}, hidden nodes={[node.id for node in self.hidden_nodes]}, "
                f"connections={[connection for connection in self.connections]}, fitness_value={self.fitness_value})")

