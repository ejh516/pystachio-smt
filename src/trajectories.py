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
    def __init__(self, id, frame, position):
        self.id = id
        self.start_frame = frame
        self.end_frame = frame
        self.path = np.zeros([1,2])
        self.path[0,:] = position
        self.length = 1

    def extend(self, frame, position):
        print(f"Extending trajectory {self.id} from frame {self.end_frame} to {frame}")
        print(f"  Started at {self.start_frame}")

        print(f"Old shape: {self.path.shape}")
        print(f"New shape: {[self.end_frame - self.start_frame+2, 2]}")
        print(f"End frame: {self.end_frame} -> {frame}")

        if frame > self.end_frame + 1: 
            sys.exit("ERROR: Cannot extend a spot over multiple frames")

        self.end_frame = frame
        old_path = self.path
        self.path = np.zeros([self.end_frame - self.start_frame+2, 2])
        self.path[0:-1,:] = old_path
        self.path[-1,:] = position
        self.length += 1

def build_trajectories(all_spots, params):
    trajectories = []
    traj_num = 0

    # Create a trajectory for all spots in the first frame
    for i in range(all_spots[0].num_spots):
        trajectories.append(Trajectory(traj_num, 0, all_spots[0].positions[i,:]))
        traj_num += 1

    # Construct trajectories for the rest of the frames
    for frame in range(1,len(all_spots)):
        assigned_spots = []
        for spot in range(all_spots[frame].num_spots):
            close_candidates = []
            for candidate in trajectories:
                if candidate.end_frame != frame - 1:
                    continue
                candidate_dist = np.linalg.norm(all_spots[frame].positions[spot,:] - candidate.path[-1,:])
                if  candidate_dist < params.max_displacement:
                    close_candidates.append(candidate)

            if len(close_candidates) == 0:
                print(f"New trajectory found at {all_spots[frame].positions[spot,:]}") 
                trajectories.append(Trajectory(traj_num, frame, all_spots[frame].positions[spot,:]))
                traj_num += 1

            if len(close_candidates) == 1:
                print(f"Extending trajcectory {close_candidates[0].id} to position {all_spots[frame].positions[spot,:]}") 
                close_candidates[0].extend(frame, all_spots[frame].positions[spot,:])

            else:
                print(f"Too many candidates, new trajectory created at {all_spots[frame].positions[spot,:]}") 
                trajectories.append(Trajectory(traj_num, frame, all_spots[frame].positions[spot,:]))
                traj_num += 1

    filtered_trajectories = list(filter(lambda x: x.length > 1, trajectories))

    actual_traj_num = 1
    for traj in filtered_trajectories:
        traj.id = actual_traj_num
        actual_traj_num += 1

    filtered_trajectories = list(filter(lambda x: x.length > 1, trajectories))
    return filtered_trajectories


def write_trajectories(trajectories,params):
    f = open(params.seed_name + "_trajectories.tsv", "w")
    for traj in trajectories:
        for i in range(traj.start_frame, traj.end_frame+1):
            f.write(f"{traj.id}\t{i}\t{traj.path[i-traj.start_frame,0]}\t{traj.path[i-traj.start_frame,1]}\n")
    f.close()

def read_trajectories(filename):
    trajectories = []
    prev_traj_id = -1
    with open(filename) as tsv_file:
        tsv_reader = csv.reader(tsv_file)
        for line in tsv_reader:
            traj_id = line[0] = traj_id
            frame = line[1]
            position = line[1:2]

            if traj_id == prev_traj_id:
                traj.extend(frame, position)


