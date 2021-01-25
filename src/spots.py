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
import cv2
import matplotlib.pyplot as plt
import sys

from images import display_image
from algorithms import *

class Spots:
    def __init__(self, num_spots=0, frame=0):
        self.num_spots = num_spots
        if num_spots > 0:
            self.positions = np.zeros([num_spots, 2])
            self.clipping = [False] * num_spots
            self.bg_intensity = np.zeros(num_spots) 
            self.spot_intensity =  np.zeros(num_spots)
            self.centre_intensity =  np.zeros(num_spots)
            self.width = np.zeros([num_spots,2])
            self.frame = frame
            self.traj_num = [-1] * self.num_spots
            self.snr = np.zeros([num_spots,2])
            self.laser_on_frame = 0
        else:
            self.frame = frame
            self.initialised = False


    def set_positions(self, positions):
        self.num_spots = len(positions)
        self.positions = np.zeros([self.num_spots, 2])
        self.clipping = [False] * self.num_spots
        self.bg_intensity = np.zeros(self.num_spots) 
        self.spot_intensity =  np.zeros(self.num_spots)
        self.centre_intensity =  np.zeros(self.num_spots)
        self.width = np.zeros([self.num_spots,2])
        self.traj_num = [-1] * self.num_spots
        self.snr = np.zeros([self.num_spots,2])

        for i in range(self.num_spots):
            self.positions[i,:] = positions[i]



    def find_in_frame(self, frame, params):
        img_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Get structural element (map with disk of ones in a square of 0s) [strel]
        disk_size = 2*params.disk_radius - 1
        disk_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(disk_size, disk_size))

        # Optionally apply gaussian filtering to the frame
        if params.filter_image == "gaussian":
            blurred_frame =cv2.GaussianBlur(img_frame,(3,3),0)
        else:
            blurred_frame = img_frame.copy()

        # Apply top-hat filtering [imtophat]
        tophatted_frame = cv2.morphologyEx(blurred_frame, cv2.MORPH_TOPHAT, disk_kernel)


        # Get b/w threshold value from the histogram
        hist_data = cv2.calcHist([tophatted_frame], [0], None, [256], [0,256])
        hist_data[0] = 0

        peak_width, peak_location = fwhm(hist_data)
        bw_threshold = int(peak_location + params.bw_threshold_tolerance*peak_width)

        # Apply gaussian filter to the top-hatted image [fspecial, imfilter]
        blurred_tophatted_frame =cv2.GaussianBlur(tophatted_frame,(3,3),0)

        # Convert the filtered image to b/w [im2bw]
        bw_frame = cv2.threshold(blurred_tophatted_frame, bw_threshold, 255, cv2.THRESH_BINARY)[1]

        # "Open" the b/w image (in a morphological sense) [imopen]
        bw_opened = cv2.morphologyEx(bw_frame, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3)))

        # Fill holes ofsize 1 pixel in the resulting image [bwmorph]
        bw_filled = cv2.morphologyEx(bw_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))

        spot_locations = ultimate_erode(bw_filled[:,:,0], frame)

        self.set_positions(spot_locations)

    def merge_coincident_candidates(self):
        new_positions = []
        skip = []
        for i in range(self.num_spots):
            tmp_positions = [self.positions[i,:]]
            if i in skip:
                continue

            for j in range(i+1,self.num_spots):
                if np.linalg.norm(self.positions[i,:] - self.positions[j,:]) < 2:
                    skip.append(j)
                    tmp_positions.append(self.positions[j,:])

            p = [0,0]
            for pos in tmp_positions:
                p[0] += pos[0]
                p[1] += pos[1]
            p[0] = p[0] / len(tmp_positions)
            p[1] = p[1] / len(tmp_positions)

            new_positions.append(p)

        self.set_positions(new_positions)

    def distance_from(self, other):
        distances = np.zeros([self.num_spots, other.num_spots])

        for i in range(self.num_spots):
            for j in range(other.num_spots):
                distances[i,j] = np.linalg.norm(self.positions[i,:] - other.positions[j,:])

        return distances
