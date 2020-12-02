#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Single Molecule Tools
"""
import numpy as np
import sys

from fitting import Fit
from images import Image

def track(filename, params):

    # Create fit type and options
    fit = Fit(params)

    # Read in the tif data
    image_data = Image.read(filename, params)


    if params.verbose: print(f"Loaded {image_data.num_frames} frames from {filename}")

    # Rotate channels if horizonatally split
    if params.c_split == "horizontal":
        image_data.rotate(270)


    # Determine the laser-on frame
    start_frames = detect_laser_on(image_data, params)

    if params.frames_to_track == 0:
        params.frames_to_track = image_data.num_frames - start_frames[0]

    # Calculate per-pixel frame average
    image_data.calculate_frame_average(start_frames, params)

    for channel in range(params.start_channel, params.end_channel+1):
        # Initialise the spot array
        spots = []
        spot_images = []

        # Determine the start & end frame and the step size
        start_frame = start_frames[channel]

        if params.ALEX:
            frame_step = 2
        else:
            frame_step = 1

        # Loop over the frames
        for i in range(start_frame, start_frame+params.frames_to_track, frame_step):
            if params.verbose:
                print(f"Tracking frame {i}") 

            if np.max(image_data.frames[:,:,i]) > params.sat_pixel_val:
                sys.stderr.write("WARNING: Frame includes saturated pixels!\n")


            if params.use_cursor:
                sys.exit("ERROR: Cursor mode not yet supported!")

            else:
                candidate_spots = find_spots(image_data.frame(i), params)

            if params.verbose:
                print("Candidates found")



            # Plot the candidate spots
            # ...




def detect_laser_on(image_data,params):
    start_frames = [0,0]
    if params.determine_first_frames:
        start_frames = (image_data, params)

    else:
        if params.ALEX:
            start_frames[0] = 1
            start_frames[1] = 2
        else:
            start_frames[0] = 0
            start_frames[1] = 0

        

    sys.stderr.write("WARNING: detect_laser_on not yet impletmented!\n")
    return start_frames
    # ...

def find_spots(frame, params):
    signal = tophat(frame)

    hist = img_histogram(signal)

    x_width, maxmin_val = fwhm(hist)

    if x_width > 0:
        threshold_cell_auto = maxmin_val
    else:
        threshold_cell_auto = maxloc(hist)

    gaussian_signal = gaussian()

    sys.stderr.write("WARNING: find_spots not yet impletmented!\n")
    return []
