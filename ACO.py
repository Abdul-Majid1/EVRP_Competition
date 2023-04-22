import random
from  ACO_fileRead import FileRead
from Ant import Ant
import math
import matplotlib.pyplot as plt
import numpy as np


class AntColonyOptimization:
    def __init__(self, alpha, beta, iteration, numAnts, evapRate, path , max_charge) -> None:
        self.alpha = alpha
        self.beta = beta
        self.iteration = iteration
        self.numAnts = numAnts
        self.evapRate = evapRate
        self.Q = 1
        temp = FileRead(path)
        fileInst = temp.instanceTaker()
        
        self.capacity = fileInst["capacity"]
        self.depot = 1 
        # print(self.depot)
        self.dimension = fileInst["dimension"]
        self.demand = fileInst["demand"]
        self.distaneMatrix = fileInst["edge_weight"]  

        for i in range(0,len(self.distaneMatrix)):
              for j in range(0,len(self.distaneMatrix[0])):
                  self.distaneMatrix[i][j]= self.distaneMatrix[i][j]/50
        #N1:Here we have just converted the minimization parameter to time instead of the distance
        self.max_charge =max_charge
        self.charge = max_charge
        self.num_charges = fileInst["vehicles"]
        #N2: New quantity that keeps track of the current EV's charge and total number of recharge stations 
        self.inverseDM = [[1/i if i != 0 else 0 for i in lst] for lst in self.distaneMatrix]
        self.path = path

    def AntMaking(self):
        fullRoute = []
        unvisited = [i for i in range(2, self.dimension+1-self.num_charges)]
        # N3: change in the unvisited list to remove charging stations and now the node number 1 is the depot instead of node number 2

       
        currentCity = self.depot
        truckCapacity = self.capacity
        totalDistance = 0
        tempRoute = []
        tempRoute.append(self.depot)
        while len(unvisited) >= 1:
            # Choosing random city from unvisited cities
            tempCity = random.randint(0, len(unvisited) - 1)
            
            city = unvisited[tempCity]
            if self.demand[city-1] <= truckCapacity :
                truckCapacity -= self.demand[city-1]
                totalDistance += self.distaneMatrix[currentCity-1][city-1]
                currentCity = city
                tempRoute.append(city)
                # N4:Adjusting the indexes since the benchmark starts from node 1 but indexing of its values starts from 0 
                #  Now its time to pop the city from unvisited
                unvisited.pop(tempCity)
            else:
                # This means that the truck is full and we need to go back to depot and line 70 will simply add the distance of depot to current city or vice versa
                totalDistance += self.distaneMatrix[currentCity-1][0]
                tempRoute.append(self.depot)
                fullRoute.append(tempRoute)
                # Changing the capacity of vehicles
                truckCapacity = self.capacity
                tempRoute = []
                tempRoute.append(self.depot)
                currentCity = self.depot
                truckCapacity -= self.demand[city-1]
                totalDistance += self.distaneMatrix[currentCity-1][city-1]
                currentCity = city
                tempRoute.append(city)
                unvisited.pop(tempCity)

        # Now I have to go back to depot to complete the route
        tempRoute.append(self.depot)
        totalDistance += self.distaneMatrix[currentCity-1][0]
        fullRoute.append(tempRoute)
        antObject = Ant(fullRoute, totalDistance)        
        print(fullRoute, totalDistance)
        return antObject
    #N5: The indexing changes needed to take place all across the board 

    def AntColonyInitialization(self):
        # Initalizing Pheromones with 1
        self.numNodes = len(self.distaneMatrix) - self.num_charges
        self.pheromones = [[0 for i in range(self.numNodes)] for j in range(self.numNodes)]
        self.ants = [0 for i in range(self.numAnts)]
        #N6 : Removing the extra recharge stations from the pheromones too


        # Making Artificial Ants by calculating Routes
        self.ants = []
        for i in range(self.numAnts):
            temp = self.AntMaking()
            self.ants.append(temp)
       

    def computingDeltaT(self):
        deltaT = [[0 for i in range(self.dimension-self.num_charges)] for j in range(self.dimension - self.num_charges)]

        for ant in self.ants:
            for route in ant.routes:
                for path in range(0,len(route)-1):
                    deltaT[route[path]-1][route[path+1]-1] += 1/ant.distance
                
        return deltaT
        # N7: Smart assossiation of the -1 wherever City is one less tahn the index we want to assign it too

    def MMAS_deltaT(self):
        deltaT = [[0 for i in range(self.dimension-self.num_charges)] for j in range(self.dimension - self.num_charges)]
        min_distance=math.inf
        min_route=None
        for ant in self.ants:
            if ant.distance< min_distance:
                min_distance = ant.distance 
                min_route = ant.routes
        for route in min_route:
                for path in range(0,len(route)-1):
                    deltaT[route[path]-1][route[path+1]-1] += 1/min_distance
        return deltaT
        # N10: Testing of the performance of the Min Max Ant colony system in this benchmark data set



    def calculateProbabilities(self, possibleCities, currentCity):

        probCities = []
        for i in possibleCities:
            temp = math.pow(self.Tau[currentCity-1][i-1], self.alpha) + math.pow(self.inverseDM[currentCity-1][i-1], self.beta)
            probCities.append(temp)
        sumProb = sum(probCities)
        finalProb = [i/sumProb for i in probCities]

        # Now making the ranges of Probabilities
        probRange = {}
        startRange = 0
        for i in range(len(finalProb)):
            probRange[i] = [startRange , startRange + finalProb[i]]
            startRange += finalProb[i]        
        return probRange



    def simulateAnt(self):
        # Copying the code from AntMaking as now I have to decide the city with the help of probabilities



        #N8: Making changes in the copied code since I made changes in the original
        #N9: Notice depot is now part of the unvisited and condition is terminated if only that is left
        fullRoute = []
        unvisited = [i for i in range(2,self.dimension-self.num_charges)]
        currentCity = self.depot
        truckCapacity = self.capacity
        totalDistance = 0
        tempRoute = []
        tempRoute.append(self.depot)
        while len(unvisited) >1:
            # Choosing random city from unvisited cities
            possibCities = []
            for i in unvisited:
                if self.demand[i-1] <= truckCapacity and i!= currentCity:
                    possibCities.append(i)
            if len(possibCities)!=0:
                probRange = self.calculateProbabilities(possibCities, currentCity)
                randNum = random.random()
                for i in probRange:
                    if randNum >= probRange[i][0] and randNum <= probRange[i][1]:
                        selectedCity = i
                        break  
                nextCity = possibCities[selectedCity]
            else:
                # selectedCity=self.depot          
                nextCity = self.depot
            truckCapacity -= self.demand[nextCity-1]
            totalDistance += self.distaneMatrix[currentCity-1][nextCity-1]

            #N9: Only visit the depot when it is absolutely essential to(is giving better results
            currentCity = nextCity
            tempRoute.append(currentCity)
            if currentCity == self.depot:
                truckCapacity = self.capacity
                fullRoute.append(tempRoute)
                tempRoute = [self.depot]
            else:
                for i in unvisited:
                    if i == nextCity:
                        unvisited.remove(i)
                        break

        # Now the path will again go to Depot to make a full route
        tempRoute.append(self.depot)
        totalDistance += self.distaneMatrix[currentCity-1][0]
        fullRoute.append(tempRoute)
        return Ant(fullRoute, totalDistance)



    def updatePhermone(self):
        DeltaT = self.computingDeltaT()
        for i in range(len(self.Tau)):
            for j in range(len(self.Tau)):
                self.Tau[i][j] = (self.Tau[i][j] * self.evapRate) + DeltaT[i][j]
            

    def ACO_main(self):
        self.AntColonyInitialization()
        # Updating the Tau Matrix
        self.Tau = self.computingDeltaT()
        
        minDist = float('inf')
        minDistanceList = []
        avgDistanceList = []
        for i in range(self.iteration):
            tempAnt = []
            avgDistance = 0
            for j in range(self.numAnts):
                tempAnt.append(self.simulateAnt())
            self.ants = tempAnt
            self.updatePhermone()
            for ant in self.ants:
                if ant.distance < minDist:
                    minDist = ant.distance
                    minRoute = ant.routes
                avgDistance += ant.distance
      
            avgDistance = avgDistance // self.numAnts
            minDistanceList.append(minDist)
            avgDistanceList.append(avgDistance)
        return minDistanceList, avgDistanceList, minDist,minRoute

if __name__ == "__main__":
    temp = AntColonyOptimization(2, 3, 300, 10, 0.5, "benchmark.evrp",40)
    result = temp.ACO_main()
    print(f'Minimum Distance is {result[2]}')
    print(f'Minimum Route is {result[3]}')
    total_time=0
    for i in result[3]:
        # print(i)
        for j in range(1,len(i)):
            
            total_time = total_time + temp.distaneMatrix[i[j-1]-1][i[j]-1]
          
    print(total_time*60)

# Code for geenrating graph with repect to changing alpha beta gamma and evaporation rate
filename = "A-n32-k5"

# alpha = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# beta = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# evapRate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# iterations = 50
# AllResults = []
# for i in range(len(alpha)):
#     temp = AntColonyOptimization(alpha[i], beta[i], iterations, 10, evapRate[i], filename )
#     result = temp.ACO_main()
#     AllResults.append(result[0][-1])

# # Now I have to create a 4d graph using Matplot Lib

# print(AllResults)

