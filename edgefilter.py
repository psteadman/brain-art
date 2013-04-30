#!/usr/bin/env python
# -*- coding: utf-8 -*-

# right now just a sobel filter

from pyminc.volumes.factory import *
from optparse import OptionParser
from scipy import ndimage
#my mac
# from scikits.image.filter import canny
#github install (on MICe linux)
from skimage import filter

if __name__ == "__main__":

    usage = "usage: %prog [options] input.mnc output.mnc"
    description = "Edge detection - sobel filter"

    parser = OptionParser(usage=usage, description=description)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Incorrect number of arguments")

    inim = volumeFromFile(args[0], dtype='ushort') #inim.data[::]
    #outim = volumeLikeFile(args[0], args[1])
    outim = volumeFromInstance(inim, args[1])

	# 3D Sobel filter (doesnt work always)
    # outim.data[::] = ndimage.generic_gradient_magnitude(inim.data, ndimage.sobel)
    
    # http://scipy-lectures.github.io/advanced/image_processing/auto_examples/plot_canny.html
    # http://scipy-lectures.github.io/advanced/image_processing/
    # http://pythongeek.blogspot.ca/2012/06/canny-edge-detection.html
    # http://cyroforge.wordpress.com/2012/01/21/canny-edge-detection/
    # 2D Canny filter
    # canny(image, sigma=1.0, low_threshold=0.1, high_threshold=0.2, mask=None)
	for i in range(inim.sizes[0]):
		print "SLICE: %i" % i
		t = inim.getHyperslab((i,0,0),(1,inim.sizes[1],inim.sizes[2]))
		t.shape = (inim.sizes[1], inim.sizes[2])
		c = filter.canny(t, sigma=6)
		outim.data[i::] = c
                      
    # write to file
    outim.writeFile()
    outim.closeVolume()
    inim.closeVolume()
    

