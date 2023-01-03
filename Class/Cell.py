from Class.Walker import *
import pygame
from random import *
import random

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

class Cell: #Une case de la map
    def __init__(self, x, y, height, width, screen, map):
        self.x = x
        self.y = y 
        self.height = height
        self.width = width
        self.map = map
        self.water = False
        self.sprite = None
        self.screen = screen
        self.hovered = False
        self.type = ""
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + self.width*self.x/2 - self.width*self.y/2
        self.top = self.HEIGHT_SCREEN/6 + self.x * self.height/2 + self.y * self.height/2

    def display(self):
        if self.type  == "empty_tree":
            self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*48/30)), (self.left, self.top-self.height*18/30))
        elif self.type == "empty_rock":
            self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*35/30)), (self.left, self.top-self.height*5/30))
        

        self.screen.blit(pygame.transform.scale(self.sprite, (self.width, self.height)), (self.left, self.top))

    def is_hovered(self, pos):
        # Initialize the number of intersections to 0
        intersections = 0

        polygon = self.get_points_polygone()

        # Iterate over the polygon's sides
        for i in range(len(polygon)):
            # Get the coordinates of the current side
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)]

            # Check if the line from the point to the edge of the polygon intersects with the current side
            if min(y1, y2) < pos[1] <= max(y1, y2):
                # Calculate the x-coordinate of the intersection
                x = (pos[1] - y1) * (x2 - x1) / (y2 - y1) + x1

                # If the x-coordinate of the intersection is greater than the point's x-coordinate, increment the number of intersections
                if x > pos[0]:
                    intersections += 1
        # If the number of intersections is odd, the point is inside the polygon
        return intersections % 2 == 1
        
        

    def handle_hover_button(self, pos):
        is_hovered = self.is_hovered(pos)
        if is_hovered and not self.hovered:
            self.hovered = True
            draw_polygon_alpha(self.screen, (0, 0, 0, 85), self.get_points_polygone())
        if not is_hovered and self.hovered:
            self.hovered = False
            self.display()
            self.grid()

    def get_points_polygone(self):
        return ((self.left + self.width / 2, self.top), (self.left, self.top + self.height / 2),
        (self.left + self.width/2, self.top + self.height), (self.left + self.width, self.top + self.height / 2))

    def get_points_rectangle(self):
        return (self.left, self.top, self.left + self.width, self.top + self.height)

    def get_size(self):
        return (self.width, self.height)
    
    def get_pos(self):
        return (self.left, self.top)

    def get_hover(self):
        return self.hover

    def set_hover(self, hover):
        self.hover = hover


    def inMap(self, x,y):
        return (0 <= x and x <= self.map.size-1 and 0 <= y and y <= self.map.size-1)

    def build(self, type):
        if self.map.array[self.x][self.y].type_of_void == "dirt":
            match type:
                case "path":
                    self.map.array[self.x][self.y] = Path(self.x, self.y, self.map)
                #case "house":
                #    self.map.array[self.x][self.y] = House(self.x, self.y, self.map)
                #case "fountain":
                #    self.map.array[self.x][self.y] = Fountain(self.x, self.y, self.map)
                #case "prefecture":
                #    self.map.array[self.x][self.y] = Prefecture(self.x, self.y, self.map)
                #case "engineer post":
                #    self.map.array[self.x][self.y] = EngineerPost(self.x, self.y, self.map)

    def grid(self):
        (top, left, bot, right) = self.get_points_polygone()
        self.x_screen = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + self.width*self.x/2 - self.width*self.y/2
        self.y_screen = self.HEIGHT_SCREEN/6 + self.x * self.height/2 + self.y * self.height/2
        pygame.draw.line(self.screen, (0, 0, 0), top, right, 1)
        pygame.draw.line(self.screen, (0, 0, 0), right, bot, 1)
        pygame.draw.line(self.screen, (0, 0, 0), bot, left, 1)
        pygame.draw.line(self.screen, (0, 0, 0), left, top, 1)

class Path(Cell):
    def __init__(self, x, y, my_current_map, my_path_level=0):
        super().__init__(x, y, my_current_map, 1)
        self.path_level = my_path_level

