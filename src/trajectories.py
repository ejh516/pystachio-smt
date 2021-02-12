#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" TRAJECTORIES - Trajectory construction and manipulation module

Description:
    trajectories.py contains the Trajectory class containing information about
    spot trajectories across multiple frames, along with the routines involved
    in locating and extending the trajectories.

Contains:
    class Trajectory
    function build_trajectories
    function read_trajectories
    function write_trajectories

Author:
    Edward Higgins

Version: 0.2.0
"""

import csv
import sys

import numpy as np


class Trajectory:
    def __init__(self, id, spots, spot_id):
        self.id = id
        self.start_frame = spots.frame
        self.end_frame = spots.frame
        self.path = [spots.positions[spot_id, :]]
        self.intensity = [spots.spot_intensity[spot_id]]
        self.snr = [spots.snr[spot_id]]
        self.length = 1
        self.stoichiometry = 0

    def extend(self, spots, spot_id):
        if spots.frame > self.end_frame + 1:
            sys.exit("ERROR: Cannot extend a spot over multiple frames")

        self.end_frame = spots.frame
        self.path.append(spots.positions[spot_id, :])
        self.intensity.append(spots.spot_intensity[spot_id])
        self.snr.append(spots.snr[spot_id])

        self.length += 1


def build_trajectories(all_spots, params):
    trajectories = []
    traj_num = 0

    # Create a trajectory for all spots in the first frame
    for i in range(all_spots[0].num_spots):
        trajectories.append(Trajectory(traj_num, all_spots[0], i))
        traj_num += 1

    # Construct trajectories for the rest of the frames
    for frame in range(1, len(all_spots)):
        assigned_spots = []
        for spot in range(all_spots[frame].num_spots):
            close_candidates = []
            for candidate in trajectories:
                if candidate.end_frame != frame - 1:
                    continue
                candidate_dist = np.linalg.norm(
                    all_spots[frame].positions[spot, :] - candidate.path[-1]
                )
                if candidate_dist < params.max_displacement:
                    close_candidates.append(candidate)

            if len(close_candidates) == 0:
                trajectories.append(Trajectory(traj_num, all_spots[frame], spot))
                traj_num += 1

            if len(close_candidates) == 1:
                close_candidates[0].extend(all_spots[frame], spot)

            else:
                trajectories.append(Trajectory(traj_num, all_spots[frame], spot))
                traj_num += 1

    filtered_trajectories = list(filter(lambda x: x.length > 1, trajectories))

    actual_traj_num = 1
    for traj in filtered_trajectories:
        traj.id = actual_traj_num
        actual_traj_num += 1

    filtered_trajectories = list(filter(lambda x: x.length > 1, trajectories))
    return filtered_trajectories


def write_trajectories(trajectories, params):
    f = open(params.seed_name + "_trajectories.tsv", "w")
    f.write(f"trajectory\tframe\tx\ty\tintensity\tSNR\n")
    for traj in trajectories:
        for frame in range(traj.start_frame, traj.end_frame + 1):
            i = frame - traj.start_frame
            f.write(
                f"{traj.id}\t{frame}\t{traj.path[i][0]}\t{traj.path[i][1]}\t{traj.intensity[i]}\t{traj.snr[i]}\n"
            )
    f.close()


def read_trajectories(filename):
    trajectories = []
    prev_traj_id = -1
    with open(filename) as tsv_file:
        tsv_reader = csv.reader(tsv_file)
        for line in tsv_reader:
            spot = Spots(num_spots=1)
            traj_id = line[0] = traj_id
            spot.frame = line[1]
            spot.position[0, :] = line[2:3]
            spot.intensity[0] = line[4]
            spot.snr[0] = line[5]

            if traj_id != prev_traj_id:
                trajectories.append(Trajectory(traj_id, spot, 0))
            else:
                trajectories[-1].extend(spot, 0)
