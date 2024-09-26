import random
from src.genetics.connection_gene import ConnectionGene
from src.genetics.node import Node
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.genetics.node import Node


class Genome:
    """
    Represents some neural network.
    It has a unique id, and contains a set of nodes and connections. 
    """
    def __init__(self, id: int):
        self.id = id
        self.nodes: list['Node'] = []
        self.connections: list[ConnectionGene] = []
        self.output_nodes = []

    

    def add_node(self, node: 'Node'):
        self.nodes.append(node)
        if node.type == 'output':
            self.output_nodes.append(node)

    def add_connection(self, connection: 'ConnectionGene'):
        self.connections.append(connection)
        
    def disable_connection(self, connection:'ConnectionGene'):
        #self.connections.remove(connection)
        connection.is_enabled = False
    
    def add_node_mutation(self, connection:'ConnectionGene', node_id: int, global_innovation_number: int):
        node1 = connection.in_node
        node2 = connection.out_node
        new_node = Node(node_id, 'hidden')
        self.add_node(new_node)
        
        connection1 = ConnectionGene(node1, new_node, 1, True, global_innovation_number)
        global_innovation_number += 1 #Hvordan funker innovation number? Skal de to nye connections ha ulike innovation numbers?
        connection2 = ConnectionGene(new_node, node2, connection.weight, True, global_innovation_number)
        global_innovation_number += 1
        self.disable_connection(connection)
        self.add_connection(connection1)    
        self.add_connection(connection2)
        node2.add_node_connection(new_node)
        node1.add_node_connection(new_node)
        new_node.add_node_connection(node1)
        new_node.add_node_connection(node2)
        new_node.add_connection_connection(connection2)
        node1.add_connection_connection(connection1)
    

    def add_connection_mutation(self, node1: 'Node', node2: 'Node', global_innovation_number: int):
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
        weight = self.get_weight()
        if self.is_valid_connection(node1, node2):
            connection = ConnectionGene(node1, node2, weight, True, global_innovation_number)
            global_innovation_number += 1
            self.add_connection(connection)
            node2.add_node_connection(node1)
            node1.add_node_connection(node2)
            node1.add_connection_connection(connection)
            return True
        else:
            return False
    
    def get_weight(self):
        return 2*random.random() - 1  #TODO Make this better. Chooses a random value between -1 and 1 for the new weight

    def weight_mutation(self, connection: 'ConnectionGene'):
        connection.weight = self.get_weight() #TODO Make this better. Chooses a random value between -1 and 1 for the new weight

    def is_valid_connection(self, node1: 'Node', node2: 'Node') -> bool:
        # check if it is valid to add a connection between two nodes
        # not valid if node1 is output, node2 is input or if they are the same node.
        # (Maybe other restrictions) 
        if node1.id == node2.id:
            return False
        elif node1.type == "output":
            return False
        elif node2.type == "input":
            return False
        elif node1.id in node2.connected_nodes: # TODO Hva skjer hvis connectionen er disabled? svar: enable og oppdater vekten 
            return False
        else:
            return True
    def get_nodes(self):
        return self.nodes
    def __repr__(self):
        return (f"Genome(id={self.id}, nodes={[node.id for node in self.nodes]}, "
                f"connections={[connection.is_enabled for connection in self.connections]})")

