"""Dynamic Vehicle Routing Problem with eligibility traces reinforcement learning algorithm"""

import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh import *
import time
from preprocessing1 import *
from tsp import *
from llh2 import g1, g2, g3
from tsp1 import tsp1

filename = 'c100D.txt' 
time_slices = 40
cutoff = 0.5

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




def distance(a,b):
    return math.sqrt(math.pow(a[0] - b[0], 2.0) + math.pow(a[1] - b[1], 2.0))




def calc_centre(paths):
    for i in range(len(paths)):
        if not len(paths[i]):
            continue
        x = 0
        y = 0
        k=0
        for j in paths[i][2][np.maximum( 0, paths[i][3]-1): ] :
            x += location[j][0]
            y += location[j][1]
            k += 1

        paths[i][0] = (x/k, y/k)

        d=0
        for j in range(len(paths[i][2])):
            d+=demand[paths[i][2][j]]

        paths[i][1] = d

    return paths.copy()


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))



def merge(paths, node, location, demand, capacity):
    
    
    d = 1000000
    avg_dis = 10
    k = 0
    for i in range(len(paths)):
        if not len(paths[i]):
            continue

        if d > distance(location[paths[i][2][-1]], location[node]) and paths[i][1] + demand[node] < capacity :
            d = distance(location[paths[i][2][-1]], location[node])
            k = i 

        

    if len(paths) > (sum(demand)/capacity)* cutoff:
        return paths, node

    elif d < distance(location[node], location[0]) :
        paths[k][2] = list(paths[k][2])
        paths[k][2].append(node)
        paths[k][1] += demand[node]
        paths[k][5] = 1
        paths[k][6] = 1


        return paths, 0

    else :
        paths.append([location[node], demand[node], [node], 0, 0, 1, 1])
        return paths, 0




