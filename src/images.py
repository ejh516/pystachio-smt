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

import tifffile
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2 as cv

class ImageData():
    def __init__(self):
        self.defined = False

    def __getitem__(self, index):
        frame = ImageData()
        frame.initialise(1, self.resolution)
        frame.pixel_data[0,:,:] = self.pixel_data[index,:,:]
        return frame

    def __setitem__(self, index, value):
        if value.__class__ == "ImageData":
            self.pixel_data[index,:,:] = value.pixel_data[0,:,:]
        else:
            self.pixel_data[index,:,:] = value

    def initialise(self, num_frames, resolution):
        self.num_frames = num_frames
        self.resolution = resolution
        self.num_pixels = resolution[0] * resolution[1]

        self.pixel_data = np.zeros([num_frames, resolution[0], resolution[1]])

        self.defined = True

    def as_image(self):
        max_val = np.max(self.pixel_data)
        min_val = np.min(self.pixel_data)

        img = (255 * (self.pixel_data+min_val) / (max_val+min_val)).astype(np.uint8)
        return img

    def read(self, filename):
        # Read in the file and get the data size
        pixel_data = tifffile.imread(filename)
        self.num_frames = pixel_data.shape[0]
        self.resolution = (pixel_data.shape[1], pixel_data.shape[2])
        self.num_pixels = pixel_data.shape[1] * pixel_data.shape[2]

        # Store the frames in a list
        self.pixel_data = pixel_data

        self.determine_first_frame()

        self.defined = True

    def write(self, params):
        # Create the data array
        img_data = self.as_image()

        tifffile.imsave(params.seed_name + ".tif", img_data)

    def rotate(self, angle):
        if angle % 90 == 0:
            for frame in self.num_frames:
                np.rot90(self.pixel_data[frame,:,:], angle//90)

        else:
            sys.exit("ERROR: Images can only be rotated by multiples of 90°")

    def determine_first_frame(self):
        self.first_frame = 0

    def max_intensity(self):
        max_intensity = np.max(self.pixel_data)

        return max_intensity

    def render(self, params, spot_positions=[]):
        maxval = self.max_intensity()
        figure = plt.figure()
        plt_frames = []

        for frame in range(self.num_frames):
            plt_frame = plt.imshow(self.pixel_data[frame,:,:], animated=True, vmin=0, vmax=maxval, 
                    extent=[0, self.resolution[0]*params.pixelSize, 0, self.resolution[1]*params.pixelSize])
            if len(spot_positions) > 0:
                [x,y] = zip(*spot_positions)
                x_scaled = []
                y_scaled = []
                for i in range(len(x)):
                    x_scaled.append((64-x[i]) * params.pixelSize)
                    y_scaled.append(y[i] * params.pixelSize)
                plt.scatter(y_scaled,x_scaled,c="r")

            plt_frames.append([plt_frame])

        video = animation.ArtistAnimation(figure, plt_frames, interval=50)
        plt.title("Simulated spot data")
        plt.xlabel("μm")
        plt.ylabel("μm")
        plt.show()

def display_image(img):
    cv.imshow('image', img)
    cv.watKEy(0)
    cv.destroyAllWindows()
