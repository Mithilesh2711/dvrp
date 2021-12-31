import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append

def distance(a,b):
	return math.sqrt(math.pow(a[0] - b[0], 2.0) + math.pow(a[1] - b[1], 2.0))

def get_val(paths, location):
	d = 0
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

def g1(path1, path2, demand, capacity, location):
    if (path1[2] != 0 and path2[2] != 0) or (path1[1] + path2[1]>capacity):
        return path1, path2

    
    n = len(path1[0])
    m = len(path2[0])

    if m==0 or n==0:
        return path1, path2

    if path1[1] + path2[1] < capacity and distance(location[path1[0][n-1]], location[path2[0][0]]) < distance(location[path1[0][n-1]], location[0]) + distance(location[path2[0][0]], location[0]):
        
        if path2[2] == 0:
            p1 = np.concatenate((path1[0], path2[0]))
            dem = path1[1] + path2[1]
            path1 = []
            path1.append(p1) 
            path1.append(dem)
            path1.append(0)
            return path1, []

        elif path1[2] == 0:
            p1 = np.concatenate((path2[0], path1[0]))
            dem = path1[1] + path2[1]
            path1 = []
            path1.append(p1) 
            path1.append(dem)
            path1.append(0)
            return path1, []

    else:
        return path1, path2    



def g2(path1, path2, demand, capacity, location):
    path1 = list(path1)
    path2 = list(path2)

        
    p = path1[2]
    q = path2[2]

    b = []


    for i in range(p, len(path1[0])):
        if demand[path1[0][i]] + path2[1] < capacity:
            for j in range(q, len(path2[0])):
                if j!=len(path2[0])-1:

                    if distance(location[path1[0][i]], location[path2[0][j]]) + distance(location[path1[0][i]], location[path2[0][j+1]]) + distance(location[path1[0][np.maximum(0,i-1)]], location[path1[0][np.minimum(len(path1[0])-1, i+1)]]) < distance(location[path2[0][j]], location[path2[0][j+1]]) + distance(location[path1[0][np.maximum(0,i-1)]], location[path1[0][i]]) + distance(location[path1[0][np.minimum(len(path1[0])-1,i+1)]], location[path1[0][i]]):
                        path2[0] = np.concatenate((path2[0][0:j+1], [path1[0][i]], path2[0][j+1:]))
                        path2[1] += demand[path1[0][i]]
                        path1[1] -= demand[path1[0][i]]
                        b.append(path1[0][i])
                        break
    
    for i in range(len(b)):
        path1[0] = list(path1[0])
        path2[0] = list(path2[0])
        path1[0].remove(b[i])


    
    b = []
            
    for i in range(q, len(path2[0])):
        if demand[path2[0][i]] + path1[1] < capacity:
            for j in range(p, len(path1[0])):
                if j!=len(path1[0])-1:
                    if distance(location[path2[0][i]], location[path1[0][j]]) + distance(location[path2[0][i]], location[path1[0][j+1]]) + distance(location[path2[0][np.maximum(0,i-1)]], location[path2[0][np.minimum(len(path2[0])-1, i+1)]]) < distance(location[path1[0][j]], location[path1[0][j+1]]) + distance(location[path2[0][np.maximum(0,i-1)]], location[path2[0][i]]) + distance(location[path2[0][np.minimum(len(path2[0])-1,i+1)]], location[path2[0][i]]):
                        path1[0] = np.concatenate((path1[0][0:j+1], [path2[0][i]], path1[0][j+1:]))
                        path1[1] += demand[path2[0][i]]
                        path2[1] -= demand[path2[0][i]]
                        b.append(path2[0][i])
                        break
            

    for i in range(len(b)):
        path1[0] = list(path1[0])
        path2[0] = list(path2[0])
        path2[0].remove(b[i])

    return path1, path2



def g3(path1, path2, demand, capacity, location):
    p = path1[2]
    q = path2[2]
    z=1



    while z==1:
        z = 0
        w=0
        path1[0] = np.array(path1[0], dtype=np.int)
        path2[0] = np.array(path2[0], dtype=np.int)

        for i in range(p, len(path1[0])):
            d1=0
            z=0
            w=0
            for j in range(i+w+1, len(path1[0])):
                if j >= len(path1[0]):
                    break
                for k in range(i, j):
                    d1+=demand[path1[0][k]]

                for l in range(q, len(path2[0])):
                    d2=0
                    for m in range(l+1, len(path2[0])):
                        for n in range(l,m):
                            d2+=demand[path2[0][n]]

                        if path1[1] - d1 + d2 < capacity and path2[1] -d2 +d1 < capacity :
                            tp1 = path1[0]
                            tp2 = path2[0]
                            p1 = np.concatenate((tp1[0:i], tp2[l:m], tp1[j:]))
                            tp2 = np.concatenate((tp2[0:l], tp1[i:j], tp2[m:]))
                            tp1 = p1
                            if get_val([tp1,tp2], location) < get_val([path1[0], path2[0]], location):

                                path1[0] = tp1
                                path2[0] = tp2
                                path1[1] = path1[1] - d1 + d2
                                path2[1] = path2[1] -d2 +d1
                                z = 1
                                w += 1

                        if z==1:
                            break

                    if z==1:
                        break



    
    path1[0] = list(path1[0])
    path2[0] = list(path2[0])
    return path1, path2
