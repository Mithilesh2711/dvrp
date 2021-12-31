import math
import random
from matplotlib import pyplot as plt  
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.numeric import normalize_axis_tuple
from numpy.lib.function_base import append
from llh import *

def plotTSP1(paths, points, num_iters=1):


    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])
    
    plt.plot(x, y, 'co')

    a = np.linspace(0.0, 1.0, num_iters)
    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x))/float(100)

    # Draw the older paths, if provided
    if num_iters >= 1:

        for i in range(0, num_iters):

            # Transform the old paths into a list of coordinates
            xi = []
            yi = []

            

            for j in range(len(paths[i])):
            	xi.append(points[paths[i][j]][0])
            	yi.append(points[paths[i][j]][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), 
                    head_width = a_scale, color = 'g', 
                    length_includes_head = True, ls = 'dashed',
                    width = 0.001/float(num_iters))
            for i in range(len(xi) - 1):
                plt.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                        head_width = a_scale, color = ((0.5, 0.1, 0.4, 1)), length_includes_head = True,
                        ls = 'dashed', width = 0.001/float(num_iters))
            plt.xlim(0, 1000)
            plt.ylim(0, 1000)
            plt.show()  