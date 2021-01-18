#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
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
        self.end_frame = frame
        old_path = self.path
        self.path = np.zeros([self.end_frame - self.start_frame+2, 2])
        self.path[0:-1,:] = old_path
        self.path[-1,:] = position
        self.length += 1

def build_trajectories(all_spots):
    trajectories = []
    for frame_spots in all_spots:
        for i in range(frame_spots.num_spots):
            traj_num = frame_spots.traj_num[i]
            frame = frame_spots.frame
            position = frame_spots.positions[i,:]
            if traj_num >= len(trajectories):
                print(f"Creating {traj_num} in frame {frame}")
                traj = Trajectory(len(trajectories), frame, position)
                traj.start_frame = frame
                traj.end_frame = frame

                trajectories.append(traj)
            else:
                print(f"Extending {traj_num} in frame {frame}")
                trajectories[traj_num].extend(frame, position)

    filtered_trajectories = filter(lambda x: x.length > 1, trajectories)
    
    return filtered_trajectories

def write_trajectories(trajectories,params):
    f = open(params.seed_name + "_trajectories.tsv", "w")
    for traj in trajectories:
        for i in range(traj.start_frame, traj.end_frame+1):
            f.write(f"{traj.id}\t{i}\t{traj.path[i-traj.start_frame,0]}\t{traj.path[i-traj.start_frame,1]}\n")
    f.close()

