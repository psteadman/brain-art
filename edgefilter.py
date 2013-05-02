#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sobel and canny filter

from pyminc.volumes.factory import *
from optparse import OptionParser
from scipy import ndimage
from skimage import filter

if __name__ == "__main__":

    usage = "usage: %prog [options] input.mnc output.mnc"
    description = "Edge detection - sobel filter"

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-s","--sigma", dest="sigma", 
        help="Canny filter sigma default: %default", 
        default=3, type='float')
    parser.add_option("--sobel", dest="sobel",
        help="Use sobel filter",
        default=False, action='store_true')
    parser.add_option("--nosobel", dest="sobel",
        help="Don't use sobel filter [default]",
        action='store_false')
    parser.add_option("--canny", dest="canny",
        help="Use canny filter [default]",
        default=True, action='store_true')
    parser.add_option("--nocanny", dest="canny",
        help="Don't use canny filter",
        action='store_false')
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Incorrect number of arguments")

    inim = volumeFromFile(args[0], dtype='ushort') #inim.data[::]
    #outim = volumeLikeFile(args[0], args[1])
    outim = volumeFromInstance(inim, args[1])

    # 3D Sobel filter (doesnt work always)
    if options.sobel:
        outim.data[::] = ndimage.generic_gradient_magnitude(inim.data, ndimage.sobel)
        options.canny = 0

    # 2D Canny filter
    # http://scipy-lectures.github.io/advanced/image_processing/auto_examples/plot_canny.html
    # canny(image, sigma=1.0, low_threshold=0.1, high_threshold=0.2, mask=None)
    if options.canny:
        for i in range(inim.sizes[0]):
            # print "SLICE: %i" % i
            t = inim.getHyperslab((i,0,0),(1,inim.sizes[1],inim.sizes[2]))
            t.shape = (inim.sizes[1], inim.sizes[2])
            c = filter.canny(t, sigma=6)
            outim.data[i::] = c
                      
    if options.canny or options.sobel:
        outim.writeFile()
        outim.closeVolume()
    else:
        print "No filter selected, no filtering performed."
    inim.closeVolume()
    

