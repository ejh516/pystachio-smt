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
        print(f"    Frame size: {frame.shape}")
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
        print("    Peak width = ", peak_width)
        print("    Peak location = ", peak_location)

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

    def index_first(self):

        self.traj_num = list(range(self.num_spots))

    def link(self, prev_spots, params):
        print("Linking trajectories:")
        distances = self.distance_from(prev_spots)

        assigned = []
        neighbours = np.argsort(distances[:,:], axis=1)
        paired_spots = []
        next_trajectory = max(prev_spots.traj_num)+1
        for i in range(self.num_spots):
            for j in range(prev_spots.num_spots):
                neighbour = neighbours[i,j]
                if (distances[i,neighbour] < params.max_displacement):
                    if neighbour in paired_spots:
                        continue
                    else:
                        paired_spots.append(neighbour)
                        print(f"    Extending trajectory {prev_spots.traj_num[neighbour]}")
                        self.traj_num[i] = prev_spots.traj_num[neighbour]
                else:
                    self.traj_num[i] = next_trajectory
                    next_trajectory += 1
                    print(f"    Creating trajectory {self.traj_num[i]}")
                break

            if self.traj_num[i] == -1:
                sys.exit(f"Unable to find a match for spot {i}, frame {self.frame}")


    def get_spot_intensities(self, frame):
        for i in range(self.num_spots):
            x = int(self.positions[i,0])
            y = int(self.positions[i,1])
            #Create a tmp array with the centre of the spot in the centre
            tmp = frame[x-8:x+9,y-8:y+9] # ED: is this right? or should be other way round?
            spotmask = np.zeros(tmp.shape)
            cv2.circle(spotmask, (8,8), 5, 1, -1)
            bgintensity = np.mean(tmp[spotmask==0])
            tmp = tmp - bgintensity
            intensity = np.sum(tmp[spotmask==1])
            print(intensity)
            self.spot_intensity[i] = intensity
            
#EJH#     def link():
#EJH#         return False
#EJH# 
#EJH#     def find_centre():
#EJH#         return False
