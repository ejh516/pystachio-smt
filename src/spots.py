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
        print("find_in_frame is not yet implemented")
#EJH#         # This routine uses a bunch o' Matlab image processing calls.
#EJH#         # The equivelant Python library appears to be scikit-image.
#EJH#         # Below is the basic process, with the relevantk Matlab routines included
#EJH# 
#EJH#         # Convert frame to image format (i.e. 8 bit uints rather than floats) [mat2grey]
#EJH#         img_frame = frame.as_image()
#EJH#         display_image(img_frame)
#EJH# 
#EJH#         # Optionally apply gaussian filtering to the frame
#EJH#         if params.filter_image == "gaussian":
#EJH#             img_frame =cv2.GaussianBlur(img_frame,(3,3),0)
#EJH# 
#EJH#         # Get structural element (map with disk of ones in a square of 0s) [strel]
#EJH#         r = params.disk_radius
#EJH#         disk_size = 2*r - 1
#EJH#         disk_kernel = np.zeros([disk_size, disk_size]).astype(np.uint8)
#EJH#         for i in range(disk_size):
#EJH#             for i in range(disk_size):
#EJH#                 if (i-r+1)**2 + (j-r+1)**2 <= r**2:
#EJH#                 disk_kernel[i,j] = 1
#EJH# 
#EJH#         # Apply top-hat filtering [imtophat]
#EJH#         img_frame = cv2.tophat(img_frame, disk_kernel)
#EJH# 
#EJH#         # Get b/w threshold value from the histogram
#EJH#         hist_data = cv2.calcHist([img_frame], [0], None, [256], [0,256])
#EJH#         peak_width, peak_location = fwhm(hist_data)
#EJH#         bw_threshold = peak_location
#EJH# 
#EJH#         # Apply gaussian filter to the top-hatted image [fspecial, imfilter]
#EJH#         img_frame =cv2.GaussianBlur(img_frame,(3,3),0)
#EJH# 
#EJH#         # Convert the filtered image to b/w [im2bw]
#EJH#         bw_frame = cv2.threshold(img_frame, bw_threshold, 255, cv2.THRESH_BINARY)[1]
#EJH# 
#EJH#         # "Open" the b/w image (in a morphological sense) [imopen]
#EJH#         bw_opened = cv2.morphologyEx(bw_frame, cv2.MORPH_OPEN, disk_kernel)
#EJH# 
#EJH#         # Fill holes ofsize 1 pixel in the resulting image [bwmorph]
#EJH#         bw_filled = cv2.morphologyEx(bw_opened, cv2.MORPH_CLOSE, [[1]]) 


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
