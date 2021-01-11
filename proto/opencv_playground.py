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

def main_program():
    frames = tifffile.imread(sys.argv[1])

    img_frame = cv2.cvtColor(frames[0,:,:], cv2.COLOR_GRAY2BGR)
    filter_image = "none"
    disk_radius = 5

    imshow(img_frame, "original image")

    # Optionally apply gaussian filtering to the frame
    if filter_image == "gaussian":
        img_frame =cv2.GaussianBlur(img_frame,(3,3),0)
        imshow(img_frame, "filtered image")

    # Get structural element (map with disk of ones in a square of 0s) [strel]
    disk_size = 2*disk_radius - 1
    disk_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(disk_size, disk_size))

    # Apply top-hat filtering [imtophat]
    img_frame = cv2.morphologyEx(img_frame, cv2.MORPH_TOPHAT, disk_kernel)

    imshow(img_frame, "top-hatted image")

    # Get b/w threshold value from the histogram
    hist_data = cv2.calcHist([img_frame], [0], None, [256], [0,256])
    peak_width, peak_location = fwhm(hist_data)
    bw_threshold = peak_location*0.8
    print("Peak width = ", peak_width)
    print("Peak location = ", peak_location)

    # Apply gaussian filter to the top-hatted image [fspecial, imfilter]
    img_frame =cv2.GaussianBlur(img_frame,(3,3),0)
    imshow(img_frame, "blurred, top-hatted image")

    # Convert the filtered image to b/w [im2bw]
    bw_frame = cv2.threshold(img_frame, bw_threshold, 255, cv2.THRESH_BINARY)[1]
    imshow(bw_frame, "BW image")

    # "Open" the b/w image (in a morphological sense) [imopen]
#EJH#     bw_opened = cv2.morphologyEx(bw_frame, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3)))
#EJH#     imshow(bw_opened, "BW image opened")

    # Fill holes ofsize 1 pixel in the resulting image [bwmorph]
    bw_filled = cv2.morphologyEx(bw_frame, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
    imshow(bw_filled, "BW image filled")

    eroded = ultimate_erode(bw_filled, cv2.getStructuringElement(cv2.MORPH_RECT, (2,2)))

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

def imshow(image, title):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ultimate_erode(orig_image, mask):
    image = orig_image.copy()
    ult_erode = orig_image.copy()
    ult_erode[:,:,:] = 0
    eroded_image= cv2.erode(image, mask)

    spots = []
    while(np.sum(eroded_image - image) != 0):
        imshow(cv2.hconcat([orig_image, image, eroded_image, ult_erode]), "Ultimate eroded image")
        for i in range(1,63):
            for j in range(1,63):
                if image[i,j].any() and not eroded_image[i-1:i+1,j-1:j+1].any():
                    ult_erode[i,j] += np.ones(3).astype(np.uint8) * 255

        image = eroded_image
        eroded_image = cv2.erode(image, mask)

    imshow(cv2.hconcat([orig_image, ult_erode]), "Ultimate eroded image")

main_program()
