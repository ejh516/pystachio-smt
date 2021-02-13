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

class State:
    def __init__(self, parameters):
        self.parameters = parameters
        self.image_data = None
        self.spots = None
        self.trajectories = None

    def render(self):
        maxval = self.image_data.max_intensity()
        figure = plt.figure()
        plt_frames = []

        px_size = self.parameters.pixelSize
        fr_size = self.image_data.frame_size
        
        for frame in range(self.image_data.num_frames):
            plt_frame = plt.imshow(
                    self.image_data.pixel_data[frame,:,:],
                    animated=True,
                    vmin=0,
                    vmax=maxval, 
                    extent=[0, fr_size[0]*px_size, 0, fr_size[1]*px_size]
            )

#EJH#             if self.trajectories:
#EJH#                 colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple"]
#EJH#                 x = []
#EJH#                 y = []
#EJH#                 for traj in self.trajectories:
#EJH#                     if frame < traj.start_frame or frame > traj.end_frame:
#EJH#                         continue
#EJH# 
#EJH#                     x.append(traj.path[frame - traj.start_frame][0])
#EJH#                     y.append(traj.path[frame - traj.start_frame][1])
#EJH# 
#EJH#                 x = np.array(x)
#EJH#                 y = np.array(y)
#EJH#                 x_scaled = (fr_size[0]-x) * px_size
#EJH#                 y_scaled = y * px_size
#EJH#                 plt.scatter(y_scaled,x_scaled,c=colors[traj.id % 5])
#EJH# 
        plt_frames.append([plt_frame])

        video = animation.ArtistAnimation(figure, plt_frames, interval=50)
        plt.title("Simulated spot data")
        plt.xlabel("μm")
        plt.ylabel("μm")
        plt.colorbar()
        plt.show()
