
import random
# TODO: Rudimentary NN structure which can interact with the environment.

class Genome:
    """
    Represents some neural network.
    It has a unique id, and contains a set of nodes and connections. 
    """
    def __init__(self, id: int):
        self.id = id
        self.nodes: list[Node] = []
        self.connections: list[ConnectionGene] = []

    def add_node(self, node: 'Node'):
        self.nodes.append(node)

    def add_connection(self, connection: 'ConnectionGene'):
        self.connections.append(connection)
        
    def disable_connection(self, connection:'ConnectionGene'):
        #self.connections.remove(connection)
        connection.is_enabled = False
    
    def add_node_mutation(self, connection:'ConnectionGene', node_id: int, node_type, global_innovation_number: int):
        node1 = connection.in_node
        node2 = connection.out_node
        
        # Checking to see if you can add the new node or not
        if node1.layer_number > node2.layer_number:
            return
        
        new_node_layer_number = node1.layer_number * 0.5 + node2.layer_number * 0.5 
        new_node = self.Node(node_id, node_type, new_node_layer_number)
        self.add_node(new_node)
        
        connection1 = ConnectionGene(node1, new_node, 1, True, global_innovation_number)
        # global_innovation_number += 1, Hvordan funker innovation number? Skal de to nye connections ha ulike innovation numbers?
        connection2 = ConnectionGene(new_node, node2, connection.weight, True, global_innovation_number )
        self.disable_connection(connection)
        self.add_connection(connection1)    
        self.add_connection(connection2)
    
    def add_connection_mutation(self, node1: 'Node', node2: 'Node', global_innovation_number: int):
        weight = self.get_weight()
        if self.is_valid_connection(self, node1, node2):
            connection = ConnectionGene(node1, node2, weight, True, global_innovation_number)
        self.add_connection(connection)
    
    def get_weight():
        return 2*random.random() - 1  #TODO Make this better. Chooses a random value between -1 and 1 for the new weight

    def weight_mutation(self, connection: 'ConnectionGene'):
        connection.weight = self.get_weight() #TODO Make this better. Chooses a random value between -1 and 1 for the new weight

    def is_valid_connection(self, node1: 'Node', node2: 'Node') -> bool:
        # check if it is valid to add a connection between two nodes
        # not valid if both are outputs, both are inputs, there exists a previous connection between them
        # or other setrictions
        if node1.id == node2.id:
            return False
        elif node1.type == "output" and node2.type == "output":
            return False
        elif node1.type == "input" and node2.type == "input":
            return False
        elif node1.id in node2.connected_nodes: # TODO Hva skjer hvis connectionen er disabled? svar: enable og oppdater vekten 
            return False
        elif node1.layer_number > node2.layer_number:
            return False
        else:
            return True

    def __repr__(self):
        return (f"Genome(id={self.id}, nodes={[node.id for node in self.nodes]}, "
                f"connections={[connection.innovation_number for connection in self.connections]})")

class Node:
    """
    A node in a neural network.
    Has a unique id and a type.
    """
    def __init__(self, id: int, type: str, value: float = 0.):
        self.id = id
        self.type = type
        self.connected_nodes = []
        self.value = value
        """
        Type is one of the following:
        - Input
        - Hidden
        - Output 
        """
        
    def add_connection(self, node:'Node'):
        self.connected_nodes.append(node.id)

    def __repr__(self):
        return f"Node(id={self.id}, type={self.type})"

class ConnectionGene:
    """
    Quote from the NEAT paper, Section II A: Genetic encoding:

    "Each connection gene specifies the in-node, the out-node, the weight of the connection, whether
    or not the connection gene is expressed (enable bit), and an innovation number, which allows finding
    corresponding genes during crossover."
    """   

    def __init__(self, in_node: Node, out_node: Node, weight: float, is_enabled: bool, global_innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight 
        self.is_enabled = is_enabled 
        self.innovation_number = global_innovation_number


    def __repr__(self):
        return (f"ConnectionGene(in_node={self.in_node.id}, out_node={self.out_node.id}, "
                f"weight={self.weight}, is_enabled={self.is_enabled}, innovation_number={self.innovation_number})")


if __name__ == '__main__':
    esel = Genome(1)
    node1 = Node(1, 'input')
    node2 = Node(2, 'output')
    connection1 = ConnectionGene(node1, node2, 3.4, True, 1)
    esel.add_connection(connection1)
    print(esel)
    print(node1)
    print(connection1)