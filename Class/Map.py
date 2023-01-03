import numpy as np
import math as m
import random as rd
import networkx as nx

from Class.Cell import *


class Map:  # Un ensemble de cellule
    def __init__(self, size, height, width, screen):
        self.size = size  # La taille de la map est size*size : int
        self.height_land = height
        self.width_land = width
        self.offset_top = 0
        self.offset_left = 0
        self.screen = screen
        self.grided = False
        self.array = [[Empty(j, i, self.height_land, self.width_land, self.screen, self) for i in range(
            size)] for j in range(size)]  # tableau de cellule (voir classe cellule) : list
        self.walkers = []
        self.migrantQueue = []
        self.laborAdvisorQueue = []
        self.buildings = []
        self.path_graph = nx.DiGraph()
        self.spawn_cell = self.array[39][19]
        self.init_path()
        self.wallet = 3000
        self.update_hover = 0
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = False
        self.zoom = 1

    def init_path(self):  # Permet d'initialiser le chemin de terre sur la map.
        for i in range(self.size):
            # On modifie la valeur des cellules pour représenter le chemin dans la matrice
            self.array[self.size-m.floor(self.size/3)][i] = Path(self.size-m.floor(
                self.size/3), i, self.height_land, self.width_land, self.screen, self)

    def __str__(self):
        s = f"Map {self.size}*{self.size}\n"
        for j in range(self.size):
            for i in range(self.size):

                for k in self.walkers:
                    if k.currentCell == self.getCell(i, j):
                        s += f"{(str(self.getCell(i,j)) + ' ' + str(k)):^20}"
                        break
                else:
                    s += f"{str(self.getCell(i,j)):^20}"
            s += "\n"
        return s


    def handle_road_button(self):
        self.road_button_activated = True
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = False

    def handle_house_button(self):
        self.road_button_activated = False
        self.house_button_activated = True
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = False

    def handle_shovel_button(self):
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = True
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = False

    def handle_prefecture_button(self):
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = True
        self.engineerpost_button_activated = False
        self.well_button_activated = False

    def handle_engineerpost_button(self):
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = True
        self.well_button_activated = False

    def handle_well_button(self):
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = True

    def handle_esc(self):
        self.road_button_activated = False
        self.house_button_activated = False
        self.shovel_button_activated = False
        self.prefecture_button_activated = False
        self.engineerpost_button_activated = False
        self.well_button_activated = False

    def handle_zoom(self, zoom_in):
        self.screen.fill((0, 0, 0))
        #self.offset_left, self.offset_top = (0, 0)
        if zoom_in:
            self.height_land *= 1.04
            self.width_land *= 1.04
        else:
            self.height_land /= 1.04
            self.width_land /= 1.04
        for x in range(40):
            for y in range(40):
                self.get_cell(x, y).handle_zoom(zoom_in)
        self.display_grid(0)

    def handle_move(self, move, m):
        self.screen.fill((0, 0, 0))
        for x in range(40):
            for y in range(40):
                self.get_cell(x, y).handle_move(move, m)
                self.get_cell(x, y).display()
        self.display_grid(0)

    # Check if these coordinates are in the map
    def inMap(self, x, y):
        return (0 <= x and x <= self.size-1 and 0 <= y and y <= self.size-1)

    def update_walkers(self):

        waitfornext = False
        if len(self.migrantQueue) != 0:
            for i in self.migrantQueue :
                if i.spawnCount%60 == randint(0,59): i.path_finding(i.currentCell, i.building)
                if len(i.path) != 0 and ((rd.randint(0, 9) == 9 and not waitfornext) or i.spawnCount == 20):
                    self.walkers.append(i)
                    self.migrantQueue.remove(i)
                    i.screen.blit(pygame.transform.scale(i.walker_sprites["top"], 
                    (i.currentCell.width, i.currentCell.height)), (i.currentCell.left, i.currentCell.top))
                    waitfornext = True
                elif i.spawnCount == 100:
                    i.building.clear()
                else : i.spawnCount += 1   


        if len(self.laborAdvisorQueue) != 0 :
            for i in self.laborAdvisorQueue : 
                if any(house.nb_occupants != 0 for house in self.buildings if isinstance(house, House)): i.leave_building()

        for i in self.walkers:
            i.move()
            i.display()
            i.currentCell.display_around()
            if not isinstance(i, Migrant):
                i.previousCell.display()
                i.previousCell.display_around()


        for i in self.buildings :
            if not i.risk.happened : i.risk.riskIncrease()

    def update_fire(self) : 
        for i in self.buildings :
            if i.risk.happened and i.risk.type == "fire":
                i.risk.burn()

    def update_collapse(self) : 
        for i in self.buildings : 
            if i.risk.happened and i.risk.type == "collapse" : 
                i.risk.collapse()



    def set_cell_array(self, x, y, cell):
        self.array[x][y] = cell
        self.array[x][y].display()

    def get_cell(self, x, y):
        if (x < 0 or x >= 40) or (y < 0 or y >= 40):
            return None
        return self.array[x][y]

    # def handle_hovered_cell(self, pos):
    #     # Goal of using update_hover :
    #     # Pygame uses almost all of the ressources with the graphics
    #     # And updating the hovering case doesn't need to be at 60 per seconds
    #     # Only 3, 5, or maybe even is engough
    #     # It uses way less ressources and doesn't have a visual effect
    #     self.update_hover += 1
    #     if (self.update_hover == 10):
    #         self.update_hover = 0
    #         for x in range(self.size):
    #             for y in range(self.size):
    #                 self.get_cell(x, y).handle_hover_button(pos)

    def handle_click_cells(self, pos):
        for x in range(self.size):
            for y in range(self.size):
                self.get_cell(x, y).handle_click_cell(pos)

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell)
              for i in range(self.size)] for j in range(self.size)]))

    def display_map(self):
        for i in range(40):
            for j in range(40):
                self.array[i][j].display()

    def set_grided(self, g):
        self.grided = g

    def get_grided(self):
        return self.grided

    def grid_map(self):
        self.grided = not self.grided
        self.display_grid()

    def display_grid(self, pushed=1):
        if self.grided:
            for x in range(40):
                for y in range(40):
                    self.array[x][y].grid()
        elif pushed:
            for x in range(40):
                for y in range(40):
                    self.array[x][y].display()

    def get_housed(self):
        return self.house_button_activated

    def get_shoveled(self):
        return self.shovel_button_activated

    def get_road_button_activated(self):
        return self.road_button_activated

    def get_prefectured(self):
        return self.prefecture_button_activated

    def get_engineered(self):
        return self.engineerpost_button_activated

    def get_welled(self):
        return self.well_button_activated

    def get_height_land(self):
        return self.height_land

    def get_width_land(self):
        return self.width_land
