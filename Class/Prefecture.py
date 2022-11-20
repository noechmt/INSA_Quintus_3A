from Building import *
from LaborAdvisor import *
from Prefect import *

class Prefecture(Building) :
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "prefecture", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0
        self.prefect = Prefect(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.CollapseTimer.start()

