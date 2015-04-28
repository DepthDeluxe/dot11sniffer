#!/usr/bin/env python
import math
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# import something for database
import Image
import sys
import os.path
from DBFinder import *

# SCALE: 5 ft = 32 pixels, 6.4 pix/ft
# NODE_SIZE: ~12x12 pixels

# in feet, credit Marchiori
def dist( x1, x2, y1, y2 ):
    d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
    if d==0.0:
        return 1.0
    else:
        return d

def plotLocations():
    f = DBFinder()
    l = f.findIds()

    d = f.pull_processed_block(l[-3])

    sizeX = 904
    sizeY = 1033
    numBins = 2.0
    xi = np.arange(0.0, float(sizeX))
    yi = np.arange(0.0, float(sizeY))
    locationsX = []
    locationsY = []
    for i in range(0, len(d)):
        locationsX += [d[i][0]]
        locationsY += [d[i][1]]

    # print "Computed contour, plotting"
    scale = 0.5
    dpi = 80

    # 80 dots/inch * 12 inches/foot * 5 feet/32 pixels = 150
    lena = Image.open("larrison-floorplan.png")  #Image.open('brki_w_nodes.png')
    figsize = scale*lena.size[0]/dpi, scale*lena.size[1]/dpi

    #print lena.size[0], lena.size[1]
    #print figsize
    fig = plt.figure(figsize=figsize)
    #while figsize[0] > 12 or figsize[1] > 12:
#       figsize = figsize[0]/2, figsize[1]/2

    ax = fig.add_subplot(111)
    ax.imshow(lena)

    #CS = ax.contour(xi, yi, zi, 15, linewidth=0.5, colors='k', alpha=0.3)
    #CSF = ax.contour(xi, yi, zi, 15, cmap=plt.cm.jet, alpha=0.3)

    #cb = fig.colorbar(CSF)
    #colorLabel = "Device Count Density"
    #cb.set_label(colorLabel)

    ax.plot(locationsX, locationsY,'o')
    ax.set_xlim(0, len(xi))
    ax.set_ylim(0, len(yi))
    #fig.axes.get_xaxis().set_visible(False)
    #fig.axes.get_yaxis().set_visible(False)
    ax.set_title("Muenster Cheese")
    fig.savefig("test.png", pad_inches=0)
    plt.close(fig)

def plotCounts():

    # each index represents one node
    X = [361.5, 351, 352.5, 198]
    Y = [231, 432, 616.5, 687]

    # arbitrary testing counts
    count = [86, 76, 45, 65]
    sizeX = 904
    sizeY = 1033
    xi = np.arange(0.0, float(sizeX))
    yi = np.arange(0.0, float(sizeY))
    zi = np.zeros([len(yi), len(xi)], float)

    num_sensors = len(X)

    # Interpolate using Shepard's Method
    for x in range(0, len(xi)):
        for y in range(0, len(yi)):
            totaldist = 0
            for sensor in range(0, num_sensors):
                totaldist += (dist(x,y,X[sensor], Y[sensor])**-2)
                    #print totaldist, " totaldist"
            for sensor in range(0, num_sensors):
                d = dist(x,y,X[sensor], Y[sensor])**-2
                    #print "dist is ", d, "weight is ", d/totaldist
                zi[y,x] += count[sensor] * (d/totaldist)

    #print x, "/", len(xi)
    #print zi[y,x], "weighted value at ", x, y
    print("Computed contour, plotting")
    scale = 0.5
    dpi = 80
    # 80 dots/inch * 12 inches/foot * 5 feet/32 pixels = 150
    lena = Image.open('brki_w_nodes.png')
    figsize = scale*lena.size[0]/dpi, scale*lena.size[1]/dpi
    print(lena.size[0], lena.size[1])
    print(figsize)
    fig = plt.figure(figsize=figsize)
    #while figsize[0] > 12 or figsize[1] > 12:
#   figsize = figsize[0]/2, figsize[1]/2

    ax = fig.add_subplot(111)
    ax.imshow(lena, origin="upper")

    CS = ax.contour(xi, yi, zi, 15, linewidth=0.5, colors='k', alpha=0.3)
    CSF = ax.contour(xi, yi, zi, 15, cmap=plt.cm.jet, alpha=0.3)

    cb = fig.colorbar(CSF)
    #colorLabel = "Device Count Density"
    #cb.set_label(colorLabel)

    ax.plot(X,Y,'o')
    ax.set_xlim(0, len(xi))
    ax.set_ylim(0, len(yi))
    ax.set_title("Device Count Density")

    fig.savefig("grad.png", pad_inches=0)
    plt.close(fig)

if __name__ == "__main__":
    plotLocations()
