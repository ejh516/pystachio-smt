#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import numpy as np
from images import display_image

class Spots:
    def __init__(self, num_spots):
        self.num_spots = num_spots
        self.positions = np.zeros([num_spots, 2])
        self.clipping = [False] * num_spots
        self.bg_intensity = np.zeros(num_spots) 
        self.spot_intensity =  np.zeros(num_spots)
        self.centre_intensity =  np.zeros(num_spots)
        self.width = np.zeros([num_spots,2])
        self.frame = 0
        self.traj_num = np.array(range(num_spots))
        self.snr = np.zeros([num_spots,2])
        self.laser_on_frame = 0

    def find_in_frame(self, frame):
        # This routine uses a bunch o' Matlab image processing calls.
        # The equivelant Python library appears to be scikit-image.
        # Below is the basic process, with the relevantk Matlab routines included

        # Convert frame to image format (i.e. 8 bit uints rather than floats) [mat2grey]
        img_frame = frame.as_image()
        display_image(img_frame)

        # get structural element (map with disk of ones in a square of 0s) [strel]


        # Apply top-hat filtering [imtophat]

        # Get x & y histograms of the image data [imhist]

        # Apply gaussian filter to the top-hatted image [fspecial, imfilter]

        # Convert the filtered image to b/w [im2bw]

        # "Open" the b/w image (in a morphological sense) [imopen]

        # Morph the resulting image some other way [bwmorph]

        # Ultimate erode the image [bwulterode]


#EJH#     def link():
#EJH#         return False
#EJH# 
#EJH#     def find_centre():
#EJH#         return False
#EJH# 
#EJH#     def distance_from(self, candidate):
#EJH#         dx = self.pos[x] - candidate.pos[x]
#EJH#         dy = self.pos[y] - candidate.pos[y]
#EJH#         return sqrt(dx**2 + dy**2)
#EJH# 
#EJH# def find_spots():
#EJH#     return False
#EJH# 
#EJH# def merge_coincedent_spots(candidate_spots, min_distance):
#EJH#     good_spots = []
#EJH#     for candidate in candidate_spots
#EJH#         is_good_spot = True
#EJH#         for good_spot in good_spots
#EJH#             if good_spot.distance_from(candidate) < min_distance:
#EJH#             is_good_spot = False
#EJH#             break
#EJH#         if is_good_spot:
#EJH#             good_spots.append(candidate)
#EJH# 
#EJH#     return good_spots
