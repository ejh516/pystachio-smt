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

import spots

def track(image_data, params):

    sys.exit("Tracking is not yet implemented")
    # For each frame, detect spots
    all_spots = []
    for frame in range(image_data.num_frames):
        if params.verbose: print(f"Tracking frame {frame+1} of {image_data.num_frames}")

        # Isolate this frame's data
        frame_data = image_data[frame]
        frame_data.show()

        # Find the spots in this frame
        frame_spots = spots.Spots()
        frame_spots.find_in_frame(frame_data)
        frame_spots.merge_coincedent_candidates(frame_data)
        if params.verbose: print(f"    {frame_spots.num_spots} candidates found")

        # Iteratively refine the spot centres
        frame_spots.refine_centres(frame_data)

        all_spots.append(frame_spots)

    # Link the spot trajectories across the frames
    spots.link_spot_trajectories(all_spots)

    return all_spots
