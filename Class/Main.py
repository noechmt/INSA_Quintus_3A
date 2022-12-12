from time import sleep
from Map import *

myMap = Map(5)
myMap.init_path()
#myMap.display()
# myMap.array[1][1] = House(1, 1, myMap)

#myMap.array[2][2] = Fountain(2, 2, myMap)
myMap.array[3][2].build("path")
myMap.array[2][2].build("path")
myMap.array[2][3].build("path")
myMap.array[2][4].build("path")
myMap.array[3][4].build("path")
myMap.array[3][0].build("house")
myMap.array[2][1].build("well")
print(myMap)


while 1:
      myMap.update()
      print(myMap)
      sleep(2)
# myMap.array[3][0].prefect.leave_building()
# for i in range(15):
#     myMap.array[3][0].prefect.prefect_move()
#print(myMap.array[1][1].type_of_building)
#myMigrant = Migrant(myMap.array[3][0])



#TODO 
# risks
#house levels
#animation des walkers 
#archeduc 

