from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.genetics.node import Node


class ConnectionGene:
    """
    Quote from the NEAT paper, Section II A: Genetic encoding:

    "Each connection gene specifies the in-node, the out-node, the weight of the connection, whether
    or not the connection gene is expressed (enable bit), and an innovation number, which allows finding
    corresponding genes during crossover."
    """

    def __init__(
        self,
        in_node: "Node",
        out_node: "Node",
        weight: float,
        is_enabled: bool,
        global_innovation_number: int,
    ):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.is_enabled = is_enabled
        self.innovation_number = global_innovation_number

    def get_connection_weight(self):
        return self.weight

    def __repr__(self):
        return (
            f"ConnectionGene(in_node={self.in_node.id}, out_node={self.out_node.id}, "
            f"weight={self.weight}, is_enabled={self.is_enabled}, innovation_number={self.innovation_number})"
        )
