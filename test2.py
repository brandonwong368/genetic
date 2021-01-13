import math

citiesList = [ [2,1],[3,1],[4,1],[5,1],[6,4],[5,7],[4,7],[3,7],[2,7],[1,4] ]

sol = [ [0,0], [1,1], [0,1] ,[1,0] ]

popSize = len(citiesList)

firstCity = citiesList [0]

def distance (city1,city2): #calculates distance between 2 points

    x1 = city1[0]
    y1 = city1[1]
    x2 = city2[0]
    y2 = city2[1]
    dist= math.sqrt ( (x2-x1)**2 + (y2-y1)**2 )
    return dist

def updateFitness (solution):
    cmldist = 0
    for index,point in enumerate(solution):
        if index == popSize-1:
            cmldist = cmldist + distance(point,firstCity)
        else:
            cmldist = cmldist + distance (point,solution[index+1])
    return cmldist



print ( updateFitness(citiesList) )

