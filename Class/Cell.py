from Class.Walker import *
from Class.RiskEvent import *
import pygame
from random import *
import math
import random

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [
                        (x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


class Cell:  # Une case de la map
    def __init__(self, x, y, height, width, screen, map):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.map = map
        self.type = ""
        self.water = False
        self.sprite = ""
        self.aleatoire = 0
        self.screen = screen
        self.hovered = False
        self.type_empty = None
        self.grided = False
        self.house_mode = False
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()

    def isBuildable(self):
        return isinstance(self, Empty) and self.type_empty == "dirt"

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + \
            self.width*self.x/2 - self.width*self.y/2 - self.map.offset_left
        self.top = self.HEIGHT_SCREEN/6 + self.x * \
            self.height/2 + self.y * self.height/2 + self.map.offset_top

    def display(self):
        if self.type_empty  == "tree":
            if self.aleatoire == 1:
                self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*42/30)), (self.left, self.top-self.height*12/30))
            elif self.aleatoire == 2:
                self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*41/30)), (self.left, self.top-self.height*11/30))
            elif self.aleatoire == 3:
                self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*44/30)), (self.left, self.top-self.height*14/30))
            elif self.aleatoire == 4:
                self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*45/30)), (self.left, self.top-self.height*15/30))
        elif self.type_empty == "rock":
            self.screen.blit(pygame.transform.scale(self.sprite,(self.width, self.height*35/30)), (self.left, self.top-self.height*5/30))
        

        if(self.type == "well"):
            self.screen.blit(pygame.transform.scale(
            self.sprite, (self.width, self.height*53/30)), (self.left, self.top - self.height*23/30))
        elif(self.type == "engineer post"):
            self.screen.blit(pygame.transform.scale(
            self.sprite, (self.width, self.height*50/30)), (self.left, self.top - self.height*20/30))
        elif(self.type == "prefecture"):
            self.screen.blit(pygame.transform.scale(
            self.sprite, (self.width, self.height*38/30)), (self.left, self.top - self.height*8/30))
        else:
            self.screen.blit(pygame.transform.scale(
                self.sprite, (self.width, self.height)), (self.left, self.top))
        if self.map.grided:
            self.grid()

    def display_water(self):
        draw_polygon_alpha(self.screen, (0, 0, 255, 85),
                                   self.get_points_polygone())

    def display_around(self):
        if (self.y+1<40 and (self.map.get_cell(self.x,self.y+1).type_empty != "dirt") and self.map.get_cell(self.x,self.y+1).type != "path"):
            if(self.map.get_cell(self.x,self.y+1).type_empty != "water"):
                self.map.get_cell(self.x,self.y+1).display()
                if(self.map.get_cell(self.x,self.y+1).get_water() and self.map.get_welled() and self.map.get_cell(self.x,self.y+1).type != "well"):
                    self.map.get_cell(self.x,self.y+1).display_water()
                self.map.get_cell(self.x,self.y+1).display_around()
        if (self.x+1<40 and self.map.get_cell(self.x+1, self.y).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y).type != "path"):
            if(self.map.get_cell(self.x+1,self.y).type_empty != "water"):
                self.map.get_cell(self.x+1, self.y).display()
                if(self.map.get_cell(self.x+1, self.y).get_water() and self.map.get_welled() and self.map.get_cell(self.x+1, self.y).type != "well"):
                    self.map.get_cell(self.x+1, self.y).display_water()
                self.map.get_cell(self.x+1, self.y).display_around()
        if (self.x+1<40 and self.y+1<40 and self.map.get_cell(self.x+1, self.y+1).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y+1).type != "path"):
            if(self.map.get_cell(self.x+1,self.y+1).type_empty != "water"):
                self.map.get_cell(self.x+1, self.y+1).display()
                if(self.map.get_cell(self.x+1, self.y+1).get_water() and self.map.get_welled() and self.map.get_cell(self.x+1, self.y+1).type != "well"):
                    self.map.get_cell(self.x+1, self.y+1).display_water()
                self.map.get_cell(self.x+1, self.y+1).display_around()

    def handle_zoom(self, zoom_in):
        if zoom_in:
            self.height *= 1.04
            self.width *= 1.04
        else:
            self.height /= 1.04
            self.width /= 1.04
        self.init_screen_coordonates()
        self.display()

    def handle_move(self, move, m):
        if move == "up":
            self.top += 15 * m
        if move == "down":
            self.top -= 15 * m
        if move == "right":
            self.left -= 15 * m
        if move == "left":
            self.left += 15 * m
        # self.display()

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

    def handle_hover_button(self):
        #is_hovered = self.is_hovered(pos)
        # if is_hovered and not self.hovered:
        #self.hovered = True
        if (self.map.get_housed()):
            house_sprite = pygame.image.load(
                    "game_screen/game_screen_sprites/house_0.png")
            self.screen.blit(pygame.transform.scale(
                    house_sprite, (self.width, self.height)), (self.left, self.top))
            if self.isBuildable():
                draw_polygon_alpha(self.screen, (0, 0, 0, 85),
                                   self.get_points_polygone())
            else:
                draw_polygon_alpha(self.screen, (255, 0, 0, 85),
                                   self.get_points_polygone())
        elif self.map.get_road_button_activated() and not self.isBuildable():
            draw_polygon_alpha(self.screen, (255, 0, 0, 85),
                               self.get_points_polygone())
        else:
            draw_polygon_alpha(self.screen, (0, 0, 0, 85),
                               self.get_points_polygone())
        # if not is_hovered and self.hovered:
        #     self.hovered = False
        #     self.display()
        #     self.grid()

    # def handle_click_cell(self, pos):
    #     if self.is_hovered(pos) and isinstance(self, Empty) and self.map.road_button_activated:
    #         self.map.set_cell_array(self.x, self.y, Path(self.x, self.y,
    #                                                      self.height, self.width, self.screen, self.map))
    #         self.map.get_cell(self.x, self.y).handle_sprites()

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

    def set_aleatoire(self, ent):
        self.aleatoire = ent

    def get_aleatoire(self):
        return self.aleatoire

    # Return an cell array which match with the class type (ex: Path, Prefecture (not a string)) in argument
    def check_cell_around(self, type):
        path = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j) and self.map.inMap(self.x + i, self.y + j):
                    if isinstance(self.map.get_cell(self.x + i, self.y + j), type):
                        path.append(self.map.get_cell(self.x + i, self.y + j))
        return path

    def build(self, type):
        if isinstance(self, Empty) and self.type_empty != "dirt":
            print("This cell is already taken")
        else:
            match type:
                case "path":
                    self.map.set_cell_array(self.x, self.y, Path(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.get_cell(self.x, self.y).handle_sprites()
                    self.map.get_cell(self.x, self.y).display()
                    self.map.wallet -= 4
                case "house":
                    self.map.set_cell_array(self.x, self.y, House(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 10
                case "well":
                    self.map.set_cell_array(self.x, self.y, Well(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.set_cell_array(self.x, self.y, Prefecture(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.set_cell_array(self.x, self.y, EngineerPost(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if(37>self.x>3 and 37>self.y>3 and self.map.get_cell(self.x+i, self.y+j).type == "well"):
                        self.map.get_cell(self.x,self.y).set_water(True)

    def grid(self):
        if self.map.get_grided():
            pygame.draw.polygon(self.screen, (25, 25, 25),
                                self.get_points_polygone(), 2)
        else:
            self.display()

    def clear(self):
        if not isinstance(self, Empty) and self.type_empty != "rock" and self.type_empty != "water":
            self.type_empty = "dirt"
            self.map.set_cell_array(self.x, self.y, Empty(
                self.x, self.y, self.height, self.width, self.screen, self.map))
            self.map.wallet -= 2

    def set_type(self, type):
        self.type = type

    def set_water(self, bool):
        self.water = bool

    def get_water(self):
        return self.water


sprite_hori = pygame.image.load(
    "game_screen/game_screen_sprites/road_straight_hori.png")
sprite_verti = pygame.image.load(
    "game_screen/game_screen_sprites/road_straight_verti.png")
sprite_all_turn = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_all.png")
sprite_turn_bot_left = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_bot_left.png")
sprite_turn_bot_right = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_bot_right.png")
sprite_turn_hori_bot = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_hori_bot.png")
sprite_turn_hori_top = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_hori_top.png")
sprite_turn_left_top = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_left_top.png")
sprite_turn_right_top = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_right_top.png")
sprite_turn_verti_left = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_verti_left.png")
sprite_turn_verti_right = pygame.image.load(
    "game_screen/game_screen_sprites/road_turn_verti_right.png")


class Path(Cell):
    def __init__(self, x, y, height, width, screen, map, path_level=0):
        super().__init__(x, y, height, width, screen, map)
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/road_straight_verti.png")
        self.level = path_level
        self.handle_sprites()
        self.display()
        self.grid()
        self.type = "path"

    def handle_sprites(self, r=0):
        if r < 2:
            # Check if the road is in all turns
            if self.check_surrondings([1, 1, 1, 1]):
                self.set_sprite(sprite_all_turn)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()
                return
            # Check if the road is a turn bottom to left
            if self.check_surrondings([1, 0, 1, 0]):
                self.set_sprite(sprite_turn_bot_left)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()
                return
            # Check if the road is a turn bottom to right
            if self.check_surrondings([0, 0, 1, 1]):
                self.set_sprite(sprite_turn_bot_right)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()
                return
            # Check if the road is a turn horizontal to bottom
            if self.check_surrondings([1, 0, 1, 1]):
                self.set_sprite(sprite_turn_hori_bot)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()

                return
            # Check if the road is a turn horizontal to top
            if self.check_surrondings([1, 1, 0, 1]):
                self.set_sprite(sprite_turn_hori_top)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.grid()

                return
            # Check if the road is a turn letf to top
            if self.check_surrondings([1, 1, 0, 0]):
                self.set_sprite(sprite_turn_left_top)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.grid()
                return
            # Check if the road is a turn right to top
            if self.check_surrondings([0, 1, 0, 1]):
                self.set_sprite(sprite_turn_right_top)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.grid()

                return
            # Check if the road is a turn vertical to left
            if self.check_surrondings([1, 1, 1, 0]):
                self.set_sprite(sprite_turn_verti_left)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()

                return
            # Check if the road is a turn vertical to right
            if self.check_surrondings([0, 1, 1, 1]):
                self.set_sprite(sprite_turn_verti_right)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()

                return

            # Check horizontal road
            if self.check_surrondings([2, 0, 0, 1]):
                self.set_sprite(sprite_hori)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x - 1, self.y), Path):
                    self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.grid()
                return
            if self.check_surrondings([1, 0, 0, 2]):
                self.set_sprite(sprite_hori)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x + 1, self.y), Path):
                    self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.grid()
                return
            # Check vertical road
            if self.check_surrondings([0, 2, 1, 0]):
                self.set_sprite(sprite_verti)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x, self.y - 1), Path):
                    self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.grid()
                return
            if self.check_surrondings([0, 1, 2, 0]):
                self.set_sprite(sprite_verti)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x, self.y + 1), Path):
                    self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                self.grid()
                return

    def check_surrondings(self, check):
        i = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if abs(dx) != abs(dy):
                    if check[i] != 2 and isinstance(self.map.get_cell(self.x + dx, self.y + dy), Path) != check[i]:
                        return False
                    i += 1
        return True

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.display()

    def __str__(self):
        return f"Chemin { self.level}"


class Empty(Cell):
    def __init__(self, x, y, height, width, screen, map, type_empty="dirt"):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty #"dirt", "trees"
        self.type = "empty"
        tree_or_dirt_list = ["tree", "dirt", "dirt"]
        rock_or_dirt_list = ["rock", "dirt", "dirt", "dirt"]
        
        #place the trees
        for i in range (40):
            for j in range (40):
                if (x,y)==(i,j):
                    self.type_empty = random.choice(tree_or_dirt_list)
                    if self.type_empty == "tree":
                        self.type_sprite = "tree"
                        self.type = "empty_tree"
                    else:
                        self.type_sprite = "dirt"
                
        #place the rocks
        for i in range (40):
            for j in range (40):
                
                if (x,y)==(i,j) and ((27<i<36 and 12<j<16) or (27<i<31 and 15<j<23) or (i>30 and j>25) or (i>35 and j<5) or (i>35 and j>30)):
                    self.type_empty = random.choice(rock_or_dirt_list)
                    if self.type_empty == "rock":
                        self.type_sprite = "rock"
                        self.type = "empty_rock"
                    else:
                        self.type_sprite = "dirt"



    #place the water with conditions for sprites
        #river at the top
        for i in range (40):
            
            #line under the first river  
            if ((x,y) == (i,i+10) and i<5) or ((x,y)==(i,i+14) and 5<i<8) or ((x,y)==(i,i+15) and 8<i<13) or ((x,y)==(i,i+18) and 14<i<17) or ((x,y)==(i,i+20) and 17<i<20):
                self.type_sprite = "watersiderightD"
                self.type_empty = "water"
            elif ((x,y) == (i,i+11) and i<5) or ((x,y)==(i,i+15) and 4<i<8) or ((x,y)==(i,i+16) and (7<i<13)) or (x,y)==(13,31) or ((x,y)==(i,i+19) and 13<i<17) or ((x,y)==(i,i+21) and 16<i<19):
                self.type_sprite = "watersiderightW"
                self.type_empty = "water"
            elif (x,y) == (5,15) or (x,y) == (8,22) or (x,y)==(13,28) or (x,y)==(14,31) or (x,y)==(17,35):
                self.type_sprite = "watersidecornerA"
                self.type_empty = "water"
            elif ((x,y) == (5, i) and 15<i<20) or (x,y)==(8,23) or (x,y)==(13,29) or (x,y)==(13,30) or (x,y)==(14,32) or (x,y)==(17,36) or (x,y)==(17,37):
                self.type_sprite = "watersideunder"
                self.type_empty = "water"
            
            #line behind the first river
            elif ((x,y) == (i,i+19) and i<10) or ((x,y)==(i,i+26) and 9<i<14):
                self.type_sprite = "watersideleftW"
                self.type_empty = "water"
            elif ((x,y) == (i, i+20) and i<9) or ((x,y)==(i,i+27) and 8<i<13):
                self.type_sprite = "watersideleftD"
                self.type_empty = "water"
            elif ((x,y)==(9,i) and 28<i<36):
                self.type_sprite = "watersideupper"
                self.type_empty = "water"

            elif ((x,y)==(i+31,i) and i<5) or ((x,y)==(i+28,i) and 8<i<12):
                self.type_sprite = "watersiderightD"
                self.type_empty = "water"
            elif ((x,y)==(i+30,i) and i<6) or ((x,y)==(i+27,i) and 8<i<13):
                self.type_sprite = "watersiderightW"
                self.type_empty = "water"
            elif (x,y)==(36,5):
                self.type_sprite = "watersidecornerA"
                self.type_empty = "water"
            elif ((x,y)==(36,i) and 5<i<9):
                self.type_sprite = "watersideunder"
                self.type_empty = "water"

            #line behind the second river
            elif ((x,y)==(i+24,i) and 8<i<16) or ((x,y)==(i+27,i) and i<6):
                self.type_sprite = "watersideleftD"
                self.type_empty = "water"
            elif ((x,y)==(i+25,i) and 8<i<15) or ((x,y)==(i+28,i) and i<6):
                self.type_sprite = "watersideleftW"
                self.type_empty = "water"
            elif ((x,y)==(33,i) and 5<i<9):
                self.type_sprite = "watersideupper"
                self.type_empty = "water"
            
            #full water in the second river
            elif ((x,y)==(i+26,i) and 7<i<14) or ((x,y)==(i+27,i) and 6<i<9) or ((x,y)==(i+28,i) and 5<i<9) or ((x,y)==(i+29,i) and i<7):
                self.type_sprite = "water"
                self.type_empty = "water"
        
            #full water in the first river
            for j in range (40):
                if (x,y)==(i,j) and ((i<5 and 11+i<j<19+i) or (4<i<8 and 15+i<j<19+i) or (7<i<10 and 16+i<j<19+i) or (9<i<13 and 16+i<j<26+i) 
                    or (i==13 and 18+i<j<26+i) or (13<i<17 and 19+i<j<26+i) or (i==17 and j==39)):
                    self.type_sprite = "water"
                    self.type_empty = "water"

        
        #river at the bottom
           
            

        #select the sprites randomly
        if (self.type_empty == "rock") or (self.type_empty == "tree"):
            aleatoire = randint(1,4)
        elif (self.type_empty == "dirt"):
            aleatoire = randint(1, 13)
        else :
            aleatoire = randint(1,2)
        super().set_aleatoire(aleatoire)
        self.sprite = pygame.image.load("game_screen/game_screen_sprites/" + self.type_sprite + "_" + str(aleatoire) + ".png")

        self.display()

    def __str__(self):
        return self.type_empty

    def clear(self):
        if self.type_empty == "tree":
            self.type_empty = "dirt"
            self.map.wallet -= 2

    def canBuild(self):
        return self.type_empty == "dirt"


class Building(Cell):  # un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.map.buildings.append(self)
        self.destroyed = False


    def destroy(self):
        self.destroyed = True


class House(Building):  # la maison fils de building (?)
    def __init__(self, x, y, height, width, screen, my_map, level=0, nb_occupants=0):
        super().__init__(x, y, height, width, screen, my_map)
        self.level = level  # niveau de la maison : int
        self.nb_occupants = nb_occupants  # nombre d'occupants: int
        # nombre max d'occupant (dépend du niveau de la maison) : int
        self.max_occupants = 5
        self.unemployedCount = 0
        self.migrant = Migrant(self)
        self.risk = RiskEvent("fire", self)
        # Temporary
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/house_" + str(self.level) + ".png")
        self.type = "house"
        self.display()

    def __str__(self):
        return f"House { self.level}"

    def nextLevel(self):
        self.level += 1
        match self.level:
            case 1:
                self.max_occupants = 7
            case 2:
                self.max_occupants = 9


class Well(Building):
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        #le risque est la en stand by
        self.risk = RiskEvent("collapse", self)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (37>self.x>3, 37>self.y>3):
                    self.map.get_cell(self.x+i, self.y+j).water = True
                    checkedCell = self.map.get_cell(self.x+i, self.y+i)
                    if isinstance(checkedCell, House) and checkedCell.level == 1 and checkedCell.max_occupants == checkedCell.nb_occupants:
                        checkedCell.nextLevel

        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/well.png")
        self.type = "well"

    def __str__(self):
        return "Puit"


class Prefecture(Building):
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.prefect = Prefect(self)
        self.requiredEmployees = 5
        self.risk = RiskEvent("collapse", self)
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/prefecture.png")
        self.type="prefecture"

    def __str__(self):
        return f"Prefecture { self.employees}"

    def patrol(self):
        self.prefect.leave_building()


class EngineerPost(Building):
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.engineer = Engineer(self)
        self.requiredEmployees = 5
        self.risk = RiskEvent("fire", self)
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/engineerpost.png")
        self.type="engineer post"

    def __str__(self):
        return "Engineer Post"

    def patrol(self):
        self.engineer.leave_building()
