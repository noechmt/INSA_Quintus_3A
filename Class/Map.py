import numpy as np
import math as m

from Class.Cell import *


class Map:  # Un ensemble de cellule
    def __init__(self, size, height, width, screen):
        self.size = size  # La taille de la map est size*size : int
        self.height_land = height
        self.width_land = width
        self.screen = screen
        self.array = [[Empty(j, i, self.height_land, self.width_land, self.screen, self) for i in range(
            size)] for j in range(size)]  # tableau de cellule (voir classe cellule) : list
        self.walkers = []
        self.spawn_cell = self.array[0][0]
        self.init_path()
        self.wallet = 3000
        self.update_hover = 0
        self.grided = False
        self.housed = False

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

    def update(self):
        for i in self.walkers:
            i.move()

    def set_cell_array(self, x, y, cell):
        self.array[x][y] = cell
        self.array[x][y].display()

    def get_cell(self, x, y):
        return self.array[x][y]

    def handle_hovered_cell(self, pos):
        # Goal of using update_hover :
        # Pygame uses almost all of the ressources with the graphics
        # And updating the hovering case doesn't need to be at 60 per seconds
        # Only 3, 5, or maybe even is engough
        # It uses way less ressources and doesn't have a visual effect
        self.update_hover += 1
        if (self.update_hover == 10):
            self.update_hover = 0
            for x in range(self.size):
                for y in range(self.size):
                    if(self.get_housed()):
                       self.get_cell(x, y).handle_hover_button_house(pos)
                    else:
                        self.get_cell(x, y).handle_hover_button(pos)

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell)
              for i in range(self.size)] for j in range(self.size)]))

    def dispay_map(self):
        print("Ceci est une map :)")

    def set_grided(self, g):
        self.grided = g

    def get_grided(self):
        return self.grided

    def grid_map(self):
        self.grided = not self.grided
        if self.grided:
            for x in range(40):
                for y in range(40):
                    self.array[x][y].grid()
        else:
            for x in range(40):
                for y in range(40):
                    self.array[x][y].display()
        
    def house_mod(self):
        self.housed = not self.housed

    def get_housed(self):
        return self.housed
    
    def set_housed(self, g):
        self.housed = g


