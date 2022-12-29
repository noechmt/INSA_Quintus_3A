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
        # self.buildingAlive = True
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

        if self.riskCounter >= 50 :
            self.happened = True

    def ignite(self) :
        if not self.happened :
            return 
        if self.fireCounter >= 500 : 
            self.building.screen.blit(pygame.transform.scale(pygame.image.load("game_screen/game_screen_sprites/dirt_0.png"), (self.building.width, self.building.height)), (self.building.left, self.building.top))
            self.building.screen.blit(pygame.transform.scale(self.fire_sprites[8], (self.building.width, self.building.height)), (self.building.left, self.building.top))
        else : 
            # arr = self.building.check_cell_around(Cell.Cell)
            # for i in arr :
            #     i.display()
            self.building.screen.blit(pygame.transform.scale(self.fire_sprites[self.fireCounter%8], (self.building.width, self.building.height)), (self.building.left, self.building.top))
            self.fireCounter += 1

        


    def resetEvent(self) :
        self.riskCounter = 0

    
         


     