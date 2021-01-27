#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" PARAMETERS - Program parameters module

Description:
    parameters.py contains the Parameters class that holds all the program
    parameters, along with the default value for each parameter and routines
    for setting those parameters.

Contains:
    class Parameters

Author:
    Edward Higgins

Version: 0.2.0
"""

import sys

class Parameters:
    def __init__(self):
        self.verbose = True                 # Whether or not to display verbose console output
        self.c_split = "None"               # How the channels are split
        self.frames_to_track = 0            # How many frames to track after the laser has switched on
        self.start_channel = 0              # First channel to use
        self.end_channel = 0                # Last channel to use
        self.ALEX = 0                       # Whether or not this is an ALEX experiment
        self.use_cursor = False             # Whether or not to use the cursor
        self.determine_first_frames = False # Are there blank frames before the shutter opens?
        self.frame_avg_window = 5           # Number of frames to average over
        self.sat_pixel_val = 10**10         # Value representing saturated pixels

        self.task = ""
        self.verbose = True
        self.render_image = False
        self.seed_name = ""

        # Spots.find_in_frame
        self.filter_image = "none"
        self.disk_radius = 5
        self.bw_threshold_tolerance = 0.75

        self.max_displacement = 5
        # Initialise
        self.num_spots = 10
        self.Isingle = 10000
        self.BGmean = 500.0 # mean background pixel intensity
        self.BGstd = 120.0 # standard deviation of background pixels
        self.num_frames = 10
        self.resolution = [64, 64]
        self.bleach_time = 10 # in frames, if 0 then no bleaching
        self.diffusionCoeff = 1# um2/s
        self.nDiffPoints = 4 # number of MSD points to calculate diffusion const
        self.frameTime = 0.005 # seconds
        self.pixelSize = 0.120 # microns
        self.PSFwidth = 0.160/self.pixelSize # Sigma of a Gaussian, ~2/3 airy disk diameter

    def read(self, args):
        self.task = args[1]
        self.task = self.task.split(",")
        self.seed_name = args[2]
        for arg in args[3:]:
            key, value = arg.split("=", 2)
            try:
                print(f"Setting {key} to {value}")
                if type(getattr(self,key)) is type(0):
                    setattr(self, key, int(value))
                elif type(getattr(self,key)) is type(0.0):
                    setattr(self, key, float(value))
                elif type(getattr(self,key)) is type(True):
                    setattr(self, key, value == "True")
                else:
                    setattr(self, key, value)

            except NameError:
                sys.exit(f"ERROR: No such parameter '{key}'")

            if key == "pixelSize":
                self.PSFwidth = 0.160/self.pixelSize

            print(f"Using {key} = {getattr(self,key)}")
