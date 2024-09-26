from species import Species
from src.utils.config import Config

class NEAT:
    def __init__(self, config: Config):
        self.config = config
        self.innovation_number = 0
        self.species = []
        
    def start(self): 
        # Everyone starts in the same species
        self.species += Species(self.config)
        # Initialize random population

        for _ in range(self.config.population_size):
            pass
            
