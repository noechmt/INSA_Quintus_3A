import Cell
import random

import networkx as nx

class Walker() : 
    def __init__(self, job, building, state) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.current_Cell = building #La cellule de départ de l'entity : Cell
        self.previous_cell = None
        self.current_Cell.map.walker_list.append(self)
        self.building = building #string (prefecture, engineer post, house)
        self.inBuilding = state
        building.map.walkers.append(self)

        
    def cell_assignement(self, new_cell) : #si la position est différente des coordonnées de la cellule, on change current_Cell
        #if (self.position_x != self.current_Cell.x or self.position_y != self.current_Cell.y ) :
            self.previous_cell = self.current_Cell
            self.current_Cell = new_cell

    #if (self.building.employees == self.building.required_employees) :
    def leave_building(self) :
        path = self.current_Cell.check_cell_arround(Cell.Path)
        assert len(path) != 0
        self.cell_assignement(random.choice(path))
        self.inBuilding = False 
        print("Walker is leaving the building on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

    def enter_building(self):
        assert self.building in self.current_Cell.check_cell_arround(Cell.House)
        self.cell_assignement(self.building)
        self.inBuilding = True

    def move(self):
        path = self.current_Cell.check_cell_around(Cell.Path)
        assert len(path) != 0
        if (len(path) == 1):
            self.cell_assignement(path[0])
        else:
            path.remove(self.previous_cell)
            self.cell_assignement(random.choice(path))
        print("Prefect is moving on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

class Migrant(Walker):
    def __init__(self, building):
        super().__init__("migrant", building, False)
        self.cell_assignement(self.current_Cell.map.array[2][2])
        self.path = None
        self.path_finding()

    def path_finding(self):
        # Create a graph
        G = nx.Graph()

        # Loop through the map to add edges to the graph
        for l in self.current_Cell.map.array:
            for i in l:

                #Check if the cell is a path
                if isinstance(i, Cell.Path):
                    #Get an array of all neighbor path
                    cell_around = i.check_cell_around(Cell.Path)
                    #Loop through this array
                    for j in cell_around:
                        #print("Add edge from "+str((i.x, i.y))+" to "+str((j.x, j.y)))
                        G.add_edge(i, j)

                #Check if the cell is a house
                if isinstance(i, Cell.House):
                    cell_around = i.check_cell_around(Cell.Path)
                    for j in cell_around:
                        #print("Add edge from "+str((i.x, i.y))+" to "+str((j.x, j.y)))
                        G.add_edge(i, j)

        #Calculate with the dijkstra algorithm the shortest path
        self.path = nx.dijkstra_path(G, self.current_Cell, self.building)

    def enter_building(self):
        super().enter_building()
        assert self.building.nb_occupants < self.building.max_occupants
        self.building.unemployedCount += 1
        self.nb_occupants += 1
        

    def move(self):
        if not self.inBuilding:
            assert len(self.path) != 0
            self.cell_assignement(self.path.pop(0))

class LaborAdvisor(Walker) : 
    def __init__(self, building):
        super().__init__("labor advisor", building, True)
        
    def move(self) : 
        super().move()
        HouseList = self.current_Cell.check_cell_around(Cell.House)
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

    def move(self) :
        if not(self.inBuilding):
           super().move()
           self.reset_fire_risk()

    def reset_fire_risk(self):
        cell = self.current_Cell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.Building.Prefecture):
                #Method that can reset the risk / timer
                pass

class Engineer(Walker):
    def __init__(self, engineerPost):
        super().__init__("engineer", engineerPost, True)

    def move(self):
        if not(self.inBuilding):
            super().move()
            self.reset_collapse_risk

    def reset_collapse_risk(self):
        cell = self.current_Cell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.Building.EngineerPost):
                #Method that can reset the risk / timer
                pass

