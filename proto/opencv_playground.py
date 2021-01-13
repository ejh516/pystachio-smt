#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
OPENCV PLAYGROUND

A testbed for manipulating images using Python's bindings to the OpenCV library.
"""

import sys
import cv2
import tifffile
import numpy as np
import matplotlib.pyplot as plt

def main_program():
    frames = tifffile.imread(sys.argv[1])
    target_frame = int(sys.argv[2])

    img_frame = cv2.cvtColor(frames[target_frame,:,:], cv2.COLOR_GRAY2BGR)
    filter_image = "none"
    disk_radius = 5
    threshold_tolerance = 0.75

    imshow(img_frame, "original image")

    # Get structural element (map with disk of ones in a square of 0s) [strel]
    disk_size = 2*disk_radius - 1
    disk_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(disk_size, disk_size))

    # Optionally apply gaussian filtering to the frame
    if filter_image == "gaussian":
        blurred_frame =cv2.GaussianBlur(img_frame,(3,3),0)
    else:
        blurred_frame = img_frame.copy()

    # Apply top-hat filtering [imtophat]
    tophatted_frame = cv2.morphologyEx(blurred_frame, cv2.MORPH_TOPHAT, disk_kernel)


    # Get b/w threshold value from the histogram
    hist_data = cv2.calcHist([tophatted_frame], [0], None, [256], [0,256])
    hist_data[0] = 0
#EJH#     plt.plot(hist_data)
#EJH#     plt.show()
    peak_width, peak_location = fwhm(hist_data)
    bw_threshold = int(peak_location + threshold_tolerance*peak_width)
    print("Peak width = ", peak_width)
    print("Peak location = ", peak_location)

    # Apply gaussian filter to the top-hatted image [fspecial, imfilter]
    blurred_tophatted_frame =cv2.GaussianBlur(tophatted_frame,(3,3),0)

    # Convert the filtered image to b/w [im2bw]
    bw_frame = cv2.threshold(blurred_tophatted_frame, bw_threshold, 255, cv2.THRESH_BINARY)[1]

    # "Open" the b/w image (in a morphological sense) [imopen]
    bw_opened = cv2.morphologyEx(bw_frame, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3)))

    # Fill holes ofsize 1 pixel in the resulting image [bwmorph]
    bw_filled = cv2.morphologyEx(bw_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))

    spot_locations = ultimate_erode(bw_filled[:,:,0])

    print("Spot localtions: ", spot_locations)

    ultimate_eroded = np.zeros([bw_filled.shape[0], bw_filled.shape[1]])
    for spot in spot_locations:
        ultimate_eroded[spot[0], spot[1]] = 1


    imshow(img_frame, "Final result", spots=spot_locations)

def fwhm(hist):
    x = np.linspace(0, 255, 256).astype(int)

    hist = hist / np.max(hist)
    N = hist.size-1

    lev50 = 0.5
    if hist[0] < lev50:
        centre_index = np.argmax(hist)
        Pol = +1
    else:
        centre_index = np.argmin(hist)
        Pol = -1

    extremum_val = x[centre_index]

    i = 1
    while np.sign(hist[i]-lev50) == np.sign(hist[i-1]-lev50):
        i += 1

    interp = (lev50-hist[i-1]) / (hist[i]-hist[i-1])
    lead_t = x[i-1] + interp*(x[i]-x[i-1])

    i = centre_index+1
    while (np.sign(hist[i]-lev50) == np.sign(hist[i-1]-lev50)) and (i <= N-1):
        i += 1

    if i != N:
        p_type  = 1
        interp  = (lev50-hist[i-1]) / (hist[i]-hist[i-1])
        trail_t = x[i-1] + interp*(x[i]-x[i-1])
        x_width = trail_t - lead_t
    else:
        p_type = 2
        trail_t = None
        x_width = None

    return (x_width, extremum_val)

def imshow(image, title, spots=[]):
    plt.title(title)
    plot = plt.imshow(image, vmin=0)
    plt.colorbar()
    if len(spots) > 0 :
        x,y = zip(*spots)
        plt.scatter(y,x)

    plt.show()

main_program()
