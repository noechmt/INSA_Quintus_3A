from Path import *
from House import *
from Fountain import *
from Prefecture import *
from EngineerPost import *

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