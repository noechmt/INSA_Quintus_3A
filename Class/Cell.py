from Class.Walker import *
import pygame

class Cell: #Une case de la map
    def __init__(self, x, y, height, width, screen, map):
        self.x = x #coordonnée dans le tableau : int
        self.y = y #coordonnée dans le tableau : int
        self.height = height
        self.width = width
        self.map = map
        self.water = False
        self.sprite = None
        self.screen = screen
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.x_screen = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + self.width*self.x/2 - self.width*self.y/2
        self.y_screen = self.HEIGHT_SCREEN/6 + self.x * self.height/2 + self.y * self.height/2

    def display(self):
        self.screen.blit(pygame.transform.scale(self.sprite, (self.width, self.height)), (self.x_screen, self.y_screen))

    def inMap(self, x,y):
        return (0 <= x and x <= self.map.size-1 and 0 <= y and y <= self.map.size-1)

    def build(self, type):
        if self.map.array[self.x][self.y].type_of_void == "dirt":
            match type:
                case "path":
                    self.map.array[self.x][self.y] = Path(self.x, self.y, self.map)
                case "house":
                    self.map.array[self.x][self.y] = House(self.x, self.y, self.map)
                case "fountain":
                    self.map.array[self.x][self.y] = Fountain(self.x, self.y, self.map)
                case "prefecture":
                    self.map.array[self.x][self.y] = Prefecture(self.x, self.y, self.map)
                case "engineer post":
                    self.map.array[self.x][self.y] = EngineerPost(self.x, self.y, self.map)

class Path(Cell):
    def __init__(self, x, y, my_current_map, my_path_level=0):
        super().__init__(x, y, my_current_map, 1)
        self.path_level = my_path_level

class Empty(Cell):
    def __init__(self, x, y, height, width, map, screen, type_empty="dirt"):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty #"dirt", "trees", "water", #"rocks"
        self.sprite = pygame.image.load("game_screen/game_screen_sprites/" + self.type_empty + "_" + str(1) + ".png")
        self.display()

    def clear(self):
        if self.type_of_void == "tree":
            self.type_of_void = "dirt"
            # draw function

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

class EngineerPost(Building):
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "engineer post", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.map.array[self.x][self.y], self)
        self.employees = 0

class Fountain(Building) :
    def __init__(self, x, y, my_current_map) : 
        super().__init__(x, y, my_current_map, "fountain", True)
    
    def check_house(self) : 
        for i in range(-2, 3):
            for j in range(-2, 3):
                cell = self.map.array[self.x+i][self.y+j]
                if cell.type_of_cell == 2:
                    if cell.type_of_building == "house":
                        cell.water = True

class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, my_current_map, level=0, nb_occupants=0) :
        super().__init__(x, y, my_current_map, "house", True)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
    
    def check_fountain(self):
        for i in range(-2, 3):
            for j in range(-2, 3):
                cell = self.map.array[self.x+i][self.y+j]
                if cell.type_of_cell == 2:
                    if cell.type_of_building == "fountain":
                        self.water = True

class Prefecture(Building) :
    def __init__(self, x, y, my_current_map):
        super().__init__(x, y, my_current_map, "prefecture", True)
        self.labor_advisor = LaborAdvisor(self.x, self.y, self.map.array[self.x][self.y], self)
        self.employees = 0
        self.prefect = Prefect(self.x, self.y, self.map.array[self.x][self.y], self)
