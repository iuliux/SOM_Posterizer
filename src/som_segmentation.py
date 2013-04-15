#!/usr/bin/python
# -*- coding: utf-8 -*-

from learning_rate import *
from radius import *
from neighbourhood import *

import numpy as np


def euclidian(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)


def som_train(img_pixels, n, max_iters=3000, thresh=0.001):
    '''
    Learns the SOM and returns resulted n^2 cluster centroids, as 3 1D arrays:
        (R, G, B)
    @img_pixels = list of tuples (r, g, b), with values in [0, 1]
    @n = width of square neurons map (sqrt of total number of resulting colors)
    '''
    img_len = len(img_pixels)

    # Randomly init neurons' color
    WR = np.random.sample((1, n ** 2))
    WG = np.random.sample((1, n ** 2))
    WB = np.random.sample((1, n ** 2))

    delta = 99999
    deltas = []
    it = 0

    while it < max_iters and delta >= thresh:
        pick = np.random.randint(0, img_len)
        pick_rgb = img_pixels[pick]

        # Computes all distances and picks the closest
        dists = euclidian(WR, WG, WB, *pick_rgb)
        choosen = dists.argmin()

        # Restore matrix indeces from liniar index
        choosen_x = choosen % n
        choosen_y = choosen / n

        rad = radius(it, max_iters, n, n)
        eta = learning_rate(it, max_iters)
        # Generate neighbouring mask used to only influence the neighbours
        neigh = neighbourhood(choosen_x, choosen_y, rad, n, n)

        # Compute deltas
        deltaR = eta * neigh * (pick_rgb[0] - WR)
        deltaG = eta * neigh * (pick_rgb[1] - WG)
        deltaB = eta * neigh * (pick_rgb[2] - WB)

        # Update weights
        WR += deltaR
        WG += deltaG
        WB += deltaB

        # Convergence check
        delta = np.sum(np.abs(deltaR)) + np.sum(np.abs(deltaG)) + \
            np.sum(np.abs(deltaB))
        deltas.append(delta)

        it += 1
    return (WR, WG, WB)


def som_segmentation(orig_pixels, WR, WG, WB):
    '''
    Generates a posterized (segmented) version of input image, based on SOM
    given as @WR, @WG, @WB
    @orig_pixels = list of tuples (r, g, b), with values in [0, 1]
    @WR, @WG, @WB = red, green and blue coordinates of SOM neurons
    '''
    segm_pixels = orig_pixels[:]

    for i, px in enumerate(orig_pixels):
        dists = euclidian(WR, WG, WB, *px)
        choosen = dists.argmin()

        o = (WR[0, choosen], WG[0, choosen], WB[0, choosen])
        segm_pixels[i] = \
            (int(o[0] * 255.0), int(o[1] * 255.0), int(o[2] * 255.0))

    return segm_pixels


def plot_som_3d(img_pixels, WR, WG, WB, reducer=50):
    '''
    Plots a 3D representation of the input image and the SOM centroids
    @reduce = the fraction of input image pixels to plot (for @reduce = 1 all
        pixels will be plotted, but this may be very slow)
    '''
    import pylab as pl
    import mpl_toolkits.mplot3d.axes3d as p3

    px_r = [p[0] for i, p in enumerate(img_pixels) if i % reducer == 0]
    px_g = [p[1] for i, p in enumerate(img_pixels) if i % reducer == 0]
    px_b = [p[2] for i, p in enumerate(img_pixels) if i % reducer == 0]

    fig = pl.figure()
    ax = p3.Axes3D(fig)
    ax.scatter3D(px_r, px_g, px_b, s=8)
    ax.scatter3D(WR, WG, WB, c='r', s=30)
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    pl.show()


def plot_deltas(deltas, smooth=10):
    '''
    @smooth = how many delta values to group and average (used for a smoother
        graphic). @smooth = 1 means no smoothing
    '''
    ds = np.array([np.mean(deltas[i-smooth+1:i+1])
                   for i in xrange(smooth, len(deltas), smooth)])
    x = np.arange(0, ds.size, 1)
    pl.plot(x, ds)
    pl.show()
