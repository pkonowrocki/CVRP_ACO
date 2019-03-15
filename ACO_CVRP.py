import math
import RegExService
import random
import numpy
from functools import reduce
import sys
import getopt

alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
fileName = "E-n22-k4.txt"
iterations = 1000
ants = 22

def generateGraph():
    capacityLimit, graph, demand, optimalValue = RegExService.getData(fileName)
    vertices = list(graph.keys())
    vertices.remove(1)

    edges = { (min(a,b),max(a,b)) : numpy.sqrt((graph[a][0]-graph[b][0])**2 + (graph[a][1]-graph[b][1])**2) for a in graph.keys() for b in graph.keys()}
    feromones = { (min(a,b),max(a,b)) : 1 for a in graph.keys() for b in graph.keys() if a!=b }
    
    return vertices, edges, capacityLimit, demand, feromones, optimalValue

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, feromones):
    solution = list()

    while(len(vertices)!=0):
        path = list()
        city = numpy.random.choice(vertices)
        capacity = capacityLimit - demand[city]
        path.append(city)
        vertices.remove(city)
        while(len(vertices)!=0):
            probabilities = list(map(lambda x: ((feromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta), vertices))
            probabilities = probabilities/numpy.sum(probabilities)
            
            city = numpy.random.choice(vertices, p=probabilities)
            capacity = capacity - demand[city]

            if(capacity>0):
                path.append(city)
                vertices.remove(city)
            else:
                break
        solution.append(path)
    return solution

def rateSolution(solution, edges):
    s = 0
    for i in solution:
        a = 1
        for j in i:
            b = j
            s = s + edges[(min(a,b), max(a,b))]
            a = b
        b = 1
        s = s + edges[(min(a,b), max(a,b))]
    return s

def updateFeromone(feromones, solutions, bestSolution):
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
    feromones = { k : (ro + th/Lavg)*v for (k,v) in feromones.items() }
    solutions.sort(key = lambda x: x[1])
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    else:
        bestSolution = solutions[0]
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    return bestSolution

def main():
    bestSolution = None
    vertices, edges, capacityLimit, demand, feromones, optimalValue = generateGraph()
    
    for i in range(iterations):
        solutions = list()
        for _ in range(ants):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, feromones)
            solutions.append((solution, rateSolution(solution, edges)))
        bestSolution = updateFeromone(feromones, solutions, bestSolution)
        print(str(i)+":\t"+str(int(bestSolution[1]))+"\t"+str(optimalValue))
    return bestSolution

if __name__ == "__main__":
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "f:a:b:s:r:t:i:n:",["fileName=",
        "alpha=","beta=","sigma=","rho=","theta=","iterations=","numberOfAnts="])
    except getopt.GetoptError:
        print("""use: python ACO_CVRP.py 
            -f <fileName> 
            -a <alpha> 
            -b <beta> 
            -s <sigma> 
            -r <rho> 
            -t <theta>
            -i <iterations>
            -n <numberOfAnts>

            Default values:
            fileName: E-n22-k4.txt
            alpha: 80
            beta: 5
            sigma: 3
            rho: 0.8
            theta: 80
            iterations: 1000
            number of ants: 22""")
        sys.exit(2)
    for opt,arg in opts:
        if(opt in ("-a", "--alpha")):
            alfa = float(arg)
        elif(opt in ("-b", "--beta")):
            beta = float(arg)
        elif(opt in ("-s", "--sigma")):
            sigm = float(arg)
        elif(opt in ("-r", "--rho")):
            ro = float(arg)
        elif(opt in ("-t", "--theta")):
            th = float(arg)
        elif(opt in ("-f", "--fileName", "--file")):
            fileName = str(arg)
        elif(opt in ("-i", "--iterations")):
            iterations = int(arg)
        elif(opt in ("-n", "--numberOfAnts")):
            ants = int(arg)

    print("file name:\t"+str(fileName)+
"\nalpha:\t"+str(alfa)+
"\nbeta:\t"+str(beta)+
"\nsigma:\t"+str(sigm)+
"\nrho:\t"+str(ro)+
"\ntheta:\t"+str(th)+
"\niterations:\t"+str(iterations)+
"\nnumber of ants:\t"+str(ants))

    solution = main()

    print("Solution: "+str(solution))
    if(fileName=="E-n22-k4.txt"):
        optimalSolution = ([[18, 21, 19, 16, 13], [17, 20, 22, 15], [14, 12, 5, 4, 9, 11], [10, 8, 6, 3, 2, 7]], 375)
        print("Optimal solution: "+str(optimalSolution))