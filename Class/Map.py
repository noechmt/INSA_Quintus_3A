import numpy as np
import math as m

from Class.Cell import *

class Map:#Un ensemble de cellule
    def __init__(self, size):
        self.size = size #La taille de la map est size*size : int
        self.array = np.zeros((size, size), dtype=Empty) #tableau de cellule (voir classe cellule) : list
        self.walker_list = []
        self.update_hover = 0

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche 
    
    def set_cell_array(self, x, y, cell):
        self.array[x][y] = cell
    
    def get_cell(self, x, y):
        return self.array[x][y]
    
    def handle_hovered_cell(self, pos):
        # Goal of using update_hover :
        # Pygame uses almost all of the ressources with the graphics
        # And updating the hovering case doesn't need to be at 60 per seconds
        # Only 3, 5, or maybe even is engough
        # It uses way less ressources and doesn't have a visual effect
        self.update_hover += 1
        if (self.update_hover == 20):
            self.update_hover = 0
            for x in range(self.size):
                    for y in range(self.size):
                        self.get_cell(x, y).handle_hover_button(pos)

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell) for i in range(self.size)] for j in range(self.size)]))
    
    def dispay_map(self):
        print("Ceci est une map :)")

    



