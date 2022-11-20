import threading as th

class TimerEvent :
    def __init__(self, building, type_of_event) :
        self.building = building
        match type_of_event :
            case "fire" :
                self.timer = th.Timer(120, self.building.destroy())
            case "damage" : 
                self.timer = th.Timer(240, self.building.destroy()) # pas les vrais valeur
    
    def start(time):
        pass