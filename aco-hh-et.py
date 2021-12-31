import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh import *
import time
from backup import plotTSP1

no_of_nodes = 50
no_of_heuristics = 7
eps = 0.9
r = 0.0001
steps = 20
ants = 20
alpha = 3
beta = 1
roe = 0.2
cycles = 20
mar = 2.0
gap = 20
etd = 0.5



def get_path(nodes):
    return np.random.permutation(nodes)

def get_val(path, distances):
    val = 0
    
    path = [int(i) for i in path]
    i=0
    
    for j in range(1, len(path)):
        val = val + distances[path[i]][path[j]]
        i=j    
    
    return val


def mutate(path):
    n = len(path)
    a = random.randrange(1,n-4)
    b = random.randrange(a+1,n-2)

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



if __name__ == '__main__':
    nodes = [(random.randrange(10, 900), random.randrange(10, 900)) for _ in range(no_of_nodes)]
    print(nodes)
    distances = [[None] * no_of_nodes for _ in range(no_of_nodes)]
    for i in range(no_of_nodes):
        distances[i][i] = 0
        for j in range(i+1, no_of_nodes):
            distances[i][j] = distances[j][i] = math.sqrt(math.pow(nodes[i][0] - nodes[j][0], 2.0) + math.pow(nodes[i][1] - nodes[j][1], 2.0))

    
    f = [h1, h2, h3, h4, h5, h6, h7]

    h_val = [[0] for _ in range(no_of_heuristics)]

    greedy_val, greedy_path = greedy_TSP(no_of_nodes, distances)
      
    #min_val, min_path = greedy_TSP(no_of_nodes, distances)
    initial_path = get_path(no_of_nodes)
    min_path = f[6](initial_path.copy(), distances)
    min_val = get_val(min_path.copy(), distances)
    print(min_val, greedy_val)
    min_path = greedy_path.copy()

    global npath, npath1

    ant_path = initial_path.copy()
    ant_val = get_val(ant_path.copy(), distances)

    edges_weight = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]
    edges_pheromone = [[1]*no_of_heuristics for _ in range(no_of_heuristics)]

    


    for cycle in range(cycles):
        hpath = [[None]*steps for _ in range(ants)]
        pheromone_val = [None]*ants
        e = [[[0]*no_of_heuristics]*no_of_heuristics]*ants

        for ant in range(ants):
            hi = random.randrange(0, no_of_heuristics)
            if cycle == 0:
                npath = get_path(no_of_nodes)
            else:
                if ant == 0:
                    npath = ant_path.copy()
                else :
                    npath = mutate(ant_path.copy())

            ant_val = get_val(npath.copy(), distances)
            k=0
            for step in range(steps):
                hpath[ant][step] = hi
                val = get_val(npath.copy(), distances)
                global hf
                
                arr = [(edges_weight[hi][i]**alpha + edges_pheromone[hi][i]**beta) for i in range(no_of_heuristics)]

                
                hf = np.argmax(arr)
                npath1 = f[hf](npath.copy(), distances)


                for i in range(no_of_heuristics):
                    for j in range(no_of_heuristics):
                        e[ant][i][j] = e[ant][i][j]*etd

                e[ant][hi][hf] += 1

                val1 = get_val(npath1.copy(), distances)
                edges_weight[hi][hf] += r*(val-val1-(cycle+1)*(ant+1)*(step+1)*0.01)

                h_val[hf].append(val - val1)

                hi = hf

                if val1 < min_val :
                    min_path = npath1.copy()
                    min_val = get_val(min_path.copy(), distances)
                    print(cycle,hf,min_val)
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
                edges_pheromone[hpath[ant][i]][hpath[ant][i+1]] += e[ant][hpath[ant][i]][hpath[ant][i+1]]*pheromone_val[ant]

        
    #print(get_val(npath1.copy(), distances))
    print(get_val(min_path.copy(), distances))

    paths = [initial_path, greedy_path, min_path]    
    plotTSP1(paths, nodes, 3)

    plt.plot(np.arange(0,len(h_val[0]),gap), h_val[0][0:len(h_val[0]):gap], color = 'r' , label = "line 1", linestyle="-.")
    plt.plot(np.arange(0,len(h_val[1]),gap), h_val[1][0:len(h_val[1]):gap], color = 'b' , label = "line 2", linestyle="--")
    plt.plot(np.arange(0,len(h_val[2]),gap), h_val[2][0:len(h_val[2]):gap], color = 'g' , label = "line 3", linestyle=":")
    plt.plot(np.arange(0,len(h_val[3]),gap), h_val[3][0:len(h_val[3]):gap], color = 'c' , label = "line 4", linestyle="-")
    plt.plot(np.arange(0,len(h_val[4]),gap), h_val[4][0:len(h_val[4]):gap], color = 'm' , label = "line 5", linestyle=":")
    plt.plot(np.arange(0,len(h_val[5]),gap), h_val[5][0:len(h_val[5]):gap], color = 'y' , label = "line 6", linestyle=":")
    plt.plot(np.arange(0,len(h_val[6]),gap), h_val[6][0:len(h_val[6]):gap], color = 'k' , label = "line 7", linestyle="-")
    plt.legend()
    plt.show()

   

    
