#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" IMAGES - Image access and manipulation module

Description:
    images.py contains the ImageData class for storing datasets of multiple
    frames, along with routines for manipulating the images.

Contains:
    class    ImageData
    function display_image

Author:
    Edward Higgins

Version: 0.2.0
"""

import sys
import os

import cv2 as cv
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import tifffile


class ImageData:
    def __init__(self):
        self.exists = False

    def __getitem__(self, index):
        frame = ImageData()
        frame.initialise(1, self.frame_size)
        frame.pixel_data[0, :, :] = self.pixel_data[index, :, :]
        return frame

    def __setitem__(self, index, value):
        if value.__class__ == "ImageData":
            self.pixel_data[index, :, :] = value.pixel_data[0, :, :]
        else:
            self.pixel_data[index, :, :] = value

    def initialise(self, num_frames, frame_size):
        self.num_frames = num_frames
        self.frame_size = frame_size
        self.num_pixels = frame_size[0] * frame_size[1]

        self.pixel_data = np.zeros([num_frames, frame_size[1], frame_size[0]])

        self.exists = True

    def as_image(self, frame=0, drop_dim=True):

        if drop_dim:
            img = self.pixel_data.astype(np.uint16)[frame, :, :]
        else:
            img = self.pixel_data.astype(np.uint16)
        return img

    def read(self, params):
        # Determine the filename from the seedname
        if os.path.isfile(params.seed_name):
            filename = params.seed_name
        elif os.path.isfile(params.seed_name + ".tif"):
            filename = params.seed_name + ".tif"
        else:
            sys.abort(f"Unable to find file matching '{seed_name}'")

        # Read in the file and get the data size
        pixel_data = tifffile.imread(filename)

        if params.num_frames:
            self.num_frames = min(params.num_frames, pixel_data.shape[0])
        else:
            self.num_frames = pixel_data.shape[0]

        if params.split_frame:
            self.frame_size = (pixel_data.shape[2]//2, pixel_data.shape[1])
        else:
            self.frame_size = (pixel_data.shape[2], pixel_data.shape[1])

        self.num_pixels = self.frame_size[0] * self.frame_size[1]

        # Store the frames in a list
        self.pixel_data = pixel_data[:self.num_frames, :self.frame_size[1], :self.frame_size[0]]

        self.determine_first_frame()

        self.exists = True

    def write(self, params):
        # Create the data array
        img_data = self.as_image(drop_dim=False)

        tifffile.imsave(params.seed_name + ".tif", img_data)

    def rotate(self, angle):
        if angle % 90 == 0:
            for frame in self.num_frames:
                np.rot90(self.pixel_data[frame, :, :], angle // 90)

        else:
            sys.exit("ERROR: Images can only be rotated by multiples of 90°")

    def determine_first_frame(self):
        self.first_frame = 0

    def max_intensity(self):
        max_intensity = np.max(self.pixel_data)

        return max_intensity
