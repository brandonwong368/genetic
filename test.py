import math
import random
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
        return quicksort(right)+[pivot] +quicksort(left)

def bubbleSort(array):
    for i in range (0,len(array)-1):
        for index in range(0,len(array)-1):
            if array[index] > array[index+1]:
                array[index],array[index+1] = array[index+1],array[index]
    return array

def sort():

    sortFit = list(f.values())
    sortPop = list(p.values())


    popSize = len(sortFit)
    sortDict = {}

    print(sortFit)
    print(sortPop)

    #create sorting Dict
    for species in range (0,popSize):
        sortDict.update({sortFit[species]:sortPop[species]})

    print(sortDict)
    sortFit = quicksort(sortFit)
    sortPop.clear() 

    for fitness in sortFit:
        sortPop.append(sortDict.get(fitness))

    print(sortFit)
    print(sortPop)

    for species in range (1,popSize+1):
        p.update({species:sortPop[species-1]})
        f.update({species:sortFit[species-1]})
        
    print (p)
    print (f)

parent = [ [1,1],[2,2],[4,4],[5,1] ] 

numCities = len(parent)

segment = random.sample(range(0,numCities),2)

if segment[0] < segment[1]:
    start = segment[0]
    end = segment [1]
else:
    start = segment[1]
    end = segment [0]

print ("duplicate segment" , parent[start:end])
child = [None]*numCities
child[start:end] = parent[start:end]
print ("child with duplicate segment", child)

if child[0] == None:
    child[0] = parent [0]
else:
    pass

fill = parent.copy()
for city in child:
    if city != None:
        fill.remove(city)
print ("cities to be filled" , fill)

fillindex = []
for count,city in enumerate(child):
    if city == None:
        fillindex.append(count)

print ("indexes to be filled" , fillindex)

random.shuffle(fillindex)
random.shuffle(fill)

for index,city in zip(fillindex,fill):
    child[index] = city

print ("new child", child)

