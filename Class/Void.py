from Cell import *


class Void(Cell):
    def __init__(self, x, y, my_current_map, my_type_of_void="dirt"):
        super().__init__(x, y, my_current_map, 0)
        self.type_of_void = my_type_of_void #"dirt", "tree filled", "water filled"

    def clear(self):
        if self.type_of_void == "tree filled":
            self.type_of_void = "dirt"
            
