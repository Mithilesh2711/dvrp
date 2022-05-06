"""Travelling Salesman Problem with eligibility traces reinforcement learning algorithm"""

import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh3 import g1, g2, g3
import time

global no_of_nodes 

no_of_heuristics = 3
eps = 0.9
r = 0.0001
steps = 20
ants = 20
alpha = 0
beta = 1
roe = 0.4
cycles = 50
mar = 2.0
gap = 20
etd = 0.5

def distance(a,b):
    return math.sqrt(math.pow(a[0] - b[0], 2.0) + math.pow(a[1] - b[1], 2.0))





def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2))

def get_val(paths, location):
    d = 0
    p = []
    for i in range(len(paths)):
        if len(paths[i]):
            p.append(paths[i][0])

    paths = p

    for i in range(len(paths)):
        for j in range(len(paths[i])):
            if len(paths[i])==1:
                d+=2*distance(location[paths[i][0]], location[0])

            elif j==0:
                d+=distance(location[paths[i][0]], location[0])

            elif j==len(paths[i])-1:
                d+=distance(location[paths[i][j]], location[paths[i][j-1]]) + distance(location[paths[i][j]], location[0])

            else:
                d+=distance(location[paths[i][j]], location[paths[i][j-1]])

    return d


def mutate(paths, demand, capacity, location):
    a = []


    for i in range(len(paths)):
        if len(paths[i]):
            paths[i][0] = list(paths[i][0])
            for j in range(len(paths[i][0])):
                a.append(paths[i][0][j])

    k = random.randrange(0,9)

    if k%3==0:
        for i in range(len(a)):
            a[i] = (distance(location[a[i]], location[0]), a[i])

        a.sort()
        for i in range(len(a)):
            a[i] = a[i][1]

    elif k%3==1:
        for i in range(len(a)):
            a[i] = (angle_between(location[a[i]], location[0]), a[i])

        a.sort()
        for i in range(len(a)):
            a[i] = a[i][1]


    


    p = random.randrange(2,len(a)-4)
    q = random.randrange(p+1, len(a)-2)
    a = np.concatenate((a[0:p], np.random.permutation(a[p:q]), a[q:]))

    


    k=0
    path = []
    paths = []
    for i in a:
        if k+demand[i]<capacity:
            k+=demand[i]
            path.append(i)

        else:
            paths.append([path, k, 0])
            path = [i]
            k = demand[i]

    if len(path):
        paths.append([path, k, 0])

    return paths.copy()





def tsp1(paths, location, demand, capacity, r=0.01):
    
    f = [g1, g2, g3]

    h_val = [[0] for _ in range(no_of_heuristics)]

      
    #min_val, min_path = greedy_TSP(no_of_nodes, distances)
    initial_path = paths.copy()
    min_path = initial_path.copy()
    min_val = get_val(min_path.copy(), location)

    global npath, npath1

    ant_path = initial_path.copy()
    ant_val = get_val(ant_path.copy(), location)

    edges_weight = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]
    edges_pheromone = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]

    


    for cycle in range(cycles):
        hpath = [[None]*steps for _ in range(ants)]
        pheromone_val = [None]*ants
        e = [[[0]*no_of_heuristics]*no_of_heuristics]*ants

        for ant in range(ants):
            hi = random.randrange(0, no_of_heuristics)
            if cycle == 0:
                npath = initial_path.copy()
            else:
                if ant == 0:
                    npath = ant_path.copy()
                else :
                    npath = mutate(ant_path.copy(), demand, capacity, location)
             

            ant_val = get_val(npath.copy(), location)
            k=0
            for step in range(steps):
                hpath[ant][step] = hi
                val = get_val(npath.copy(), location)
                global hf
                
                arr = [(edges_weight[hi][i]**alpha + edges_pheromone[hi][i]**beta) for i in range(no_of_heuristics)]

                npath1 = npath
                d = get_val(npath, location)
                hf = np.argmax(arr)
                for i in range(len(npath)):
                    for j in range(i+1, len(npath)):
                        if len(npath[i]) and len(npath[j]):
                            npath1[i], npath1[j] = f[hf](npath[i], npath[j], demand, capacity, location)

                d1 = get_val(npath1.copy(), location)

                for i in range(no_of_heuristics):
                    for j in range(no_of_heuristics):
                        e[ant][i][j] = e[ant][i][j]*etd

                e[ant][hi][hf] += 1


                edges_weight[hi][hf] += r*(d-d1)

                h_val[hf].append(d - d1)

                hi = hf

                print(d, d1)


                if d1 < min_val :
                    min_path = npath1.copy()
                    min_val = get_val(min_path.copy(), location)
                    print(cycle,hf,min_val)
                    k=1
                    #plotTSP([min_path], nodes, 1)

                if step==steps-1:
                    if k==0:
                        pheromone_val[ant] =  r*(ant_val - d1 - cycle)
                    elif k==1 :
                        pheromone_val[ant] =  r*(ant_val - d1)
                    if ant==ants-1:
                        ant_path = min_path.copy()

                npath = npath1.copy()

        r *= 1.1

        #print(pheromone_val,"\n\n",edges_pheromone,"\n\n",edges_weight,"\n\n\n\n")
        for ant in range(ants):
            for i in range(steps-1):
                edges_pheromone[hpath[ant][i]][hpath[ant][i+1]] *= (1-roe)
                edges_pheromone[hpath[ant][i]][hpath[ant][i+1]] += e[ant][hpath[ant][i]][hpath[ant][i+1]]*pheromone_val[ant]

        
    #print(get_val(npath1.copy(), distances))
    print(get_val(min_path.copy(), location))
    return min_path.copy(), min_val


if __name__ == '__main__':
    p1 = np.arange(1, 25)
    p2 = np.arange(25, 51)

    location = [(30, 40), (37, 52), (49, 49), (52, 64), (20, 26), (40, 30), (21, 47), (17, 63), (31, 62), (52, 33), (51, 21), (42, 41), (31, 32), (5, 25), (12, 42), (36, 16), (52, 41), (27, 23), (17, 33), (13, 13), (57, 58), (62, 42), (42, 57), (16, 57), (8, 52), (7, 38), (27, 68), (30, 48), (43, 67), (58, 48), (58, 27), (37, 69), (38, 46), (46, 10), (61, 33), (62, 63), (63, 69), (32, 22), (45, 35), (59, 15), (5, 6), (10, 17), (21, 10), (5, 64), (30, 15), (39, 10), (32, 39), (25, 32), (25, 55), (48, 28), (56, 37)]
    demand = [0, 7, 30, 16, 9, 21, 15, 19, 23, 11, 5, 19, 29, 23, 21, 10, 15, 3, 41, 9, 28, 8, 8, 16, 10, 28, 7, 15, 14, 6, 19, 11, 12, 23, 26, 17, 6, 9, 15, 14, 7, 27, 13, 11, 16, 10, 5, 25, 17, 18, 10]
    capacity = 160
    paths = mutate([[p1, 0, 0], [p2,0,0]],  demand, capacity, location)

    print(tsp1(paths.copy(), location, demand, capacity))
