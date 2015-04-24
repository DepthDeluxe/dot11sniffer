# Image testing file, the following are notes from
#                   effbot.org/imagingbook/image.htm
# PLT.Image methods we might use
#   im.getbbox() => 4-tuple or None
#   im.getbands() => tuple of strings
#   im.getdata() => sequence
#   im.load() => pixel access object that can be used to read and modify
#                pixels. Access object behaves like 2d array, access like:
#                       pix = im.load(); pix[x,y] = value;
#   im.paste(color,box): pass a 4-tuple into box defining the pixel corners
#                   of the region to color
#   im.show() => saves image to temporary PPM file, calls xv utility to 
#                   display it
#   im.save( outfile, [format,] options ): save img under given filename.
#                   format determined from filename extension if possible.

from PIL import Image

img = Image.new( 'RGB', (255,255), "black") # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):   # for every pixel:
    for j in range(img.size[1]):
	pixels[i,j] = (i, j, 100) # set the color accordingly

img.save( "img_test.ppm" );
