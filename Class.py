import numpy as np
import math as m
import threading as th
import random

        


class Map:#Un ensemble de cellule
    def __init__(self, size):
        self.size = size #La taille de la map est size*size : int
        self.array = [[Void(j,i, self) for i in range (size)] for j in range(size)] #tableau de cellule (voir classe cellule) : list
        self.walker_list = []

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche 

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell) for i in range(self.size)] for j in range(self.size)]))



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
            
class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x,y, my_current_map, my_type_of_building, my_state):
        super().__init__(x, y, my_current_map, 2)
        self.type_of_cell = 2
        self.type_of_building = my_type_of_building  #le type de batiments (house, fountain, ...) : ? 
        self.state = my_state #état (détruit ou pas) 
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


class Void(Cell):
    def __init__(self, x, y, my_current_map, my_type_of_void="dirt"):
        super().__init__(x, y, my_current_map, 0)
        self.type_of_void = my_type_of_void #"dirt", "tree filled", "water filled"

    def clear(self):
        if self.type_of_void == "tree filled":
            self.type_of_void = "dirt"
            
class Path(Cell):
    def __init__(self, x, y, my_current_map, my_path_level=0):
        super().__init__(x, y, my_current_map, 1)
        self.path_level = my_path_level


class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, my_current_map, level=0, nb_occupants=0) :
        super().__init__(x, y, my_current_map, "house", True)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
    
    def check_fountain(self):
        for i in range(-2, 3):
            for j in range(-2, 3):
                cell = self.current_map.array[self.x+i][self.y+j]
                if cell.type_of_cell == 2:
                    if cell.type_of_building == "fountain":
                        self.water = True


        
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
                

class Prefecture(Building) :
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "prefecture", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0
        self.prefect = Prefect(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.CollapseTimer.start()


class EngineerPost(Building):
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "engineer post", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y], self)
        self.employees = 0


class Walker() : 
    def __init__(self, job, position_x, position_y, starting_Cell, building) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.position_x = position_x #position sur la map : int
        self.position_y = position_y #position sur la map : int
        self.current_Cell = starting_Cell #La cellule de départ de l'entity : Cell
        self.previous_cell = None
        self.current_Cell.current_map.walker_list.append(self)
        self.Walkers_building = building #string (prefecture, engineer post, house)
        
        

    def move_up(self) : #bouger d'une case vers le haut
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_y += 1

    def move_down(self) : #bouger d'une case vers le bas
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_y -= 1

    def move_left(self) : #bouger d'une case vers la gauche
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_x -= 1
 
    def move_right(self) : #bouger d'une case vers la droite
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_x += 1
    
    def cell_assignement(self, new_cell) : #si la position est différente des coordonnées de la cellule, on change current_Cell
        #if (self.position_x != self.current_Cell.x or self.position_y != self.current_Cell.y ) :
            self.previous_cell = self.current_Cell
            self.current_Cell = new_cell

    def check_path(self) :
        path = []
        for i in range(-1, 2) :
            for j in range(-1, 2) : 
                if abs(i) != abs(j) and self.current_Cell.inMap(self.current_Cell.x + i, self.current_Cell.y + j):
                    if self.current_Cell.current_map.array[self.current_Cell.x + i][self.current_Cell.y + j].type_of_cell  == 1:
                        path.append(self.current_Cell.current_map.array[self.current_Cell.x + i][self.current_Cell.y + j])
        return path

    def leave_building(self) :
        #if (self.Walkers_building.employees == self.Walkers_building.required_employees) :
            for i in range(-1, 2) :
                #print(abs(i))
                for j in range(-1, 2) :
                    #print("Test : " + str(self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j].type_of_cell)) 
                    if abs(i) != abs(j) and self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j].type_of_cell  == 1: 
                        #print("Test : " + str(self.current_building.x + i) + ";" + self.current_building.y + j)
                        self.cell_assignement(self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j])
                        self.prefect_in_building = False 
                        break
            print("Prefect is leaving the building on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

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

        
class LaborAdvisor(Walker) : 
    def __init__(self, position_x, position_y, starting_Cell, building):
        super().__init__("labor advisor", position_x, position_y, starting_Cell, building)




# class TimerEvent :
#     def __init__(self, building, type_of_event) :
#         self.building = building
#         match type_of_event :
#             case "fire" :
#                 self.timer = th.Timer(120, self.building.destroy())
#             case "damage" : 
#                 self.timer = th.Timer(240, self.building.destroy()) # pas les vrais valeur
    
#     def start(time):
#         pass


    
        









myMap = Map(5)
myMap.init_path()
myMap.display()
# myMap.array[1][1] = House(1, 1, myMap)
myMap.array[1][1].build("house")

#myMap.array[2][2] = Fountain(2, 2, myMap)
myMap.array[3][0].build("prefecture")
myMap.array[3][2].build("path")
myMap.array[2][2].build("path")
myMap.array[2][3].build("path")
myMap.array[2][4].build("path")
myMap.array[3][4].build("path")
myMap.display()
myMap.array[3][0].prefect.leave_building()
for i in range(15):
    myMap.array[3][0].prefect.prefect_move()
print(myMap.array[1][1].type_of_building)
print(myMap.array[1][1].water)


