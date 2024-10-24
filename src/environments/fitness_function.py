from gym_super_mario_bros.actions import SIMPLE_MOVEMENT 
"""
Things that matter
Positive:
- distance
- killing enemies (?)
- coins
- win


Negative:
- times standing still
- death
- Holding down the jump button
- Time used
"""

"""
done is a boolean value, either True or False.
done = True if you die or grab the flag, else False.

info is a dictionary with length 10.

{
coins: int
flag_get: bool
life: int
score: int
stage: int
status: str
time: int
world: int
x_pos: int
y_pos: int
}
"""

"""
TODO: Another good way is to implent the fitness function from https://medium.com/@savas/craig-using-neural-networks-to-learn-mario-a76036b639ad 
def fitness(xpos, time):
    if xpos > 350:
        return xpos + 0.1* (400-time)
    else:
        return xpos
"""



class Fitness:
    def __init__(self) -> None:
        self.fitness = 0.0
        
        self.prev_lives = 2
        self.prev_pos = 0
        self.stand_still_time = 0
        self.prev_action = 0
        self.prev_num_coins = 0
        # Rewards
        self.rewards = {
            "lose_life": -5,
            "win": 100,
            "move_forward": 0.01,
            "move_backward": -0.005,
            "dont_move_forward": -0.005,
            "coins": 1,
            "score": 0.001,
            "jump_multiple": 0,
            "time": -0.00001,
        }
        

    def calculate_fitness(self, info, action):
        """
        The fitness function that descides how good the genome is. 
        This only works for SIMPLE_MOVEMENT movement scheme.
        """


        # Win #################
        if info["flag_get"]:
            self.fitness += self.rewards["win"]
        ########################
        
        # Score ################
        self.fitness += info["score"] * self.rewards["score"]

        # Lose #########################
        if info["life"] < self.prev_lives:
            self.prev_lives = info["life"]
            self.fitness += self.rewards["lose_life"]
        ###################################

        # Move x-dir ################
        if (info["x_pos"] - self.prev_pos) < -0.001:  # Moving backward
            self.fitness += (self.prev_pos - info["x_pos"]) * self.rewards["move_backward"]
        elif (info["x_pos"] - self.prev_pos) < 0.001:  # Not moving forward
            self.fitness += self.rewards["dont_move_forward"]
        else:  # Moving forward
            self.fitness += (info["x_pos"] - self.prev_pos) * self.rewards["move_forward"]
        self.prev_pos = info["x_pos"]
        #################################

        # Time #########################
        self.fitness += info["time"] * self.rewards["time"]
        ###################################


        # Jump multiple times in a row ####
        # if action == self.prev_action and (SIMPLE_MOVEMENT[action] == ["right", "A"] or SIMPLE_MOVEMENT[action] == ["A"] or SIMPLE_MOVEMENT[action] == ["right", "A", "B"]):
        #    self.fitness += self.rewards["jump_multiple"]
        #    print("JUMP MULTIPLE")
        ##############################
            
        # Stand still
        #if SIMPLE_MOVEMENT[action] == ["NOOP"]:
        #    print("STAND STILL")
        #    self.stand_still_time += 1
        #    self.fitness += self.stand_still_time * self.rewards["stand_still"]
        #else:
        #    self.stand_still_time = 0
        #################################

        # Collect coin #################
        if info["coins"] > self.prev_num_coins:
            self.fitness += self.rewards["coins"]
            self.prev_num_coins = info["coins"]

        # Saves the previous action to use for fitness in the next frame
        #self.prev_action = action

    def get_fitness(self):
        return self.fitness if self.fitness > 0 else 0



