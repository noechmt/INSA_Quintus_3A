from Walker import *
from TimerEvent import *

class Cell: #Une case de la map
    def __init__(self, x, y, map):
        self.x = x #coordonnée dans le tableau : int
        self.y = y #coordonnée dans le tableau : int
        self.map = map
        self.water = False


    def inMap(self, x,y):
        return (0 <= x and x <= self.map.size-1 and 0 <= y and y <= self.map.size-1)

    def build(self, type):
        if isinstance(self, Empty) and self.type == "dirt":
            match type:
                case "path":
                    self.map.setCell(self, Path(self.x, self.y, self.map))
                case "house":
                    self.map.setCell(self, House(self.x, self.y, self.map))
                case "fountain":
                    self.map.setCell(self, Fountain(self.x, self.y, self.map))
                case "prefecture":
                    self.map.setCell(self, Prefecture(self.x, self.y, self.map))
                case "engineer post":
                    self.map.setCell(self, EngineerPost(self.x, self.y, self.map))

class Path(Cell):
    def __init__(self, x, y, my_map, my_path_level=0):
        super().__init__(x, y, my_map)
        self.level = my_path_level

class Empty(Cell):
    def __init__(self, x, y, my_map, type="dirt"):
        super().__init__(x, y, my_map)
        self.type = type #"dirt", "tree", "water", "rock"

    def clear(self):
        if self.type == "tree":
            self.type = "dirt"

class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x,y, my_map):
        super().__init__(x, y, my_map)
        self.state = "build" #état (détruit ou pas) 
        self.Firetimer = TimerEvent(self, "fire") #timer pour le feu : TimeEvent
        self.CollapseTimer = TimerEvent(self, "damage") #timer pour les effondrement = : TimeEvent
        self.employees = 0
        # match my_type_of_building :
        #     case "prefecture" :
        #         self.required_employees = 6
        #     case "engineer post" : 
        #         self.required_employees = 5
        #     case _: 
        #         self.required_employees = None
    
    def destroy(self) : 
        self.state = "destroyed"
                     
class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, my_map, level=0, nb_occupants=0) :
        super().__init__(x, y, my_map)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
        self.Firetimer.start()

class Fountain(Building) :
    def __init__(self, x, y, my_map): 
        super().__init__(x, y, my_map)
        self.CollapseTimer.start()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.inMap(self.x+i, self.y+j):
                    self.map.getCell(self.x+i, self.y+j).water = True

class Prefecture(Building) :
    def __init__(self, x, y, my_map):
        super().__init__(x, y, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.prefect = Prefect(self)
        self.CollapseTimer.start()

class EngineerPost(Building):
    def __init__(self, x, y, my_map):
        super().__init__(x, y, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0