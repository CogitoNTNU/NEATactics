import nodes

class Traverse:
    def __init__(self, genome: 'nodes.Genome') -> None:
        self.genome = genome
    
    
    def traverse(self, genome: 'nodes.Genome') -> None:
        for node in genome.nodes:
            print(node.id)
            print(node.connections)
            print(node.type)
            print(node.value)
        
        for connection in genome.connections:
            print(connection.in_node)
            print(connection.out_node)
            print(connection.weight)
            print(connection.is_enabled)
            print(connection.innovation_number)
    
    def output(self, done: bool) -> int:
        # Returns the output after the network is done
        # Finds the output node with highest value and returns it
        output = -1
        highest_value = 0
        if done:
            for node in self.genome.output_nodes:
                if node.value > highest_value:
                    highest_value = node.value
                    output = node.id
        else:
            return -1
        return output
    
    def calculate_connection(self, connection: 'nodes.ConnectionGene'):
        # Calculates the new value of the out_node in the connection
        out_value = connection.in_node.value * connection.weight
        return self.activation_function(out_value)
    
    def update_out_node(self, connection: 'nodes.ConnectionGene'):
        # Updates the out_node value with the new value
        connection.out_node.value += self.calculate_connection(connection)

        
    def activation_function(self, value: float) -> float:
        # ReLu Activation function
        if value < 0:
            return 0
        return value 