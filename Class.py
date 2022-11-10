import numpy as np
import math as m

        


class Map:#Un ensemble de cellule
    def __init__(self, size):
        self.size = size #La taille de la map est size*size : int
        self.array = [[Void(i,j, self) for i in range (size)] for j in range(size)] #tableau de cellule (voir classe cellule) : list

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche 

    def display(self):
        print(np.array([[self.array[i][j].type_of_cell for i in range(self.size)] for j in range(self.size)]))



class Cell: #Une case de la map
    def __init__(self, x, y, my_current_map, my_type_of_cell=0, nb_of_entity = 0):
        self.x = x #coordonnée dans le tableau : int
        self.y = y #coordonnée dans le tableau : int
        self.current_map = my_current_map
        self.type_of_cell = my_type_of_cell #type de la cellule (batiments = 2, nature/vide = 0, chemin = 1) : int
        self.nb_of_entity = nb_of_entity #le nombre d'entités présentes sur la case : int
        self.water = False


    def inMap(self):
        return (0 <= self.x & self.x <= self.current_map.size-1 & 0 <= self.y & self.y <= self.current_map.size-1)

    def build(self, type):
        if self.type_of_cell == 0 & self.current_map.array[self.x][self.y].type_of_void == "dirt":
            match type:
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
        self.timer = 0.00 #timer pour le feu : float


class Void(Cell):
    def __init__(self, x, y, my_current_map, my_type_of_void="void nature"):
        super().__init__(x, y, my_current_map, 0)
        self.type_of_void = my_type_of_void #"void nature", "tree filled", "water filled"

    def clear(self):
        if self.type_of_void == "tree filled":
            self.type_of_void = "void nature"
            
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
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y])
        self.employees = 0
        self.prefect = Prefect(self.x, self.y, self.current_map.array[self.x][self.y], self)


class EngineerPost(Building):
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "engineer post", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.current_map.array[self.x][self.y])
        self.employees = 0


class Walker() : 
    def __init__(self, job, position_x, position_y, starting_Cell) :
        self.job = job #le métier (migrant, worker, etc) : int (?)
        self.position_x = position_x #position sur la map : int
        self.position_y = position_y #position sur la map : int
        self.current_Cell = starting_Cell #La cellule de départ de l'entity : Cell
        self.previous_cell = None

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
        if (self.position_x != self.current_Cell.x or self.position_y != self.current_Cell.y ) :
            self.current_Cell.value = self.current_Cell.type #On change la valeur de l'ancienne cellule (?) 
            self.current_Cell = new_cell
            #self.current_Cell.value = ?

    def check_path(self) :
        for i in range(-1, 1) :
            for j in range(-1, 1) : 
                if (abs(i) != abs(j) & self.current_prefecture.current_map.array[self.current_prefecture.x + i][self.current_prefecture.y + j].type_of_cell  == "path") : 
                    self.cell_assignement(self.current_prefecture.current_map.array[self.current_prefecture.x + i][self.current_prefecture.y + j])



class Prefect(Walker) : 
    def __init__(self, position_x, position_y, starting_Cell, current_prefecture):
        super().__init__("prefect" , position_x, position_y, starting_Cell)
        self.prefect_in_building = True
        self.current_prefecture = current_prefecture

    def leave_prefecture(self) : 
        if (self.current_prefecture.employees == 6) :
            for i in range(-1, 1) :
                for j in range(-1, 1) : 
                    if (abs(i) != abs(j) & self.current_prefecture.current_map.array[self.current_prefecture.x + i][self.current_prefecture.y + j].type_of_cell  == "path") : 
                        self.cell_assignement(self.current_prefecture.current_map.array[self.current_prefecture.x + i][self.current_prefecture.y + j])
                        self.prefect_in_building = False 
                        break


    # def prefect_move(self) :
        



class LaborAdvisor(Walker) : 
    def __init__(self, position_x, position_y, starting_Cell):
        super().__init__("labor advisor", position_x, position_y, starting_Cell)
        









myMap = Map(20)
myMap.init_path()
myMap.display()
# myMap.array[1][1] = House(1, 1, myMap)
myMap.array[1][1].build("house")
myMap.display()
#myMap.array[2][2] = Fountain(2, 2, myMap)
myMap.display()
print(myMap.array[1][1].type_of_building)
print(myMap.array[1][1].water)


