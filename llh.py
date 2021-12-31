import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh import *
global no_of_nodes, N

def get_path(nodes):
    return np.random.permutation(nodes)

def get_val(path, distances):
    val = 0
    
    path = [int(i) for i in path]
    i=0
    
    for j in range(1, len(path)):
        val = val + distances[path[i]][path[j]]
        i=j    
    
    return val + distances[i][len(path)]



def Reverse_Segment(path, a, b):
    path = np.concatenate((path[0:a],path[b:a-1:-1],path[b+1:]))
    return path.copy()  

def Make_2_Opt_Move(path, i, j):
    no_of_nodes = len(path)
    return Reverse_Segment(path, (i+1) % no_of_nodes, j)

def Gain_From_2_Opt(X1, X2, Y1, Y2, distance):
    del_Length = distance[X1][X2] + distance[Y1][Y2]
    add_Length = distance[X1][Y1] + distance[X2][Y2]
    result = del_Length - add_Length
    return result



def plotTSP(paths, points, num_iters):

    x = []
    y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    a = np.linspace(0.0, 1.0, num_iters+1)
    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x))/float(100)

    # Draw the older paths, if provided
    if num_iters >= 1:

        for i in range(0, num_iters):

            # Transform the old paths into a list of coordinates
            xi = [points[0][0]]
            yi = [points[0][1]]

            for j in range(len(paths[i])):
                xi.append(points[paths[i][j]][0])
                yi.append(points[paths[i][j]][1])


            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), 
                    head_width = a_scale, color = 'g', 
                    length_includes_head = True, ls = 'dashed',
                    width = 0.001/float(num_iters))
            for j in range(len(xi) - 1):
                plt.arrow(xi[j], yi[j], (xi[j+1] - xi[j]), (yi[j+1] - yi[j]),
                        head_width = a_scale, color = (a[i], a[-1*i], a[i], 1), length_includes_head = True,
                        ls = 'dashed', width = 0.001/float(num_iters))
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.show()  




    
 #------------------------------------------------Heuristics---------------------------------------------------------------------------------

def h1(path, distances):
    no_of_nodes = len(path)
    h7(path, distances)
    locallyOptimal = False
    global besti
    global bestj
    while not locallyOptimal:
	    locallyOptimal = True
	    bestMove = 0

	    for counter_1 in range(1,no_of_nodes-3):
		    i = counter_1
		    X1 = path[i]
		    X2 = path[(i+1) % no_of_nodes]

		    if i == 0:
		        counter_2_Limit = no_of_nodes-2
		    else:
		        counter_2_Limit = no_of_nodes-1

		    for counter_2 in range(i+2, counter_2_Limit):
			    j = counter_2
			    Y1 = path[j]
			    Y2 = path[(j+1) % no_of_nodes]

			    gainExpected = Gain_From_2_Opt(X1, X2, Y1, Y2, distances)

			    if gainExpected > bestMove:
			        bestMove = gainExpected
			        besti = i
			        bestj = j
			        locallyOptimal = False

	    if not locallyOptimal:
		    path = Make_2_Opt_Move(path, besti, bestj)
		    

	    if locallyOptimal:
	    	return path

    
def h2(path, distances):
    a=0
    b=0
    flag = False

    no_of_nodes = len(path)
    p=0

    while not flag and p<30:
        p+=1
        flag = True
        for i in range(1,no_of_nodes):
            for j in range(i+2, no_of_nodes):
                if i==0:
                    a = distances[path[j]][path[i+1]] - distances[path[i]][path[i+1]]
                else :
                    a = distances[path[i-1]][path[j]] + distances[path[j]][path[i+1]] - distances[path[i]][path[i+1]] - distances[path[i-1]][path[i]]

                if j==no_of_nodes-1:
                    b = distances[path[i]][path[j-1]] - distances[path[j]][path[j-1]]

                else :
                    b = distances[path[j-1]][path[i]] + distances[path[i]][path[j+1]] - distances[path[j-1]][path[j]] - distances[path[j]][path[j+1]]    


                if (a+b) < 0:
                    t = path[i]
                    path[i] = path[j]
                    path[j] = t
                    flag = False

    return path



def h3(path, distances):
    a=0
    b=0
    flag = False

    no_of_nodes = len(path)

    while not flag:
        flag = True
        for i in range(1,no_of_nodes):
            for j in range(i+2, no_of_nodes):
                if i==0:
                    a = -1 * distances[path[i]][path[i+1]]
                else :
                    a = distances[path[i-1]][path[i+1]] - distances[path[i]][path[i+1]] - distances[path[i-1]][path[i]]

                if j==no_of_nodes-1:
                    b = distances[path[j]][path[i]]
                else :
                    b = distances[path[j]][path[i]] + distances[path[i]][path[j+1]] - distances[path[j]][path[j+1]]    


                if (a+b) < 0:
                    if i==0 and j==no_of_nodes-1:
                        path = np.concatenate((path[i+1:j+1], [path[i]]))

                    elif i==0:
                        path = np.concatenate((path[i+1:j+1], [path[i]], path[j+1:]))

                    elif j==no_of_nodes-1:
                        path = np.concatenate((path[0:i], path[i+1:j+1], [path[i]]))

                    else :
                        path = np.concatenate((path[0:i], path[i+1:j+1], [path[i]], path[j+1:]))
                    flag = False

    return path


def h4(path,distances) :
    n= len(path)
    k=0
    while k < 100 and n> 5:
        i = random.randrange(1,len(path)-4)
        j = random.randrange(1,len(path)-2)

        a = distances[path[i-1]][path[j]] + distances[path[j]][path[i+1]] - distances[path[i]][path[i+1]] - distances[path[i-1]][path[i]]
        b = distances[path[j-1]][path[i]] + distances[path[i]][path[j+1]] - distances[path[j-1]][path[j]] - distances[path[j]][path[j+1]]

        if (a+b) < 0:
            t=path[i]
            path[i]=path[j]
            path[j]=t 

        k = k+1

    return path


def h5(path, distances) :
    k=0
    n= len(path)
    while k<100 and n>5: 
        a = random.randrange(1,len(path)-3)
        b = random.randrange(a+1,len(path)-1)
        path1 = np.concatenate((path[0:a],path[b:a-1:-1],path[b+1:]))
        if get_val(path1.copy(), distances) < get_val(path.copy(), distances):
            path = path1.copy()

        k = k+1    

    return path.copy()


def h6(path, distances) :
    n= len(path)
    if n>3:
        a = random.randrange(1,len(path)-2)

        t=path[a]
        path[a]=path[a+1]
        path[a+1]=t

    return path    


def h7(path, distances) :
    k=0
    m=1000000
    no_of_nodes = len(path)
    for i in range(1, no_of_nodes):
        if m > distances[path[0]][path[i]]:
            m=distances[path[0]][path[i]]
            k=i

    t = path[k]
    path[k] = path[no_of_nodes-1]
    path[no_of_nodes-1] = t

    return path 
#---------------------------------------------------------------Paths Heuristics-----------------------------------------------------------------------


    
