from Walker import *
import random

class Prefect(Walker) : 
    def __init__(self, position_x, position_y, starting_Cell, current_prefecture):
        super().__init__("prefect" , position_x, position_y, starting_Cell, "prefecture")
        self.prefect_in_building = True
        self.current_building = current_prefecture

    def prefect_move(self) :
        if not(self.prefect_in_building):
            path = self.check_path()
            if (len(path) == 1):
                self.cell_assignement(path[0])
            else:
                path.remove(self.previous_cell)
                self.cell_assignement(random.choice(path))
        print("Prefect is moving on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

