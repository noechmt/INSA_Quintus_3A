from Walker import *
from TimerEvent import *

class Cell: #Une case de la map
    def __init__(self, x, y, map):
        self.x = x #coordonnée dans le tableau : int
        self.y = y #coordonnée dans le tableau : int
        self.map = map
        self.water = False

    #Check if these coordinates are in the map
    def inMap(self, x,y):
        return (0 <= x and x <= self.map.size-1 and 0 <= y and y <= self.map.size-1)

    #Return an cell array which match with the class type (ex: Path, Prefecture (not a string)) in argument
    def check_cell_around(self, type) :
        path = []
        for i in range(-1, 2) :
            for j in range(-1, 2) : 
                if abs(i) != abs(j) and self.inMap(self.x + i, self.y + j):
                    if isinstance(self.map.getCell(self.x + i,self.y + j), type):
                        path.append(self.map.getCell(self.x + i, self.y + j))
        return path

    def build(self, type):
        if isinstance(self, Empty) and self.type == "dirt":
            match type:
                case "path":
                    self.map.setCell(self, Path(self.x, self.y, self.map))
                    self.map.wallet -= 4 
                case "house":
                    self.map.setCell(self, House(self.x, self.y, self.map))
                    self.map.wallet -= 10
                case "well":
                    self.map.setCell(self, Well(self.x, self.y, self.map))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.setCell(self, Prefecture(self.x, self.y, self.map))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.setCell(self, EngineerPost(self.x, self.y, self.map))
                    self.map.wallet -= 30

class Path(Cell):
    def __init__(self, x, y, my_map, my_path_level=0):
        super().__init__(x, y, my_map)
        self.level = my_path_level

    def __str__(self):
        return f"Chemin { self.level}"

class Empty(Cell):
    def __init__(self, x, y, my_map, type="dirt"):
        super().__init__(x, y, my_map)
        self.type = type #"dirt", "tree", "water", "rock"
        self

    def __str__(self):
        return self.type

    def clear(self):
        if self.type == "tree" :
            self.type = "dirt" 
            self.map.wallet -= 2

    def canBuild(self) : 
        return self.type == "dirt"  


class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x,y, my_map):
        super().__init__(x, y, my_map)
        self.state = "build" #état (détruit ou pas) 

    def destroy(self) : 
        self.state = "destroyed"
                     
class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, my_map, level=0, nb_occupants=0) :
        super().__init__(x, y, my_map)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
        self.unemployedCount = 0
        # self.Firetimer.start()
        self.migrant = Migrant(self)

    def __str__(self):
        return f"House { self.level}"

    def nextLevel(self) :
        self.level += 1
        match self.level:
            case 1:
                self.max_occupants = 7
            case 2:
                self.max_occupants = 9


class Well(Building) :
    def __init__(self, x, y, my_map): 
        super().__init__(x, y, my_map)
        # self.CollapseTimer.start()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.inMap(self.x+i, self.y+j):
                    self.map.getCell(self.x+i, self.y+j).water = True
                    checkedCell = self.map.getCell(self.x+i, self.y+i)
                    if isinstance(checkedCell, House) and checkedCell.level == 1 and checkedCell.max_occupants == checkedCell.nb_occupants :
                        checkedCell.nextLevel
                        
    def __str__(self):
        return "Puit"

class Prefecture(Building) :
    def __init__(self, x, y, my_map):
        super().__init__(x, y, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.prefect = Prefect(self)
        # self.CollapseTimer.start()

    def __str__(self):
        return "Prefecture"

class EngineerPost(Building):
    def __init__(self, x, y, my_map):
        super().__init__(x, y, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0

    def __str__(self):
        return "Engineer Post"