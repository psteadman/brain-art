#!/usr/bin/env python

# right now just a sobel filter

from pyminc.volumes.factory import *
from optparse import OptionParser
from scipy import ndimage

if __name__ == "__main__":

    usage = "usage: %prog [options] input.mnc output.mnc"
    description = "Edge detection - sobel filter"

    parser = OptionParser(usage=usage, description=description)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Incorrect number of arguments")

    inim = volumeFromFile(args[0], dtype='ubyte') #inim.data[::]
    outim = volumeLikeFile(args[0], args[1])

    outim.data[::] = ndimage.generic_gradient_magnitude(inim.data, ndimage.sobel)
                      
    # write to file
    outim.writeFile()
    outim.closeVolume()
    inim.closeVolume()
