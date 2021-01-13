#main
import random
import math
import statistics

citiesList = [ [2,1],[3,1],[4,1],[5,1],[6,4],[5,7],[4,7],[3,7],[2,7],[1,4] ]
numCities = len(citiesList)
startCity = citiesList [0]
def quicksort (array):
    length=len(array)
    if length <= 1: #if the length of the array is less than or equal to 1, it is already sorted
        return array
    else:
        middle = math.floor (length/2)
        #determine the pivot number and index using the middle of 3 numbers
        if array [0] <= array[middle] <= array[length-1] or array[length-1] <= array [middle] <= array[0]:
            pivotindex = middle
        elif array[middle] <= array [0] <= array[length-1] or array[length-1] <= array[0] <= array[middle]:
            pivotindex = 0
        else:
            pivotindex = length-1
        pivot = array.pop(pivotindex)
        left = [] 
        right = []
        for element in array:
            if element > pivot:
                right.append(element)
            else:
                left.append(element)
        return quicksort(left)+[pivot] +quicksort(right)

def distance (city1,city2): #calculates distance between 2 points
    x1 = city1[0]
    y1 = city1[1]
    x2 = city2[0]
    y2 = city2[1]
    dist= math.sqrt ( (x2-x1)**2 + (y2-y1)**2 )
    return dist

def calcFitness(population):
    global fitness
    fitness = {}
    firstCity = citiesList [0]

    for x in range(1,popSize+1):
        cmldist = 0 
        for index,point in enumerate(population[x]): #for each point in the solution, calculate distance
            firstCity = citiesList [0]

            if index == len(population[x])-1: #if the index is the last element of the list in the solution
                cmldist = cmldist + distance(point,firstCity)
            else:
                cmldist = cmldist + distance (point,population[x][index+1])

        fitness.update({x:cmldist})
    return fitness   

def updateFitness (solution): #accepts a single species in list
    cmldist = 0
    
    for index,point in enumerate(solution):
        if index == numCities-1:
            cmldist = cmldist + distance(point,startCity)
        else:
            cmldist = cmldist + distance (point,solution[index+1])
    return cmldist

def generation0 (pop_size):
    global generationPop
    global generationFit
    global popSize

    popSize = pop_size 
    #create empty dictionaries for total generation population/fitness data
    generationPop = {}
    generationFit = {}

    population0 = {}

    #populate generation0 with population0
    for x in range (1,pop_size+1):
        randomSolution = []

        firstCity = citiesList[0]
        remainingCities = citiesList [1:]

        random.shuffle(remainingCities)

        randomSolution.append(firstCity)
        randomSolution=randomSolution + remainingCities

        population0.update({x:randomSolution})
    
    generationPop.update({"generation0":population0})
    
    calcFitness(generationPop["generation0"])

    generationFit.update({"generation0":calcFitness(generationPop["generation0"])})

def geneticAlg (total_gens, generationPop,generationFit):
    global totalgens 
    totalgens = total_gens
    numKill = math.floor(popSize*0.4)

    #duplicate the previous generation into the next generation, duplicate total_gens number of times.
    for currentgen in range (1,total_gens+1): 

        generationPop.update({"generation"+str(currentgen): generationPop["generation"+ str(currentgen-1)].copy()})
        generationFit.update({"generation"+str(currentgen): generationFit["generation"+ str(currentgen-1)].copy()})

        #sort the fitness and population values , 1: is the best fitness/sequence 
        sortFit = list ( generationFit["generation"+str(currentgen)].values() )
        sortPop = list ( generationPop["generation"+str(currentgen)].values() )

        sortDict = {}
        sortDict.clear()
        for species in range (0,popSize):
            sortDict.update({sortFit[species]:sortPop[species]})
        sortFit = quicksort(sortFit)
        sortPop.clear() 

        for fitness in sortFit:
            sortPop.append(sortDict.get(fitness))
        
        for species in range (1,popSize+1):
            generationPop["generation"+str(currentgen)].update({species:sortPop[species-1]})
            generationFit["generation"+str(currentgen)].update({species:sortFit[species-1]})

        #kill off bottom 40%
        for notElite in range (popSize-numKill+1,popSize+1):

            generationPop["generation"+str(currentgen)].update({notElite:None})
            generationFit["generation"+str(currentgen)].update({notElite:None})
    
        #the current generation elite have been created (same as the previous generation with the bottom 40% killed)
        #crossover and mate to fill the "none" or killed off members of population
        #assume that each city in the list is unique, there is only one of each city

        #loop through None values in generationPop/Fit [currentgen]
        for notElite in range (popSize-numKill+1,popSize+1):

            #choose a parent randomly
            randselection = random.randint(1,popSize-numKill)
            parent = generationPop["generation"+str(currentgen)].get(randselection)

            #choose a random segment of random length from the randomly selected parent
            segment = random.sample(range(0,numCities),2)

            if segment[0] < segment[1]:
                start = segment[0]
                end = segment [1]
            else:
                start = segment[1]
                end = segment [0]

            #create child, and copy the selected segment from the parent to the exact indexes in the child
            child = [None]*numCities
            child[start:end] = parent[start:end]

            #make sure the first city is always the same
            if child[0] == None:
                child[0] = startCity
            else:
                pass

            #create fill, a list with the remaining cities that need to be in the solution
            #copies the parent, then removes the cities that come from the duplicated segment
            fill = parent.copy()
            for city in child:
                if city != None:
                    fill.remove(city)
            
            #create a list with the missing indexes of the child
            fillindex = []
            for count,city in enumerate(child):
                if city == None:
                    fillindex.append(count)

            #shuffle the fillindex/fill cities
            random.shuffle(fillindex)
            random.shuffle(fill)

            #fill the empty spaces in the new child with the remaining cities at remaining indexes randomly
            for index,city in zip(fillindex,fill):
                child[index] = city

            #set the missing species in generationPop to the new child
            #calculate the fitness and update the fitness 
            generationPop["generation"+str(currentgen)].update({notElite:child})
            generationFit["generation"+str(currentgen)].update({notElite:updateFitness(child)})

generation0 (5)

geneticAlg (5, generationPop,generationFit)

#print (generationPop)
#print (generationFit)

#create graphing data sets
generationx = []
best_gen_solutiony = []
best_gen_fity = []

mean_y = []

for x in range (0,totalgens+1):
    generationx.append(x)

for currentgen in range (0,totalgens+1):

    currentgenfitness = generationFit["generation" + str(currentgen)].values()
    mean_y.append(statistics.mean(currentgenfitness))
    
    best_gen_fity.append(max(currentgenfitness))
    speciesposition = currentgenfitness.index(max(currentgenfitness))+1
    best_gen_solutiony.append(generationPop["generation"+str(currentgen)][speciesposition])
    