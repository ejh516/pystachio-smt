#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" TRACKING - Spot tracking module

Description:
    tracking.py contains the code for the tracking task, which identifies spots
    within a set of frames and builds spot trajectories across those frames.

Contains:
    function track

Author:
    Edward Higgins

Version: 0.2.0
"""

import sys

import numpy as np
import multiprocessing as mp

import spots
import trajectories


def track(image_data, params):
    # For each frame, detect spots
    all_spots = []
    res = [None] * image_data.num_frames
    with mp.Pool(params.num_procs) as pool:
        for frame in range(image_data.num_frames):
            res[frame] = pool.apply_async(track_frame, (image_data[frame], frame, params))
        for frame in range(image_data.num_frames):
            all_spots.append(res[frame].get())


    # Link the spot trajectories across the frames
    trajs = trajectories.build_trajectories(all_spots, params)
    trajectories.write_trajectories(trajs, params)

    # EJH#     image_data.render(trajectories=traj)

    return (all_spots, trajs)

def track_frame(frame_data, frame, params):
        # Find the spots in this frame
        frame_spots = spots.Spots(frame=frame)
        frame_spots.find_in_frame(frame_data.as_image()[:, :], params)
        found_spots = frame_spots.num_spots
        frame_spots.merge_coincident_candidates()

        merged_spots = frame_spots.num_spots
        # Iteratively refine the spot centres
        frame_spots.refine_centres(frame_data, params)

        frame_spots.filter_candidates(params)

        print(
            f"Frame {frame:4d}: found {frame_spots.num_spots:3d} spots "
            f"({found_spots:3d} identified, "
            f"{found_spots-merged_spots:3d} merged, "
            f"{merged_spots-frame_spots.num_spots:3d} filtered)"
        )
        return frame_spots
