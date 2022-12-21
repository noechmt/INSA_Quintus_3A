from Class.Walker import *
from Class.RiskEvent import *
import pygame

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
        self.grided = False
        self.house_mode = False
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + self.width*self.x/2 - self.width*self.y/2
        self.top = self.HEIGHT_SCREEN/6 + self.x * self.height/2 + self.y * self.height/2

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
        if isinstance(self, Empty) and self.type != "dirt":
            print("This cell is already taken")
        else:
            match type:
                case "path":
                    self.map.setCell(self, Path(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 4 
                case "house":
                    self.map.setCell(self, House(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 10
                case "well":
                    self.map.setCell(self, Well(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.setCell(self, Prefecture(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.setCell(self, EngineerPost(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30

    def grid(self):
        if self.map.get_grided() :
            pygame.draw.polygon(self.screen, (25,25,25), self.get_points_polygone(), 2)
        else : 
            self.display()
    
    def clear(self):
        if not (isinstance(self, Empty) and (self.type_empty == "rock" or self.type_empty == "water")):
            self.type_empty = "dirt" 
            self.map.wallet -= 2

class Path(Cell):
    def __init__(self, x, y, height, width, screen, my_map, my_path_level=0):
        super().__init__(x, y, height, width, screen, my_map)
        self.level = my_path_level

    def __str__(self):
        return f"Chemin { self.level}"

class Empty(Cell):
    def __init__(self, x, y, height, width, screen, map, type_empty="dirt"):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty #"dirt", "trees", "water", #"rocks"
        self.sprite = pygame.image.load("game_screen/game_screen_sprites/" + self.type_empty + "_" + str(1) + ".png")
        self.display()
        
    def __str__(self):
        return self.type_empty

    def canBuild(self) : 
        return self.type_empty == "dirt"  


class Building(Cell) : #un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x,y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.state = "build" #état (détruit ou pas) 

    def destroy(self) : 
        self.state = "destroyed"
                     
class House(Building) : #la maison fils de building (?)
    def __init__(self, x, y, height, width, screen, my_map, level=0, nb_occupants=0) :
        super().__init__(x, y, height, width, screen, my_map)
        self.level = level #niveau de la maison : int
        self.nb_occupants = nb_occupants #nombre d'occupants: int
        self.max_occupants = 5 #nombre max d'occupant (dépend du niveau de la maison) : int
        self.unemployedCount = 0
        self.migrant = Migrant(self)
        self.fire = RiskEvent("fire")

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
    def __init__(self, x, y, height, width, screen, my_map): 
        super().__init__(x, y, height, width, screen, my_map)
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
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.prefect = Prefect(self)
        self.requiredEmployees = 5
        self.risk = RiskEvent("fire")

    def __str__(self):
        return f"Prefecture { self.employees}"

    def patrol(self):
        self.prefect.leave_building()

class EngineerPost(Building):
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.requiredEmployees = 5
        self.risk = RiskEvent("collapse")

    def __str__(self):
        return "Engineer Post"

