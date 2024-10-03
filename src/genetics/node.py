from src.genetics.connection_gene import ConnectionGene
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from src.genetics.genome import Genome

class Node:
    """A node in a neural network. Has a unique id and a type."""
    VALID_TYPES = {"input", "hidden", "output", "bias"}

    def __init__(self, id: int, type: str, value: float = 0.0):
        
        self.id = id
        self.type = self._validate_type(type)
        """Type is one of the following: {input, hidden, output, "bias"}"""
        self.connected_nodes: List[int] = [] #hmm
        self.connections_to_output = []
        self.value = value

    def _validate_type(self, type: str) -> str:
        if type not in self.VALID_TYPES:
            raise ValueError(f"Invalid type: '{type}'. Must be one of the following: {self.VALID_TYPES}")
        return type

    def set_value(self, value: float):
        if self.type == "input":
            self.value = value
        else:
            raise Exception("Only the input nodes should get different values!")

    def update_value(self, value: float):
        self.value += value

    def add_node_connection(self, nodeId: int):
        self.connected_nodes.append(nodeId)

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