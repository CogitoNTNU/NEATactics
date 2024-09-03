class Node:
    def __init__(self, id: int, type: str):
        self.id = id
        self.type = type

class Connections:
    def __init__(self, in_node: Node, out_node: Node, weight: float, is_enabeled: bool, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.is_enabeled = is_enabeled
        self.innovation_number = innovation_number
    
