from threading import *
import time
from Cell import *

class TimerEvent (Thread):
    def __init__(self, building) : 
        if isinstance(building, House) : 
            self.risk_time = 120
        if isinstance(building, Prefecture) :
            self.risk_time = 240
            

    def countdown(self, t) : 
        while t:
            time.sleep(1)
            t -= 1

    
    
