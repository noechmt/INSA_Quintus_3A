import Class.Cell as Cell
import random
import pygame

import networkx as nx

def rm_dup_list(x):
  return list(dict.fromkeys(x))

class Walker() : 
    def __init__(self, job, building, state) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.building = building #string (prefecture, engineer post, house)
        self.currentCell = building #La cellule de départ de l'entity : Cell
        self.previousCell = None
        self.inBuilding = state
        self.path = []
        self.ttl = 50
        self.wait = 0
        print("Walker spawn")
        self.screen = self.currentCell.screen
        self.walker_sprites = {}
        self.alive = False
        self.isWandering = False
        self.currentSprite = 0

    def display(self) :
        if not self.inBuilding :
            if self.previousCell.x < self.currentCell.x :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["right"][self.currentSprite%2], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.x > self.currentCell.x :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["left"][self.currentSprite%2], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.y < self.currentCell.y :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["bot"][self.currentSprite%2], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.y > self.currentCell.y :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["top"][self.currentSprite%2], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            
            self.currentSprite += 1
        # elif self.inBuilding == True :
        #     self.currentCell.display()

    def __str__(self) -> str:
        pass
    def path_finding(self, start, end):
        # Create a graph
        G = nx.Graph()

        # Loop through the map to add edges to the graph
        for l in self.currentCell.map.array:
            for i in l:
                #print(i.x, i.y, type (i))
                #Check if the cell is a path
                if isinstance(i, Cell.Path):
                    #Get an array of all neighbor path
                    cell_around = i.check_cell_around(Cell.Path)
                    #Loop through this array
                    for j in cell_around:
                        #print("Add edge from "+str((i.x, i.y))+" to "+str((j.x, j.y)))
                        G.add_edge(i, j)

                #Check if the cell is a house
                if isinstance(i, Cell.House) or isinstance(i, Cell.EngineerPost) or isinstance(i, Cell.Prefecture):
                    cell_around = i.check_cell_around(Cell.Path)
                    for j in cell_around:
                        #print("Add edge from "+str((i.x, i.y))+" to "+str((j.x, j.y)))
                        G.add_edge(i, j)

        #Calculate with the dijkstra algorithm the shortest path
        print("Path finding to reach", end, "from", start)
        self.path = nx.dijkstra_path(G, start, end)
        self.isWandering = False

    def cell_assignement(self, new_cell) : #si la position est différente des coordonnées de la cellule, on change currentCell
        #if (self.position_x != self.currentCell.x or self.position_y != self.currentCell.y ) :
            self.previousCell = self.currentCell
            self.currentCell = new_cell

    #if (self.building.employees == self.building.required_employees) :
    def leave_building(self) :
        self.isWandering = True
        print(self.isWandering)
        path = self.currentCell.check_cell_around(Cell.Path)
        assert len(path) != 0
        self.cell_assignement(random.choice(path))
        self.inBuilding = False
        # if not isinstance(self, Prefect) and not isinstance(self, Engineer) :
        if not self.alive :
            self.building.map.walkers.append(self)
            self.alive = True
        

        print("Walker is leaving the building on the cell " + str(self.currentCell.x)+ ";" + str(self.currentCell.y))

    def enter_building(self):
        assert self.building in self.currentCell.check_cell_around(type(self.building))
        self.cell_assignement(self.building)
        self.inBuilding = True
        self.currentCell.display()
        self.previousCell.display()
        print("walker enters" )

        if not isinstance(self, Prefect) and not isinstance(self, Engineer) :
            self.building.map.walkers.remove(self)

    def move(self):
        path = self.currentCell.check_cell_around(Cell.Path)
        assert len(path) != 0
        if (len(path) == 1):
            self.cell_assignement(path[0])
        else:
            if isinstance(self.previousCell, Cell.Path): path.remove(self.previousCell)
            self.cell_assignement(random.choice(path))
        print("walker is moving on the cell " + str(self.currentCell.x)+ ";" + str(self.currentCell.y))

    def movePathFinding(self):
        assert len(self.path) != 0
        self.cell_assignement(self.path.pop(0))

