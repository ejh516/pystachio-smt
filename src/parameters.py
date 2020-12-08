#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Parameters
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
        self.disk_radius = 5                # Radius of disk for finding spots in the image

        self.task = ""
        self.verbose = True
        self.filename = ""

        # Initialise
        self.num_spots = 10
        self.Isingle = 10000
        self.BGmean = 500 # mean background pixel intensity
        self.BGstd = 120 # standard deviation of background pixels
        self.num_frames = 30
        self.resolution = [64, 64]
        self.bleach_time = 10 # in frames, if 0 then no bleaching
        self.diffusionCoeff = 1# um2/s
        self.nDiffPoints = 4 # number of MSD points to calculate diffusion const
        self.frameTime = 0.005 # seconds
        self.pixelSize = 0.120 # microns
        self.PSFwidth = 0.160/self.pixelSize # Sigma of a Gaussian, ~2/3 airy disk diameter

    def read(self, args):
        for arg in args[1:]:
            key, value = arg.split("=", 2)
            try:
                print(f"Setting {key} to {value}")
                if type(getattr(self,key)) == type(0):
                    setattr(self, key, int(value))
                else:
                    setattr(self, key, value)

            except NameError:
                sys.exit(f"ERROR: No such parameter '{key}'")

        self.task = self.task.split(",")
