import numpy as np
import math as m

from Class.Cell import *

class Map:#Un ensemble de cellule
    def __init__(self, size, width_cell, height_cell, screen):
        self.size = size #La taille de la map est size*size : int
        self.array = [[Empty(j,i, width_cell,height_cell, screen, self) for i in range (size)] for j in range(size)] #tableau de cellule (voir classe cellule) : list
        self.walker_list = []
        self.grided = False

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche 

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell) for i in range(self.size)] for j in range(self.size)]))
    
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

    



