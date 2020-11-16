#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""

class Spot:
    def __init__(self, x,y):
        self.pos = [x,y]

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

