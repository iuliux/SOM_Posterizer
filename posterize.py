# -*- coding: utf-8 -*-

import sys
from PIL import Image
from src.som_segmentation import *
import math


def posterize(orig_file_name, n, do_plot=False, max_iters=3000, thresh=0.001):
    '''
    Posterizes (segments), displays and saves the result
    @n = number of colors (has to be a square number)
    '''
    # Check input
    nrootf = math.sqrt(n)
    if int(nrootf + 0.5) ** 2 != n:
        print 'Number of colors has to be a square'
        return
    nroot = int(nrootf)

    orig_img = Image.open(orig_file_name)
    orig_pixels = list(orig_img.getdata())
    orig_pixels = [(o[0]/255.0, o[1]/255.0, o[2]/255.0) for o in orig_pixels]

    print '-------------------------------------------'
    print 'Training SOM'
    WR, WG, WB = som_train(orig_pixels, nroot, max_iters, thresh)

    print '-------------------------------------------'
    print 'Posterizing the input image'
    segm_pixels = som_segmentation(orig_pixels, WR, WG, WB)

    print '-------------------------------------------'
    print 'Displaying posterized image'
    segm_img = Image.new('RGB', orig_img.size)
    segm_img.putdata(segm_pixels)
    segm_img.show()

    print '-------------------------------------------'
    print 'Saving posterized image'
    segm_img.save(orig_file_name.replace(".", "_sgm."))

    if do_plot:
        print '-------------------------------------------'
        print 'Plotting 3D representation of SOM'
        print '    Blue dots are image pixels'
        print '    Red dots are SOM centroids'
        plot_som_3d(orig_pixels, WR, WG, WB)


if __name__ == "__main__":
    posterize(sys.argv[1], int(sys.argv[2]))
