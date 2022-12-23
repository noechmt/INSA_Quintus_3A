import Class.Cell as Cell
import random
import pygame

import networkx as nx

class Walker() : 
    def __init__(self, job, building, state) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.building = building #string (prefecture, engineer post, house)
        self.currentCell = building #La cellule de départ de l'entity : Cell
        self.previousCell = None
        self.inBuilding = state
        self.path = []
        self.ttl = 10
        print("Walker spawn")
        self.screen = self.currentCell.screen
        self.walker_sprites = {}

    def display(self) :
        self.screen.blit(pygame.transform.scale(self.walker_sprites["top"], (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))

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

    def cell_assignement(self, new_cell) : #si la position est différente des coordonnées de la cellule, on change currentCell
        #if (self.position_x != self.currentCell.x or self.position_y != self.currentCell.y ) :
            self.previousCell = self.currentCell
            self.currentCell = new_cell

    #if (self.building.employees == self.building.required_employees) :
    def leave_building(self) :
        path = self.currentCell.check_cell_around(Cell.Path)
        assert len(path) != 0
        self.cell_assignement(random.choice(path))
        self.inBuilding = False
        self.building.map.walkers.append(self)
        print("Walker is leaving the building on the cell " + str(self.currentCell.x)+ ";" + str(self.currentCell.y))

    def enter_building(self):
        assert self.building in self.currentCell.check_cell_around(type(self.building))
        self.cell_assignement(self.building)
        self.inBuilding = True
        self.building.map.walkers.remove(self)

    def move(self):
        path = self.currentCell.check_cell_around(Cell.Path)
        assert len(path) != 0
        if (len(path) == 1):
            self.cell_assignement(path[0])
        else:
            if isinstance(self.previousCell, Cell.Path): path.remove(self.previousCell)
            self.cell_assignement(random.choice(path))
        print("Prefect is moving on the cell " + str(self.currentCell.x)+ ";" + str(self.currentCell.y))

    def movePathFinding(self):
        assert len(self.path) != 0
        self.cell_assignement(self.path.pop(0))

class Migrant(Walker):
    def __init__(self, building):
        super().__init__("migrant", building, False)
        self.cell_assignement(self.currentCell.map.array[30][39])
        building.map.walkers.append(self)
        self.walker_sprites = dict((k,pygame.image.load("walker_sprites/test/migrant_" + k + ".png")) for k in ["top","bot","left","right"])
        self.display()

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

    def __str__(self):
        return "Prefect"

    def move(self) :
        if self.inBuilding: self.leave_building()
        elif len(self.path) == 1: self.enter_building()
        else:
            if self.ttl == 0:
                if len(self.path) == 0: self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
            else:
                super().move()
                self.ttl -= 1
                self.reset_fire_risk()

    def reset_fire_risk(self):
        cell = self.currentCell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.Prefecture):
                #Method that can reset the risk / timer
                pass

class Engineer(Walker):
    def __init__(self, engineerPost):
        super().__init__("engineer", engineerPost, True)

    def move(self) :
        if self.inBuilding: self.leave_building()
        elif len(self.path) == 1: self.enter_building()
        else:
            if self.ttl == 0:
                if len(self.path) == 0: self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
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

