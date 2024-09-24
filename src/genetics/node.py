from src.genetics.genome import Genome
from src.genetics.connection_gene import ConnectionGene

class Node:
    """
    A node in a neural network.
    Has a unique id and a type.
    """

    def __init__(self, id: int, type: str, value: float = 0.0):
        self.id = id
        self.type = type
        self.connected_nodes = [] #hmm
        self.connections_to_output = []
        self.value = value
        
        """
        Type is one of the following:
        - input
        - hidden
        - output 
        """
    def set_value(self, value: float):
        if type == "input":
            self.value = value

    def update_value(self, value: float):
        self.value += value

    def add_node_connection(self, node:'Node'):
        self.connected_nodes.append(node)

    def add_connection_connection(self, connection: 'ConnectionGene'):
        self.connections_to_output.append(connection)

    def __repr__(self):
        return f"Node(id={self.id}, type={self.type})"


if __name__ == '__main__':
    esel = Genome(1)
    node1 = Node(1, 'input')
    node2 = Node(2, 'output')
    connection1 = ConnectionGene(node1, node2, 3.4, True, 1)
    esel.add_connection(connection1)
    print(esel)
    print(node1)
    print(connection1)