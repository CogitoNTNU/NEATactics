import nodes

class Traverse:
    def __init__(self, genome: 'nodes.Genome') -> None:
        self.genome = genome
    
    
    def traverse(self) -> None:
        """
        Traverse through the genome and returns an action
        Using Kahns alorithm to traverse through the genome 
        and insuring that the node that is being traversed has 
        all its incoming connections traversed before it.
        """
        order_of_traversal = self.kahns_algorithm()
        if not order_of_traversal:
            return None
        for node in order_of_traversal:
            for connection in node.connections:
                if connection.is_enabled:
                    self.update_out_node(connection)
        action = self.output(True)
        return action
    
    def kahns_algorithm(self) -> list[nodes.Node]:
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

            for connection in current_node.connections:
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
        
        
    
    def output(self, done: bool) -> int:
        """
        Returns the output-node with the highest value after the traversal is done
        """
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
        """
        Calculates the new value of the out_node in the connection
        """
        
        connection.out_node.value += connection.in_node.value * connection.weight
        return self.activation_function(connection.out_node.value)
    
    def update_out_node(self, connection: 'nodes.ConnectionGene'):
        """
        Updates the out_node value in the connection
        """
        connection.out_node.value += self.calculate_connection(connection)

        
    def activation_function(self, value: float) -> float:
        """
        Applies the ReLU activation function to the value
        """
        if value < 0:
            return 0
        return value 