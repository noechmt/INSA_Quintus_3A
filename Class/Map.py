import numpy as np
import math as m

from Cell import *

class Map:#Un ensemble de cellule
    def __init__(self, size):
        self.size = size #La taille de la map est size*size : int
        self.array = [[Empty(j,i, self) for i in range (size)] for j in range(size)] #tableau de cellule (voir classe cellule) : list
        self.walkers = []
        self.spawn_cell = self.array[0][0]
        self.init_path()
        self.wallet = 3000

    def init_path(self) : #Permet d'initialiser le chemin de terre sur la map. 
        for i in range(self.size) :
            self.array[self.size-m.floor(self.size/4)][i] = Path(self.size-m.floor(self.size/4), i, self) #On modifie la valeur des cellules pour représenter le chemin dans la matrice
            #Pour aucune raison, le chemin est initialisé à 1/4 sur l'axe des y(vers le haut) de la map en partant de la gauche

    def __str__(self):
        s=f"Map {self.size}*{self.size}\n"
        for j in range( self.size):
            for i in range(self.size):
                
                for k in self.walkers:
                    if k.currentCell == self.getCell(i,j):
                        s += f"{(str(self.getCell(i,j)) + ' ' + str(k)):^20}"
                        break
                else:
                    s += f"{str(self.getCell(i,j)):^20}"
            s += "\n"
        return s
        
    def update(self):
        (i.move() for i in self.walkers)

    def getCell(self, x, y):
        return self.array[x][y]

    def setCell(self, prev_cell, new_cell):
        self.array[prev_cell.x][prev_cell.y] = new_cell