if __name__ == '__main__':
    requests, vehicles, load_time, window, capacity, available, demand, location = get_data(filename)
    req_pool = []
    timestep = window/time_slices

    location[0] = location[0]
    unserved_req = []

    paths = []
    paths1 = []


    k=-1
    a = []

    visits = 0

    print("vr:",sum(demand)/capacity)

    for i in range(1, len(available)):
        if k == int(available[i]//timestep):
            a.append(i)

        else:
            k = int(available[i]//timestep)
            if len(a):
                req_pool.append(a)
            a = []
            a.append(i)
    
    if len(a):
        req_pool.append(a)

    c = 0
    time = 0
    while time <= window * cutoff:
        time += timestep
        if c>=1:
            k=0
            for i in range(len(paths)):

                if not len(paths[i]):
                    continue


                k=1
                t = timestep
                if len(paths[i]):
                    j = paths[i][3]

                while t>0:

                    if paths[i][4] == 0:
                        j = paths[i][3]

                        if j >= len(paths[i][2]):
                            paths[i][5]=0
                            break

                        if paths[i][3] == 0:
                            paths[i][4] = distance(location[paths[i][2][j]],location[0]) + load_time


                        else:
                            paths[i][4] = load_time + distance(location[paths[i][2][j]], location[paths[i][2][j-1]])

                        paths[i][3] += 1

                    if t>=paths[i][4]:
                        if j==len(paths[i][2])-1:
                            paths[i][5] = 0
                        t -= paths[i][4]
                        paths[i][4] = 0
                        visits +=1 

                        

                    else:
                        paths[i][4] -= t
                        t = 0



        for j in range(len(req_pool[c])):
            paths, n = merge(paths, req_pool[c][j], location, demand, capacity)
            if n!=0:
                unserved_req.append(n)
            
        c+=1


        paths = calc_centre(paths)

            
        for i in range(len(paths)):
            if not len(paths[i]):
                continue
            if len(paths[i][2][paths[i][3]:])>2 and paths[i][6]==1:
                if paths[i][3] == 0:
                    tp = tsp(location, np.concatenate(([0], paths[i][2][paths[i][3]:])))
                    paths[i][2][paths[i][3]:] = tp[1:]
                    paths[i][6]=0

                else:   
                    tp = tsp(location, paths[i][2][paths[i][3]-1:])
                    paths[i][2][paths[i][3]:] = tp[1:]
                    paths[i][6]=0

        tpaths = []
        b = []

        for i in unserved_req:
            d = 1000000
            p=-1
            q=0
            for j in range(len(paths)):
                if not len(paths[j]):
                    continue

                if distance(location[i], location[paths[j][2][-1]]) < d and paths[j][1]+demand[i] < capacity :
                    d = distance(location[i], location[paths[j][2][-1]])
                    p = j
            if p!=-1:
                b.append(i)
                paths[p][2] = list(paths[p][2])
                paths[p][2].append(i)
                paths[p][1] += demand[i]

        for i in b:
            unserved_req.remove(i)

        for i in range(len(paths)):
            if len(paths[i]):
                tpaths.append(paths[i][2])

        d1 = get_val(tpaths, location)

        


        global a1,b1
        a1 = []
        b1 = []
        for i in range(len(paths)):
            for j in range(i+1, len(paths)):
                if not len(paths[i]) or not len(paths[j]):
                    continue
                a1 = [paths[i][2],paths[i][1],paths[i][3]]
                b1 = [paths[j][2],paths[j][1],paths[j][3]]


                #paths = tsp1(paths, location, demand, capacity)

                d = get_val([a1[0],b1[0]], location)
                d1 = 1000000
                a1, b1 = g1(a1, b1, demand, capacity, location)
                
                while d < d1 and len(a1) and len(b1):
                    a1, b1 = g2(a1, b1, demand, capacity, location)
                    d1 = d
                    d = get_val([a1[0],b1[0]], location)

                if len(a1) and len(b1):
                    for _ in range(100):
                        a1, b1 = g3(a1, b1, demand, capacity, location)


                if len(a1):
                    paths[i][2] = a1[0]
                    paths[i][1] = a1[1]
                    paths[i][3] = a1[2]

                else:
                    paths[i] = []

                if len(b1):
                    paths[j][2] = b1[0]
                    paths[j][1] = b1[1]
                    paths[j][3] = b1[2]

                else:
                    paths[j] = []




    if time > window * cutoff:

        for i in range(len(paths)):
            if not len(paths[i]):
                continue
            if len(paths[i][2][paths[i][3]:])>2:
                if paths[i][3] == 0:
                    tp = tsp(location, np.concatenate(([0], paths[i][2][paths[i][3]:])))
                    paths[i][2][paths[i][3]:] = tp[1:]
                    paths[i][6]=0

                else:   
                    tp = tsp(location, paths[i][2][paths[i][3]-1:])
                    paths[i][2][paths[i][3]:] = tp[1:]
                    paths[i][6]=0

        print(unserved_req)
        while c<len(req_pool):
            unserved_req = unserved_req + req_pool[c]
            c+=1

        
        unserved_req = tsp(location, np.concatenate(([0], unserved_req)))
        unserved_req = unserved_req[1:]

        path = []
        d=0

        for i in range(len(unserved_req)):
            if d+demand[unserved_req[i]] < capacity:
                d += demand[unserved_req[i]]
                path.append(unserved_req[i])

            else:
                
                paths1.append([path, d, 0])
                d = demand[unserved_req[i]]
                path = [unserved_req[i]]

        if len(path):
            paths1.append([path, d, 0])
        
        """for i in range(len(unserved_req)):
                                    deg = angle_between(location[unserved_req[i]], location[0])
                                    #deg = distance(location[unserved_req[i]], location[0])
                                    unserved_req[i] = (deg, unserved_req[i])
                        
                                unserved_req.sort()
                        
                                k=0
                                path = []
                                b = [0]*len(unserved_req)
                                p=1
                        
                                while p==1:
                                    p=0
                                    k=0
                                    path = []
                                    for i in range(len(unserved_req)):
                                        if(k + demand[unserved_req[i][1]]) < capacity and b[i]==0:
                                            p=1
                                            path.append(unserved_req[i][1])
                                            k += demand[unserved_req[i][1]]
                                            b[i]=1
                                    paths1.append([path, d, 0])
                                    
                        
                                
                                for i in range(len(paths1)):
                                    if len(paths1[i][0])>2 :
                                        tp = tsp(location, np.concatenate(([0], paths1[i][0])))
                                        paths1[i][0] = tp[1:]"""



        for i in range(len(paths1)):
            for j in range(i+1, len(paths1)):
                if not len(paths1[i]) or not len(paths1[j]):
                    continue

                a1 = paths1[i]
                b1 = paths1[j]
                d = get_val([a1[0],b1[0]], location)
                d1 = 1000000
                a1, b1 = g1(a1, b1, demand, capacity, location)
                
                while d < d1 and len(a1) and len(b1):
                    a1, b1 = g2(a1, b1, demand, capacity, location)
                    d1 = d
                    d = get_val([a1[0],b1[0]], location)

                if len(a1) and len(b1):
                    for _ in range(100):
                        a1, b1 = g3(a1, b1, demand, capacity, location)

                paths1[i] = a1
                paths1[j] = b1


    d = 0

    for i in range(len(paths1)):
        if len(paths1[i]) and len(paths1[i][0])>2 :
            tp = tsp(location, np.concatenate(([0], paths1[i][0])))
            paths1[i][0] = tp[1:]

    for i in range(len(paths1)):
        if len(paths1[i]):
            paths1[i] = paths1[i][0]

    plotTSP(paths1, location, len(paths1))
    paths2 = []

    d=0
    for j in range(len(paths1[0])):
        if j==0:
            d+=load_time + distance(location[paths1[0][j]], location[0])
        else:
            d += load_time + distance(location[paths1[0][j]], location[paths1[0][j-1]])


    print("Time = ", d+window)



    for i in range(len(paths)):
        if len(paths[i]):
            paths2 += [paths[i][2]]
            paths1 += [paths[i][2]]

    paths = paths1
    plotTSP(paths2, location, len(paths2))

    d=0
    for i in range(len(paths)):
        if not len(paths[i]):
            continue
        for j in range(len(paths[i])):
            if len(paths[i])==1:
                d+=2*distance(location[paths[i][0]], location[0])

            elif j==0:
                d+=distance(location[paths[i][0]], location[0])

            elif j==len(paths[i])-1:
                d+=distance(location[paths[i][j]], location[paths[i][j-1]]) + distance(location[paths[i][j]], location[0])

            else:
                d+=distance(location[paths[i][j]], location[paths[i][j-1]])


    print("distance=",d)

    
    paths1 = []
    for i in range(len(paths)):
        c = 0
        for j in paths[i]:
            c+=demand[j]

        print(paths[i],c,"\n|\n|\n")

    plotTSP(paths, location, len(paths))



    