from Class.Walker import *
import pygame

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

class Cell: #Une case de la map
    def __init__(self, x, y, height, width, screen, map_array):
        self.x = x
        self.y = y 
        self.height = height
        self.width = width
        self.map_array = map_array
        self.water = False
        self.sprite = None
        self.screen = screen
        self.hovered = False
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()
        self.init_trs_coordonates()

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + self.width*self.x/2 - self.width*self.y/2
        self.top = self.HEIGHT_SCREEN/6 + self.x * self.height/2 + self.y * self.height/2
    
    def init_trs_coordonates(self):
        self.t1 = (self.left, self.top)
        self.t2 = (self.left, self.top + self.height)
        self.t3 = (self.left + self.width, self.top + self.height)
        self.t4 = (self.left + self.width, self.top)
        self.t_1 = (self.left + self.width / 2, self.top)
        self.t_2 = (self.left, self.top + self.height / 2)
        self.t_3 = (self.left + self.width / 2, self.top + self.height)
        self.t_4 = (self.left + self.width, self.top + self.height / 2)

    def display(self):
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
                case "house":
                    self.map.array[self.x][self.y] = House(self.x, self.y, self.map)
                case "fountain":
                    self.map.array[self.x][self.y] = Fountain(self.x, self.y, self.map)
                case "prefecture":
                    self.map.array[self.x][self.y] = Prefecture(self.x, self.y, self.map)
                case "engineer post":
                    self.map.array[self.x][self.y] = EngineerPost(self.x, self.y, self.map)

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
        self.type_empty = type_empty #"dirt", "trees", "water", #"rocks"
        self.sprite = pygame.image.load("game_screen/game_screen_sprites/" + self.type_empty + "_" + str(1) + ".png")
        self.display()
        self.grid()

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
