import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class ImageMaker:
    def __init__(self,img):
        plt.axis('off')
        plt.imshow(mpimg.imread(img))

    def addPoint(self,x,y):
        plt.scatter([x],[y])

    def saveImage(self):
        plt.savefig('/var/www/html/images/test.png')
