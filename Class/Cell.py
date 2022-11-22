from Walker import *
from TimerEvent import *

class Cell: #Une case de la map
    def __init__(self, x, y, my_current_map, my_type_of_cell=0, nb_of_entity = 0):
        self.x = x #coordonnée dans le tableau : int
        self.y = y #coordonnée dans le tableau : int
        self.current_map = my_current_map
        self.type_of_cell = my_type_of_cell #type de la cellule (batiments = 2, nature/vide = 0, chemin = 1) : int
        self.nb_of_entity = nb_of_entity #le nombre d'entités présentes sur la case : int
        self.water = False


    def inMap(self):
        return (0 <= self.x and self.x <= self.current_map.size-1 and 0 <= self.y and self.y <= self.current_map.size-1)

    def inMap(self, x,y):
        return (0 <= x and x <= self.current_map.size-1 and 0 <= y and y <= self.current_map.size-1)

    def build(self, type):
        if self.type_of_cell == 0 and self.current_map.array[self.x][self.y].type_of_void == "dirt":
            match type:
                case "path":
                    self.current_map.array[self.x][self.y] = Path(self.x, self.y, self.current_map)
                case "house":
                    self.current_map.array[self.x][self.y] = House(self.x, self.y, self.current_map)
                case "fountain":
                    self.current_map.array[self.x][self.y] = Fountain(self.x, self.y, self.current_map)
                case "prefecture":
                    self.current_map.array[self.x][self.y] = Prefecture(self.x, self.y, self.current_map)
                case "engineer post":
                    self.current_map.array[self.x][self.y] = EngineerPost(self.x, self.y, self.current_map)

class Path(Cell):
    def __init__(self, x, y, my_current_map, my_path_level=0):
        super().__init__(x, y, my_current_map, 1)
        self.path_level = my_path_level

class Void(Cell):
    def __init__(self, x, y, my_current_map, my_type_of_void="dirt"):
        super().__init__(x, y, my_current_map, 0)
        self.type_of_void = my_type_of_void #"dirt", "tree filled", "water filled"

    def clear(self):
        if self.type_of_void == "tree filled":
            self.type_of_void = "dirt"

class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x,y, my_current_map, my_type_of_building, my_state):
        super().__init__(x, y, my_current_map, 2)
        self.type_of_cell = 2
        self.type_of_building = my_type_of_building  #le type de batiments (house, fountain, ...) : ? 
        self.state = my_state #état (détruit ou pas) 
        self.Firetimer = TimerEvent(self, "fire") #timer pour le feu : TimeEvent
        self.CollapseTimer = TimerEvent(self, "damage") #timer pour les effondrement = : TimeEvent
        self.employees = 0
        match my_type_of_building :
            case "prefecture" :
                self.required_employees = 6
            case "engineer post" : 
                self.required_employees = 5
            case _: 
                self.required_employees = None
    
    def destroy(self) : 
        self.state = "destroyed"

class EngineerPost(Building):
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "engineer post", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0

class Fountain(Building) :
    def __init__(self, x, y, my_current_map) : 
        super().__init__(x, y, my_current_map, "fountain", True)
        self.check_house()
        self.CollapseTimer.start()
    
    def check_house(self) : 
        for i in range(-2, 3):
            for j in range(-2, 3):
                cell = self.current_map.array[self.x+i][self.y+j]
                if cell.type_of_cell == 2:
                    if cell.type_of_building == "house":
                        cell.water = True

class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, my_current_map, level=0, nb_occupants=0) :
        super().__init__(x, y, my_current_map, "house", True)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
        self.Firetimer.start()
    
    def check_fountain(self):
        for i in range(-2, 3):
            for j in range(-2, 3):
                cell = self.current_map.array[self.x+i][self.y+j]
                if cell.type_of_cell == 2:
                    if cell.type_of_building == "fountain":
                        self.water = True

class Prefecture(Building) :
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "prefecture", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0
        self.prefect = Prefect(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.CollapseTimer.start()

