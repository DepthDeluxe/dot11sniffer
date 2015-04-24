import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# import something for database
import Image
import sys
import os.path

# SCALE: 5 ft = 32 pixels, 6.4 pix/ft
# NODE_SIZE: ~12x12 pixels

# credit Marchiori
def dist( x1, x2, y1, y2 ):
    d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
    if d==0.0:
        return 1.0
    else:
        return d

def main():

    # each index represents one node
    X = [361.5, 351, 352.5, 198]
    Y = [231, 432, 616.5, 687]

    # arbitrary testing counts
    count = [17, 6, 5, 10]
	
    sizeX = 902
    sizeY = 1032
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
		for sensor in range(0, num_sensors):
			d = dist(x,y,X[sensor], Y[sensor])**-2
			zi[y,x] += count[sensor] * (d/totaldist)
    scale = 5
    dpi = 32
    lena = Image.open('brki_w_nodes.png')
    figsize = scale*lena.size[0]/dpi, scale*lena.size[1]/dpi
    fig = plt.figure(figsize=figsize)
    #while figsize[0] > 12 or figsize[1] > 12:
#	figsize = figsize[0]/2, figsize[1]/2
    
    ax = fig.add_subplot(111)	
    ax.imshow(lena, interpolation="hermite", origin="lower")
	
    CS = ax.contour(xi, yi, zi, 15, linewidth=0.5, colors='k', alpha=0.3)
    CSF = ax.contour(xi, yi, zi, 15, cmap=colormap, alpha=0.3)

    cb = fig.colorbar(CSF)
    colorLabel = "Device Count Density"
    cb.set_label(colorLabel)
    
    ax.plot(X,Y,'o')
    ax.set_xlim(0, len(xi))
    ax.set_ylim(0, len(yi))
    ax.set_title("Device Count Density")

    fig.save_fig("grad.png", pad_inches=0)
    plt.close(fig)
			
    
main()
