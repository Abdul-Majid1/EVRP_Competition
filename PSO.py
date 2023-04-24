import random
import math
from  Bird import bird
from ACO_fileRead import FileRead
from ACO_energy import AntColonyOptimization
class PSO:
    def __init__(self, momentum, accelConst, canvasSize, numSize, food_radius, food_fitness,numFood,accelConst2) -> None:
        self.momentum = momentum
        self.accelConst = accelConst
        
        instance = FileRead("benchmark.evrp")
        real =instance.instanceTaker()
        list_coord = real["node_coord"]
        self.X_right = 0
        self.X_left = math.inf
        self.Y_top = 0
        self.Y_down  = math.inf
        for i in list_coord:
            if i[0] > self.X_right:
                self.X_right = i[0]

            if i[0] < self.X_left:
                self.X_left = i[0]

            if i[1] > self.Y_top:
                self.Y_top = i[1]

            if i[0] < self.Y_down:
                self.Y_down = i[1]    
        
        
        self.numBirds = numSize
        self.dimension = 2
        self.accelConst2 = accelConst2
        self.stations = real["stations"]
        print()
        self.gBest = [[random.randint(int(self.X_left), int(self.X_right)), random.randint(int(self.Y_down), int(self.Y_top))] for i in range(0,self.stations) ]
        print(self.gBest)
        self.gBest_value=math.inf
        self.found_food=0
   
   
   
    def birdMaking(self):
        self.birds = []
        for i in range(self.numBirds):
            tempBird = bird(velocity = [[0,0] for i in range(self.stations)], position= [[random.randint(int(self.X_left), int(self.X_right)), random.randint(int(self.Y_down), int(self.Y_top))] for i in range(0,self.stations) ],  pBest = [[random.randint(int(self.X_left), int(self.X_right)), random.randint(int(self.Y_down), int(self.Y_top))] for i in range(0,self.stations) ],  lbest = [[random.randint(int(self.X_left), int(self.X_right)), random.randint(int(self.Y_down), int(self.Y_top))] for i in range(0,self.stations) ],pbest_value=math.inf)
            self.birds.append(tempBird)
        
    
    
    def updateVelocity(self):
        list_fitness=[]
        for index in range(0,len(self.birds)):
            bird=self.birds[index]

            temp = AntColonyOptimization(2, 3, 300, 10, 0.5, "benchmark.evrp",1.4,8)
            result = temp.ACO_main()
            fitness=result[2]
            
            if fitness < self.gBest_value:
                self.gBest_value = fitness
                self.gBest = bird.position 
            
            if fitness < bird.pBest_value:
                bird.pBest_value = fitness
                bird.pBest = bird.position

            self.birds[index] = bird

        for index in range(0,len(self.birds)):
            bird = self.birds[index]  
            added_list =[]
            indexes_used=[]
            added_list_2 =[]
            indexes_used_2=[]
            for i in range(0,self.stations):
                min_index = None
                min_value = math.inf
                
                for j in range(0,self.stations):
                    distance= math.sqrt(((self.gBest[j][0] - bird.position[i][0])**2) + ((self.gBest[j][1] - bird.position[i][1])**2))
                    if distance < min_value and j not in indexes_used:
                        min_value = distance
                        min_index = j
                indexes_used.append(min_index)

                added_list.append(self.gBest[min_index])
                # print(bird.position)
                # print(added_list)
                
                # print()
                # print()
                # print()

                for j in range(0,self.stations):
                    distance= math.sqrt(((bird.pBest[j][0] - bird.position[i][0])**2) + ((self.gBest[j][1] - bird.pBest[i][1])**2))
                    if distance < min_value and j not in indexes_used_2:
                        min_value = distance
                        min_index = j
                indexes_used_2.append(j)
                added_list_2.append(bird.pBest[min_index])
                
            
            for i in range(0,self.stations):
                for j in range(0,self.dimension):
                    bird.velocity[i][j] = self.momentum * bird.velocity[i][j] + self.accelConst * random.random() * (added_list_2[i][j] - bird.position[i][j]) + self.accelConst2 * random.random() * (added_list[i][j] - bird.position[i][j])
            self.birds[index] = bird
            

        
    
    def updatePosition(self, bird):
        for i in range(self.dimension):
            bird.position[i] = bird.position[i] + bird.velocity[i]
            if bird.position[i] > self.height:
                bird.position[i] = self.height
            if bird.position[i] < 0:
                bird.position[i] = 0
        return bird


    def main_algorithm(self, iterations):
        self.birdMaking()
        
        for i in range(0,iterations):
            self.updateVelocity()
                # if result:
                #     counter = counter + 1
                #     print(counter)
                #     self.birds[k].pBest = self.birds[k].position
                #     # print(self.gbest)
                #     # print(self.food)
                    
instance= PSO(momentum=0.9, accelConst=0.2, canvasSize= (700,700), numSize=10, food_radius=15, food_fitness=56,numFood=3, accelConst2=0.5)
instance.main_algorithm(100)





