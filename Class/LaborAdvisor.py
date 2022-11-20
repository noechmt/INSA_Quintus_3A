from Walker import *

class LaborAdvisor(Walker) : 
    def __init__(self, position_x, position_y, starting_Cell, building):
        super().__init__("labor advisor", position_x, position_y, starting_Cell, building)

