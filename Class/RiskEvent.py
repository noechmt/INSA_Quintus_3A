from threading import *
import time
import Class.Cell as Cell
import random as rd
import pygame

class RiskEvent():
    def __init__(self, eType, building) : 
        self.riskCounter = 0
        self.happened = False
        self.type = eType
        self.tmpbool = True
        self.fireCounter = 0
        self.fire_sprites = dict((k, pygame.image.load("risks_sprites/house_fire/fire_" + str(k) + ".png")) for k in range(0,9))
        self.building = building
        

    def riskIncrease(self) :
        if isinstance(self.building, Cell.House) and (self.building.migrant in self.building.map.walkers or self.building.migrant in self.building.map.migrantQueue) :
            return
        if self.type == "fire" :
            self.riskCounter += rd.randint(0,3) 
        else : 
            self.riskCounter += rd.randint(0,1)

        if self.riskCounter >= 200 :
            self.happened = True
            self.building.type = "ruin"
            self.building.sprite = pygame.image.load("risks_sprites/house_fire/fire_8.png")

    def burn(self) :
        if not self.happened :
            return 
        if self.fireCounter >= 500 : 
            self.building.screen.blit(pygame.transform.scale(pygame.image.load("game_screen/game_screen_sprites/dirt_0.png"), (self.building.width, self.building.height)), (self.building.left, self.building.top))
            self.building.screen.blit(pygame.transform.scale(self.fire_sprites[8], (self.building.width, self.building.height)), (self.building.left, self.building.top))
        else : 
            self.building.screen.blit(pygame.transform.scale(self.fire_sprites[self.fireCounter%8], (self.building.width, self.building.height)), (self.building.left, self.building.top))
            self.fireCounter += 1
            arr = self.building.check_cell_around(Cell.Cell)
            for i in arr :
                if not isinstance(i, Cell.Building) : i.display()
                for j in i.check_cell_around(Cell.Cell) :
                    if j.x < self.building.x + 2 and j.y < self.building.y + 2 : 
                        if not isinstance(j, Cell.Building) and not (j in [i.map.array[i.x-1][i.y], i.map.array[i.x - 1][i.y - 1]]) and (isinstance(i, Cell.Prefecture) or isinstance(i, Cell.EngineerPost)): j.display()
            

        if self.fireCounter >= 400 : 
            arr = self.building.check_cell_around(Cell.Building)
            for i in arr :
                i.risk.happened = True
                i.type = "ruin"
                i.sprite = pygame.image.load("risks_sprites/house_fire/fire_8.png")
        


    def resetEvent(self) :
        self.riskCounter = 0

    
         


     