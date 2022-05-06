"""Travelling Salesman Problem without eligibility traces reinforcement learning algorithm"""

import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh import *
import time

no_of_heuristics = 7
eps = 0.9
r = 0.0001
steps = 20
ants = 20
alpha = 3
beta = 1
roe = 0.4
cycles = 20
mar = 2.0
gap = 20



def get_path(nodes):
    arr = np.arange(nodes)
    arr[1:] = np.random.permutation(arr[1:])
    return arr

def get_val(path, distances):
    val = 0
    
    path = [int(i) for i in path]
    i=0
    
    for j in range(1, len(path)):
        val = val + distances[path[i]][path[j]]
        i=j    
    
    return val + distances[i][len(path)]


def mutate(path):
    n = len(path)
    if n > 4:
        a = random.randrange(1,n-3)
        b = random.randrange(a+1,n-1)

        path = np.concatenate((path[0:a],np.random.permutation(path[a:b]),path[b:]))

    return path



def greedy_TSP(nodes, distances):
    b = [0]*nodes
    i=0
    b[0]=1

    path = [0]

    dist = 0
    m = 999999
    global k,p
    k=0
    p=0

    while k<nodes-1:
        m=9999
        for j in range(nodes):
            if b[j]==0 and distances[i][j] < m:
                m = distances[i][j]
                p = j
            
        i=p
        path.append(p)
        b[p]=1
        if m < 9999:
            dist += m

        k+=1  

    return dist, path.copy()



def tspwet(location, path, r=0.0001):
    no_of_nodes = len(path)
    print(path)
    nodes = [location[path[i]] for i in range(no_of_nodes)]

    array = path
    path = np.arange(no_of_nodes)

    distances = [[None] * (no_of_nodes+1) for i in range(no_of_nodes)]
    for i in range(no_of_nodes):
        distances[i][i] = 0
        for j in range(i+1, no_of_nodes):
            distances[i][j] = distances[j][i] = math.sqrt(math.pow(nodes[i][0] - nodes[j][0], 2.0) + math.pow(nodes[i][1] - nodes[j][1], 2.0))

    for i in range(no_of_nodes):
        distances[i][no_of_nodes] = math.sqrt(math.pow(location[0][0] - location[path[i]][0], 2.0) + math.pow(location[0][1] - location[path[i]][1], 2.0))
    
    f = [h1, h2, h3, h4, h5, h6, h7]

    h_val = [[0] for _ in range(no_of_heuristics)]

    greedy_val, greedy_path = greedy_TSP(no_of_nodes, distances)
      
    #min_val, min_path = greedy_TSP(no_of_nodes, distances)
    initial_path = path.copy()
    min_path = f[6](initial_path.copy(), distances)
    min_val = get_val(min_path.copy(), distances)
    initial_val = min_val
    
    min_path = greedy_path.copy()

    global npath, npath1

    ant_path = initial_path.copy()
    ant_val = get_val(ant_path.copy(), distances)

    edges_weight = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]
    edges_pheromone = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]

    


    for cycle in range(cycles):
        hpath = [[None]*steps for _ in range(ants)]
        pheromone_val = [None]*ants

        for ant in range(ants):
            hi = random.randrange(0, no_of_heuristics)
            if cycle == 0:
                npath = get_path(no_of_nodes)
            else:
                npath = ant_path.copy()

            ant_val = get_val(npath.copy(), distances)
            k=0
            for step in range(steps):
                hpath[ant][step] = hi
                val = get_val(npath.copy(), distances)
                global hf
                
                arr = [(edges_weight[hi][i]**alpha + edges_pheromone[hi][i]**beta) for i in range(no_of_heuristics)]

                
                hf = np.argmax(arr)
                npath1 = f[hf](npath.copy(), distances)


                val1 = get_val(npath1.copy(), distances)
                edges_weight[hi][hf] += 1/val1

                h_val[hf].append(val - val1)

                hi = hf

                if val1 < min_val :
                    min_path = npath1.copy()
                    min_val = get_val(min_path.copy(), distances)
                    #print(cycle,hf,min_val)
                    k=1
                    #plotTSP([min_path], nodes, 1)

                if step==steps-1:
                    if k==0:
                        pheromone_val[ant] =  r*(ant_val - val1 - cycle)
                    elif k==1 :
                        pheromone_val[ant] =  r*(ant_val - val1)
                    if ant==ants-1:
                        ant_path = min_path

                npath = npath1.copy()

        r *= 1.1

        #print(pheromone_val,"\n\n",edges_pheromone,"\n\n",edges_weight,"\n\n\n\n")
        for ant in range(ants):
            for i in range(steps-1):
                edges_pheromone[hpath[ant][i]][hpath[ant][i+1]] *= (1-roe)
                edges_pheromone[hpath[ant][i]][hpath[ant][i+1]] += pheromone_val[ant]

        
    print(initial_val, greedy_val , min_val)

    path = []

    for i in range(len(min_path)):
        path.append(array[min_path[i]])
    return path