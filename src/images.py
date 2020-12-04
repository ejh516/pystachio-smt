#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
IMAGES
"""

import tifffile
import sys

import numpy as np

class Image():
    def __init__(self, filename="", data=[]):
        self.filename = filename
        self.data = data

    def read(self, filename):
        self.filename = filename
        self.data = tifffile.imread(filename)
        self.num_frames = self.data.shape[0]
        self.resolution = (self.data.shape[1], self.data.shape[2])
        self.num_pixels = self.data.shape[1] * self.data.shape[2]
        print(f"Read in {filename}")
        print(f"num_frames: {self.num_frames}")
        print(f"resolution: {self.resolution}")

    def write(self):
        tifffile.imsave(self.filename, self.data)

    def frame(self, iframe):
        return self.frames[iframe]

    def rotate(self, angle):
        if angle % 270 == 0:
            for frame in self.frames:
                np.rot90(frame, angle//270)

        else:
            sys.exit("ERROR: Images can only be rotated by multiples of 90°")

    def calculate_frame_average(self, params):
        self.frame_average = []
        if params.ALEX:
            sys.exit("ERROR: ALEX support not yet implemented")
        else:
            self.frame_average = np.sum(self.data[:,:,:], axis=(1,2)) / self.num_pixels