class Migrant(Walker):
    def __init__(self, building):
        super().__init__("migrant", building, False)
        self.cell_assignement(self.currentCell.map.array[27][39])
        self.currentCell.map.migrantQueue.append(self)
        # building.map.walkers.append(self)
        self.walker_sprites = dict((k,pygame.image.load("walker_sprites/migrant_sprites/mg_" + k + ".png")) for k in ["top","bot","left","right"])
        self.cart_sprites = dict((k,pygame.image.load("walker_sprites/migrant_sprites/mg_cart_" + k + ".png")) for k in ["top","bot","left","right"])
        # self.screen.blit(pygame.transform.scale(self.walker_sprites["top"], 
        # (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
        self.spawnCount = 0


    def display(self) :
       
        if self.previousCell.x < self.currentCell.x :
            if not self.inBuilding :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["right"], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                self.screen.blit(pygame.transform.scale(self.cart_sprites["right"], (self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.x < 39 :
                self.currentCell.map.array[self.previousCell.x -1][self.currentCell.y].display()
        elif self.previousCell.x > self.currentCell.x :
            if not self.inBuilding :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["left"], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                self.screen.blit(pygame.transform.scale(self.cart_sprites["left"], (self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.x < 39 :
                self.currentCell.map.array[self.previousCell.x +1][self.currentCell.y].display()
        elif self.previousCell.y < self.currentCell.y :
            if not self.inBuilding :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["bot"], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                self.screen.blit(pygame.transform.scale(self.cart_sprites["bot"], (self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.y < 39 :
                self.currentCell.map.array[self.currentCell.x][self.previousCell.y -1].display()
        elif self.previousCell.y > self.currentCell.y :
            if not self.inBuilding :
                self.screen.blit(pygame.transform.scale(self.walker_sprites["top"], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                self.screen.blit(pygame.transform.scale(self.cart_sprites["top"], (self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.y < 39 :
                self.currentCell.map.array[self.currentCell.x][self.previousCell.y +1].display()

        if (len(self.currentCell.check_cell_around(Cell.Path)) > 2 and not (self.previousCell.x == self.path[0].x or self.previousCell.y == self.path[0].y)) or self.building in self.currentCell.check_cell_around(Cell.House):
           for i in self.currentCell.check_cell_around(Cell.Path):
                i.display()
        

    def __str__(self):
        return "Migrant"

    def move(self):
        if not self.inBuilding:
            if len(self.path) == 0:
                self.path_finding(self.currentCell, self.building)
            if len(self.path) == 1:
                self.enter_building()
                self.building.nb_occupants += 5
                self.building.unemployedCount += 5
                if self.building.nb_occupants == self.building.max_occupants and self.building.water:
                    self.building.nextLevel()
            else:
                self.movePathFinding()

class LaborAdvisor(Walker) : 
    def __init__(self, building):
        super().__init__("labor advisor", building, True)
        self.leave_building()
        self.walker_sprites = dict((k,[0,0]) for k in ["top","bot","left","right"])
        for i in self.walker_sprites :
            for j in range(2) : 
                self.walker_sprites[i][j] = pygame.image.load("walker_sprites/LA_sprites/LA_" + i + "_" + str(j) + ".png")    
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/LA_sprites/LA_" + k + ".png")) for k in ["top","bot","left","right"])
        


    def __str__(self):
        return "Labor Advisor"
        
    def move(self) :
        if self.inBuilding: 
            self.leave_building()
        elif len(self.path) == 1:
            self.enter_building()
            self.building.patrol()
        else:
            if self.building.requiredEmployees == self.building.employees:
                if len(self.path) == 0: 
                    self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
            else:
                super().move()
                HouseList = self.currentCell.check_cell_around(Cell.House)
                for i in HouseList : 
                    if i.unemployedCount > 0 : 
                        if i.unemployedCount >= (self.building.requiredEmployees - self.building.employees) : 
                            i.unemployedCount -= (self.building.requiredEmployees - self.building.employees)
                            self.building.employees = self.building.requiredEmployees
                        else : 
                            self.building.employees += i.unemployedCount
                            i.unemployedCount = 0


        
class Prefect(Walker) : 
    def __init__(self, current_prefecture):
        super().__init__("prefect" , current_prefecture, True)
        self.current_building = current_prefecture
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/prefect_sprites/prefect_" + k + ".png")) for k in ["top","bot","left","right"])
        self.walker_sprites = dict((k,[0,0]) for k in ["top","bot","left","right"])
        for i in self.walker_sprites :
            for j in range(2) : 
                self.walker_sprites[i][j] = pygame.image.load("walker_sprites/prefect_sprites/prefect_" + i + "_" + str(j) + ".png")

    def __str__(self):
        return "Prefect"

    def move(self) :
        self.wait += 1
        if self.wait <= 10 :
            return
        # print("yoyoyoyo")
        if self.inBuilding: self.leave_building()
        elif len(self.path) == 1 and not self.isWandering : 
            self.enter_building()
            self.wait = 0
        else:
            if self.ttl == 0:
                if len(self.path) == 0: self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
                self.reset_fire_risk()
                if self.currentCell == self.current_building : self.ttl = 50
            else:
                super().move()
                self.ttl -= 1
                self.reset_fire_risk()

    def reset_fire_risk(self):
        cell = self.currentCell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.Prefecture) and not isinstance(i, Cell.Well) and not i.risk.happened :
                i.risk.resetEvent()
                

class Engineer(Walker):
    def __init__(self, engineerPost):
        super().__init__("engineer", engineerPost, True)
        self.current_building = engineerPost
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/engineer_sprites/engineer_" + k + ".png")) for k in ["top","bot","left","right"])
        self.walker_sprites = dict((k,[0,0]) for k in ["top","bot","left","right"])
        for i in self.walker_sprites :
            for j in range(2) : 
                self.walker_sprites[i][j] = pygame.image.load("walker_sprites/engineer_sprites/engineer_" + i + "_" + str(j) + ".png")

    def move(self) :
        self.wait += 1
        if self.wait <= 10 :
            return
        if self.inBuilding: self.leave_building()
        elif len(self.path) == 1 and not self.isWandering : 
            self.enter_building()
            self.wait = 0
        else:
            if self.ttl == 0:
                if len(self.path) == 0: self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
                if self.currentCell == self.current_building : self.ttl = 50
            else:
                super().move()
                self.ttl -= 1
                self.reset_collapse_risk()

    def reset_collapse_risk(self):
        cell = self.currentCell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.EngineerPost):
                #Method that can reset the risk / timer
                pass



# x increase -> right 
# x decrease -> left 
# y increase -> bot
# y decrease -> top 


