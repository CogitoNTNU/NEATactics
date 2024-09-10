
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

    def __repr__(self):
        return (f"Genome(id={self.id}, nodes={[node.id for node in self.nodes]}, "
                f"connections={[connection.innovation_number for connection in self.connections]})")

class Node:
    """
    A node in a neural network.
    Has a unique id and a type.
    """
    def __init__(self, id: int, type: str):
        self.id = id

        self.type = type
        """
        Type is one of the following:
        - Input
        - Hidden
        - Output 
        """

    def __repr__(self):
        return f"Node(id={self.id}, type={self.type})"

class ConnectionGene:
    """
    Quote from the NEAT paper, Section II A: Genetic encoding:

    "Each connection gene specifies the in-node, the out-node, the weight of the connection, whether
    or not the connection gene is expressed (enable bit), and an innovation number, which allows finding
    corresponding genes during crossover."
    """   

    def __init__(self, in_node: Node, out_node: Node, weight: float, is_enabled: bool, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight 
        self.is_enabled = is_enabled 
        self.innovation_number = innovation_number 

    def __repr__(self):
        return (f"ConnectionGene(in_node={self.in_node.id}, out_node={self.out_node.id}, "
                f"weight={self.weight}, is_enabled={self.is_enabled}, innovation_number={self.innovation_number})")

if __name__ == '__main__':

    esel = Genome(1)
    node1 = Node(1, 'input')
    node2 = Node(2, 'output')
    connection1 = ConnectionGene(node1, node2, 3.4, True, 1)
    print(esel)
    print(node1)
    print(connection1)