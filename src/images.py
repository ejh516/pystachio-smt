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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Frame():
    def __init__(self, frame_num, pixel_data):
        self.frame_num = frame_num
        self.pixel_data = pixel_data.astype(np.uint16)
        self.resolution = (self.pixel_data.shape[0], self.pixel_data.shape[1])
        self.num_pixels = self.pixel_data.shape[0] * self.pixel_data.shape[1]
        self.average = np.sum(self.pixel_data) / self.num_pixels

    def set_pixel_data(self, pixel_data):
        self.pixel_data = pixel_data
        self.average = np.sum(self.pixel_data) / self.num_pixels

class ImageData():
    def __init__(self):
        self.defined = False

    def initialise(self, num_frames, resolution):
        self.num_frames = num_frames
        self.resolution = resolution
        self.num_pixels = resolution[0] * resolution[1]

        self.frames = []
        for i in range(self.num_frames):
            self.frames.append(Frame(i, np.zeros(self.resolution)))

        self.defined = True

    def read(self, filename):
        # Read in the file and get the data size
        pixel_data = tifffile.imread(filename)
        self.num_frames = pixel_data.shape[0]
        self.resolution = (pixel_data.shape[1], pixel_data.shape[2])
        self.num_pixels = pixel_data.shape[1] * pixel_data.shape[2]

        # Store the frames in a list
        self.frames = []
        for i in range(self.num_frames):
            self.frames.append(Frame(i, pixel_data[i,:,:]))

        self.determine_first_frame()

        self.defined = True

    def write(self, params):
        # Create the data array
        data = np.zeros((self.num_frames, self.resolution[0], self.resolution[1])).astype(np.uint16)
        for i in range(self.num_frames):
            data[i,:,:] = self.frames[i].pixel_data

        tifffile.imsave(params.filename, data)

    def rotate(self, angle):
        if angle % 90 == 0:
            for frame in self.frames:
                np.rot90(frame.pixel_data, angle//90)

        else:
            sys.exit("ERROR: Images can only be rotated by multiples of 90°")

    def determine_first_frame(self):
        self.first_frame = 0

    def max_intensity(self):
        max_intensity = 0
        for frame in self.frames:
            max_intensity = max(max_intensity, np.max(frame.pixel_data))

        return max_intensity

    def render(self):
        print("Rendering image")
        maxval = self.max_intensity()
        figure = plt.figure()
        plt_frames = []

        for frame in self.frames:
            plt_frame = plt.imshow(frame.pixel_data, animated=True, vmin=0, vmax=maxval)
            plt_frames.append([plt_frame])

        video = animation.ArtistAnimation(figure, plt_frames, interval=50)
        plt.show()

        print("Done!")
