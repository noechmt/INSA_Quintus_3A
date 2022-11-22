import Cell
import random

class Walker() : 
    def __init__(self, job, building) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.current_Cell = building #La cellule de départ de l'entity : Cell
        self.previous_cell = None
        self.current_Cell.map.walker_list.append(self)
        self.Walkers_building = building #string (prefecture, engineer post, house)
        
        

    def move_up(self) : #bouger d'une case vers le haut
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_y += 1

    def move_down(self) : #bouger d'une case vers le bas
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_y -= 1

    def move_left(self) : #bouger d'une case vers la gauche
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_x -= 1
 
    def move_right(self) : #bouger d'une case vers la droite
        assert (0 <= self.position_x < 40 and 0 <= self.position_y < 40)
        self.position_x += 1
    
    def cell_assignement(self, new_cell) : #si la position est différente des coordonnées de la cellule, on change current_Cell
        #if (self.position_x != self.current_Cell.x or self.position_y != self.current_Cell.y ) :
            self.previous_cell = self.current_Cell
            self.current_Cell = new_cell

    def check_path(self) :
        path = []
        for i in range(-1, 2) :
            for j in range(-1, 2) : 
                if abs(i) != abs(j) and self.current_Cell.inMap(self.current_Cell.x + i, self.current_Cell.y + j):
                    if isinstance(self.current_Cell.map.getCell(self.current_Cell.x + i,self.current_Cell.y + j), Cell.Path):
                        path.append(self.current_Cell.map.getCell(self.current_Cell.x + i, self.current_Cell.y + j))
        return path

    def leave_building(self) :
        #if (self.Walkers_building.employees == self.Walkers_building.required_employees) :
            for i in range(-1, 2) :
                #print(abs(i))
                for j in range(-1, 2) :
                    #print("Test : " + str(self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j].type_of_cell)) 
                    if abs(i) != abs(j) and isinstance(self.current_building.map.getCell(self.current_building.x + i, self.current_building.y + j), Cell.Path): 
                        #print("Test : " + str(self.current_building.x + i) + ";" + self.current_building.y + j)
                        self.cell_assignement(self.current_building.map.getCell(self.current_building.x + i, self.current_building.y + j))
                        self.prefect_in_building = False 
                        break
            print("Prefect is leaving the building on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

class Prefect(Walker) : 
    def __init__(self, current_prefecture):
        super().__init__("prefect" , current_prefecture)
        self.prefect_in_building = True
        self.current_building = current_prefecture

    def prefect_move(self) :
        if not(self.prefect_in_building):
            path = self.check_path()
            if (len(path) == 1):
                self.cell_assignement(path[0])
            else:
                path.remove(self.previous_cell)
                self.cell_assignement(random.choice(path))
        print("Prefect is moving on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))

class LaborAdvisor(Walker) : 
    def __init__(self, building):
        super().__init__("labor advisor", building)
        self.starting_Cell = building

