
class Walker() : 
    def __init__(self, job, position_x, position_y, starting_Cell, building) :
        self.job = job #le métier (migrant, worker, etc) : string
        self.position_x = position_x #position sur la map : int
        self.position_y = position_y #position sur la map : int
        self.current_Cell = starting_Cell #La cellule de départ de l'entity : Cell
        self.previous_cell = None
        self.current_Cell.current_map.walker_list.append(self)
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
                    if self.current_Cell.current_map.array[self.current_Cell.x + i][self.current_Cell.y + j].type_of_cell  == 1:
                        path.append(self.current_Cell.current_map.array[self.current_Cell.x + i][self.current_Cell.y + j])
        return path

    def leave_building(self) :
        #if (self.Walkers_building.employees == self.Walkers_building.required_employees) :
            for i in range(-1, 2) :
                #print(abs(i))
                for j in range(-1, 2) :
                    #print("Test : " + str(self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j].type_of_cell)) 
                    if abs(i) != abs(j) and self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j].type_of_cell  == 1: 
                        #print("Test : " + str(self.current_building.x + i) + ";" + self.current_building.y + j)
                        self.cell_assignement(self.current_building.current_map.array[self.current_building.x + i][self.current_building.y + j])
                        self.prefect_in_building = False 
                        break
            print("Prefect is leaving the building on the cell " + str(self.current_Cell.x)+ ";" + str(self.current_Cell.y))