#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Parameters
"""

class Parameters:
    def __init__(self):
        self.verbose = True                 # Whether or not to display verbose console output
        self.c_split = "None"               # How the channels are split
        self.frames_to_track = 0            # How many frames to track after the laser has switched on
        self.start_channel = 0              # First channel to use
        self.end_channel = 0                # Last channel to use
        self.ALEX = 1                       # Whether or not this is an ALEX experiment
        self.use_cursor = False             # Whether or not to use the cursor
        self.determine_first_frames = False # Are there blank frames before the shutter opens?
        self.frame_avg_window = 5           # Number of frames to average over
        self.sat_pixel_val = 10**10         # Value representing saturated pixels
        self.disk_radius = 5                # Radius of disk for finding spots in the image
