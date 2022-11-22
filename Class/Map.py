import numpy as np
import math as m

from Cell import *

class Map:#Un ensemble de cellule
    def __init__(self, size):
        self.size = size #La taille de la map est size*size : int
        self.array = [[Void(j,i, self) for i in range (size)] for j in range(size)] #tableau de cellule (voir classe cellule) : list
        self.walker_list = []

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche 

    def display(self):
        print(np.array([[(self.array[i][j].type_of_cell) for i in range(self.size)] for j in range(self.size)]))



