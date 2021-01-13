#50x50 grid
import random
import math

#generate a list of random cities (points) 
def generateCities (num_cities):
    global citiesList
    citiesList = []
    newCity = []
    for x in range (0,num_cities):
        newCity = []
        newCity.append (random.randint(0,51))
        newCity.append (random.randint(0,51))
        citiesList.append(newCity)
        
#first city in the citiesList must be the starting city for all of the genomes in population
def populate (pop_size,citiesList):
    global population
    population = {}

    for x in range (1,pop_size+1):
        randomSolution = []

        firstCity = citiesList[0]
        remainingCities = citiesList [1:]

        random.shuffle(remainingCities)

        randomSolution.append(firstCity)
        randomSolution=randomSolution + remainingCities

        population.update({x:randomSolution})
        #population[x] = randomSolution

def distance (city1,city2): #calculates distance between 2 points
    x1 = city1[0]
    y1 = city1[1]
    x2 = city2[0]
    y2 = city2[1]

    dist= math.sqrt ( (x2-x1)**2 + (y2-y1)**2 )

    return dist
#population is a dictionary storing genomes 1 to population size with a corresponding random solution in list form

#calculate the fitness of each genome in the population, the fitness is equal to the total distance, start and return to the first city
def calcFitness (population):
    global fitness 
    fitness = {} #store corresponding fitness values (genome number) in fitness dictionary

    firstCity = citiesList[0]
    for x in range (1, len(population)+1): #loop through each random solution in the dictionary
        cmldist = 0
        for index,point in enumerate(population[x]): #for each point in the solution, calculate distance
            firstCity = citiesList [0]

            if index == len(population[x])-1: #if the index is the last element of the list in the solution
                cmldist = cmldist + distance(point,firstCity)
            else:
                cmldist = cmldist + distance (point,population[x][index+1])

        fitness.update({x:cmldist})    
        

def generation0 (pop_size): #change to this when this is done: def generation0 (num_cities,pop_size):
    global generationPop
    global generationFit
    global popSize
    global numCities
    
    #generateCities (num_cities)
    popSize = pop_size 
    numCities = len(citiesList)

    populate(pop_size,citiesList)
    calcFitness(population)

    generationPop = {}
    generationPop.update ({"generation"+str(0):population})
    #generationPop ["generation" + str(0)] = population

    generationFit = {}
    generationFit.update ({"generation"+str(0):population})
    #generationFit ["generation" + str(0)] = fitness

    print (generationPop)
    

def geneticAlg (num_generations, generationPop,generationFit):
    for currentgen in range (1,num_generations+1):
        print("ran once")
        #duplicate generation0 into generation1 for edits, duplicate the previous generation into current gen
        generationPop.update({"generation"+str(currentgen): generationPop.get("generation"+str(currentgen-1))})
        generationFit.update({"generation"+str(currentgen): generationFit.get("generation"+str(currentgen-1))})

        #elitism, kill bottom 20% and kill additional 20% randomly 
        numKill = math.floor(popSize*0.2) 
        randomKill = math.floor(popSize*0.2)
        popElite = popSize - (numKill + randomKill) 

        print(generationPop)
        

        for notElite in range (popSize-numKill+1,popSize+1): #kill the bottom 20%, set the value to none
            
            generationPop["generation" + str(currentgen)].update ( { notElite : None })
            generationFit["generation" + str(currentgen)].update ( { notElite : None })
        

citiesList = [ [2,1],[3,1],[4,1],[5,1],[6,4],[5,7],[4,7],[3,7],[2,7],[1,4] ]
generation0 (10)
geneticAlg(1,generationPop,generationFit)

print(generationPop)

