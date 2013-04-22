#!/usr/bin/python

# right no a sobel filter

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

    # dx = ndimage.sobel(inim.data, 0)  # x derivative
    # dy = ndimage.sobel(inim.data, 1)  # y derivative
    # dz = ndimage.sobel(inim.data, 2)  # z derivative
    # outim.data[::] = numpy.sqrt(dx*dx+dy*dy+dz*dz)  # magnitude
    # one line for the above 4 lines
    outim.data[::] = ndimage.generic_gradient_magnitude(inim.data, ndimage.sobel)
                      
    # write to file
    outim.writeFile()
    outim.closeVolume()
    inim.closeVolume()
