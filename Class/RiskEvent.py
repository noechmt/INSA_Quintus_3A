from threading import *
import time
from Class.Cell import *
import random as rd

class RiskEvent():
    def __init__(self, eType) : 
        self.counter = 0
        self.happened = False
        self.type = eType
        

    def riskIncrease(self) :
        self.counter += rd.randint(0,1)
        if self.counter == 10 :
            self.happened = True


    def resetEvent(self) :
        self.counter = 0

    
         


     