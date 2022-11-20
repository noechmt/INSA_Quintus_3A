from Building import *
from LaborAdvisor import *


class EngineerPost(Building):
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "engineer post", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0