from Class.Walker import *
from Class.RiskEvent import *
import pygame
from random import *
import math


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
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/house_" + str(0) + ".png")
        self.screen = screen
        self.hovered = False
        self.grided = False
        self.house_mode = False
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = self.screen.get_size()
        self.init_screen_coordonates()

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + \
            self.width*self.x/2 - self.width*self.y/2
        self.top = self.HEIGHT_SCREEN/6 + self.x * \
            self.height/2 + self.y * self.height/2

    def display(self):
        self.screen.blit(pygame.transform.scale(
            self.sprite, (self.width, self.height)), (self.left, self.top))

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
        self.display()

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
            if(self.map.get_housed()):
                house_sprite = pygame.image.load("game_screen/game_screen_sprites/house_0.png")
                self.screen.blit(pygame.transform.scale(house_sprite, (self.width, self.height)), (self.left, self.top))
            draw_polygon_alpha(self.screen, (0, 0, 0, 85),
                               self.get_points_polygone())
        if not is_hovered and self.hovered:
            self.hovered = False
            self.display()
            self.grid()

    def handle_click_cell(self, pos):
        if self.is_hovered(pos) and isinstance(self, Empty) and self.map.road_button_activated:
            self.map.set_cell_array(self.x, self.y, Path(self.x, self.y,
                                                         self.height, self.width, self.screen, self.map))
            self.map.get_cell(self.x, self.y).handle_sprites()

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

    # Check if these coordinates are in the map
    def inMap(self, x, y):
        return (0 <= x and x <= self.map.size-1 and 0 <= y and y <= self.map.size-1)

    # Return an cell array which match with the class type (ex: Path, Prefecture (not a string)) in argument
    def check_cell_around(self, type):
        path = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j) and self.inMap(self.x + i, self.y + j):
                    if isinstance(self.map.get_cell(self.x + i, self.y + j), type):
                        path.append(self.map.get_cell(self.x + i, self.y + j))
        return path

    def build(self, type):
        if isinstance(self, Empty) and self.type != "dirt":
            print("This cell is already taken")
        else:
            match type:
                case "path":
                    self.map.set_cell_array(self, self.x, self.y, Path(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 4
                case "house":
                    self.map.set_cell_array(self.x, self.y, House(self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 10
                case "well":
                    self.map.set_cell_array(self.x, self.y,Well(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.set_cell_array(self.x, self.y,Prefecture(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.set_cell_array(self.x, self.y,EngineerPost(
                        self.x, self.y, self.height, self.width, self.screen, self.map))
                    self.map.wallet -= 30

    def grid(self):
        if self.map.get_grided():
            pygame.draw.polygon(self.screen, (25, 25, 25),
                                self.get_points_polygone(), 2)
        else:
            self.display()

    def set_type(self, type):
        self.type = type


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
        self.display()
        self.grid()

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
        self.type_empty = type_empty  # "dirt", "trees", "water", #"rocks"
        super().set_type(self.type_empty)
        self.n_rand = randint(0, 15)
        self.sprite = pygame.image.load(
            "game_screen/game_screen_sprites/" + self.type_empty + "_" + str(self.n_rand) + ".png")
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
        self.state = "build"  # état (détruit ou pas)

    def destroy(self):
        self.state = "destroyed"


class House(Building):  # la maison fils de building (?)
    def __init__(self, x, y, height, width, screen, my_map, level=0, nb_occupants=0):
        super().__init__(x, y, height, width, screen, my_map)
        self.level = level  # niveau de la maison : int
        self.nb_occupants = nb_occupants  # nombre d'occupants: int
        # nombre max d'occupant (dépend du niveau de la maison) : int
        self.max_occupants = 5
        self.unemployedCount = 0
        self.migrant = Migrant(self)
        self.fire = RiskEvent("fire")

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
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.inMap(self.x+i, self.y+j):
                    self.map.get_cell(self.x+i, self.y+j).water = True
                    checkedCell = self.map.get_cell(self.x+i, self.y+i)
                    if isinstance(checkedCell, House) and checkedCell.level == 1 and checkedCell.max_occupants == checkedCell.nb_occupants:
                        checkedCell.nextLevel

    def __str__(self):
        return "Puit"


class Prefecture(Building):
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        #self.labor_advisor = LaborAdvisor(self)
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
