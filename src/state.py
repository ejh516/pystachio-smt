#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" STATE - Contains the current state of the program

Description:
    state.py contains the State class which stores the current state of the
    program, including the image data, spots and trajectories currently in use.

Contains:
    class State

Author:
    Edward Higgins

Version: 0.2.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

class State:
    def __init__(self, parameters):
        self.parameters = parameters
        self.image_data = None
        self.spots = None
        self.trajectories = None
        self.true_trajectories = None

    def render(self):
        maxval = self.image_data.max_intensity()
        figure = plt.figure()
        plt_frames = []

        px_size = self.parameters.pixelSize
        fr_size = self.image_data.frame_size

        colors = list(mcolors.TABLEAU_COLORS.keys())

        if self.trajectories:
            for traj in self.trajectories:
                x = []
                y = []
                for frame in range(traj.start_frame, traj.end_frame):
                    x.append(traj.path[frame - traj.start_frame][0])
                    y.append(traj.path[frame - traj.start_frame][1])

                x = np.array(x)
                y = np.array(y)
                x_scaled = (x+0.5) * px_size
                y_scaled = (fr_size[1]-y-0.5) * px_size
                plt.plot(x_scaled,y_scaled,"o-",c="tab:red")

        if self.true_trajectories:
            for traj in self.true_trajectories:
                x = []
                y = []
                for frame in range(traj.start_frame, traj.end_frame):
                    x.append(traj.path[frame - traj.start_frame][0])
                    y.append(traj.path[frame - traj.start_frame][1])

                x = np.array(x)
                y = np.array(y)
                x_scaled = (x+0.5) * px_size
                y_scaled = (fr_size[1]-y-0.5) * px_size
                plt.plot(x_scaled,y_scaled,"+--",c="tab:orange")


#EJH#         for frame in range(self.image_data.num_frames):
        plt_frame = plt.imshow(
                self.image_data.pixel_data[-1,:,:],
                vmin=0,
                vmax=maxval, 
                extent=[0, fr_size[0]*px_size, 0, fr_size[1]*px_size]
        )

        plt.title(f"Simulated spot data, frame {self.image_data.num_frames}")
        plt.xlabel("μm")
        plt.ylabel("μm")
        plt.colorbar()
        plt.show()
