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
#EJH#     # For each frame, detect spots
#EJH#     all_spots = []
#EJH#     for frame in range(image_data.num_frames):
#EJH#         if params.verbose: print(f"Tracking frame {frame+1} of {image_data.num_frames}")
#EJH# 
#EJH#         # Isolate this frame's data
#EJH#         frame_data = image_data.frames[frame]
#EJH#         frame_spots = spots.Spots()
#EJH# 
#EJH#         # Find the spots in this frame
#EJH#         frame_spots.find_in_frame(frame_data)
#EJH#         frame_spots.merge_coincedent_candidates(frame_data)
#EJH#         if params.verbose: print(f"    {frame_spots.num_spots} candidates found")
#EJH# 
#EJH#         # Iteratively refine the spot centres
#EJH#         frame_spots.refine_centres(frame_data)
#EJH# 
#EJH#         all_spots.append(frame_spots)
#EJH# 
#EJH#     # Link the spot trajectories across the frames
#EJH#     spots.link_spot_trajectories(all_spots)
#EJH# 
#EJH#     return all_spots
