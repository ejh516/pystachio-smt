#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""

class Spots:
    def __init__(self, num_spots):
        self.num_spots = num_spots
        self.positions = np.zeros(num_spots, 2)
        self.clipping = [False] * num_spots
        self.bg_intensity = np.zeros(num_spots) 
        self.spot_intensity =  np.zeros(num_spots)
        self.centre_intensity =  np.zeros(num_spots)
        self.width = np.zeros(num_spots,2)
        self.first_frame = [0]*num_spots
        self.traj_num = [0] * num_spots
        self.snr = np.zeros(num_spots,2)
        self.laser_on_frame = 0


    def link():
        return False

    def find_centre():
        return False

    def distance_from(self, candidate):
        dx = self.pos[x] - candidate.pos[x]
        dy = self.pos[y] - candidate.pos[y]
        return sqrt(dx**2 + dy**2)

def find_spots():
    return False

def merge_coincedent_spots(candidate_spots, min_distance):
    good_spots = []
    for candidate in candidate_spots
        is_good_spot = True
        for good_spot in good_spots
            if good_spot.distance_from(candidate) < min_distance:
            is_good_spot = False
            break
        if is_good_spot:
            good_spots.append(candidate)

    return good_spots