class Empty(Cell):
    def __init__(self, x, y, height, width, screen, map, type_empty="dirt"):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty #"dirt", "trees"
        self.type = "empty"

        tree_or_dirt_list = ["tree", "dirt"]
        rock_or_dirt_list = ["rock", "dirt"]
        
        #place the trees
        for i in range (40):
            for j in range (40):

                if (x,y)==(i,j) and (0<i<40 and 0<j<40):
                    self.type_empty = random.choice(tree_or_dirt_list)
                    if self.type_empty == "tree":
                        self.type = "empty_tree"
                
        #place the rocks
        for i in range (40):
            for j in range (40):
                
                if (x,y)==(i,j) and ((27<i<36 and 12<j<16) or (27<i<31 and 15<j<23) or (i>30 and j>25) or (i>35 and j<5)):
                    self.type_empty = random.choice(rock_or_dirt_list)
                    if self.type_empty == "rock":
                        self.type = "empty_rock"

                if (x,y)==(i,j) and (i>35 and j>30):
                    self.type = "empty_rock"
                    self.type_empty = "rock"


    #place the water with conditions for sprites
        #river at the top
        for i in range (40):
            
            #line under the first river  
            if ((x,y) == (i,i+10) and i<5) or ((x,y)==(i,i+14) and 5<i<8) or ((x,y)==(i,i+15) and 8<i<13) or ((x,y)==(i,i+18) and 14<i<17) or ((x,y)==(i,i+20) and 17<i<20):
                self.type_empty = "watersiderightD"
            elif ((x,y) == (i,i+11) and i<5) or ((x,y)==(i,i+15) and 4<i<8) or ((x,y)==(i,i+16) and (7<i<13)) or (x,y)==(13,31) or ((x,y)==(i,i+19) and 13<i<17) or ((x,y)==(i,i+21) and 16<i<19):
                self.type_empty = "watersiderightW"
            elif (x,y) == (5,15) or (x,y) == (8,22) or (x,y)==(13,28) or (x,y)==(14,31) or (x,y)==(17,35):
                self.type_empty = "watersidecornerA"
            elif ((x,y) == (5, i) and 15<i<20) or (x,y)==(8,23) or (x,y)==(13,29) or (x,y)==(13,30) or (x,y)==(14,32) or (x,y)==(17,36) or (x,y)==(17,37):
                self.type_empty = "watersideunder"
            
            #line behind the first river
            elif ((x,y) == (i,i+19) and i<10) or ((x,y)==(i,i+26) and 9<i<14):
                self.type_empty = "watersideleftW"
            elif ((x,y) == (i, i+20) and i<9) or ((x,y)==(i,i+27) and 8<i<13):
                self.type_empty = "watersideleftD"
            elif ((x,y)==(9,i) and 28<i<36):
                self.type_empty = "watersideupper"
        
            #full water in the first river
            for j in range (40):
                if (x,y)==(i,j) and ((i<5 and 11+i<j<19+i) or (4<i<8 and 15+i<j<19+i) or (7<i<10 and 16+i<j<19+i) or (9<i<13 and 16+i<j<26+i) 
                    or (i==13 and 18+i<j<26+i) or (13<i<17 and 19+i<j<26+i) or (i==17 and j==39)):
                    self.type_empty = "water"
        
        #river at the bottom
        for i in range (40):

            #line under the second river
            if ((x,y)==(i+31,i) and i<5) or ((x,y)==(i+28,i) and 8<i<12):
                self.type_empty = "watersiderightD"
            elif ((x,y)==(i+30,i) and i<6) or ((x,y)==(i+27,i) and 8<i<13):
                self.type_empty = "watersiderightW"
            elif (x,y)==(36,5):
                self.type_empty = "watersidecornerA"
            elif ((x,y)==(36,i) and 5<i<9):
                self.type_empty = "watersideunder"

            #line behind the second river
            elif ((x,y)==(i+24,i) and 8<i<16) or ((x,y)==(i+27,i) and i<6):
                self.type_empty = "watersideleftD"
            elif ((x,y)==(i+25,i) and 8<i<15) or ((x,y)==(i+28,i) and i<6):
                self.type_empty = "watersideleftW"
            elif ((x,y)==(33,i) and 5<i<9):
                self.type_empty = "watersideupper"
            
            #full water in the second river
            elif ((x,y)==(i+26,i) and 7<i<14) or ((x,y)==(i+27,i) and 6<i<9) or ((x,y)==(i+28,i) and 5<i<9) or ((x,y)==(i+29,i) and i<7):
                self.type_empty = "water"
            

        #select the sprites randomly
        if (self.type_empty == "rock") or (self.type_empty == "tree") or (self.type_empty == "dirt"):
            aleatoire = randint(1,4)
        else :
            aleatoire = randint(1,2)

        self.sprite = pygame.image.load("game_screen/game_screen_sprites/" + self.type_empty + "_" + str(aleatoire) + ".png")

        self.display()
        self.grid()

    def clear(self):
        if self.type_of_void == "tree":
            self.type_of_void = "dirt"
            # draw function


class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x, y, my_current_map, my_type_of_building, my_state):
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
