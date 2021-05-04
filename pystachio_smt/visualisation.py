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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

import images
import trajectories

def render(params):
    image_data = images.ImageData()
    image_data.read(params)
    trajs = trajectories.read_trajectories(params.name + "_trajectories.tsv")
    true_trajs = trajectories.read_trajectories(params.name + "_simulated.tsv")

    maxval = image_data.max_intensity()
    figure = plt.figure()
    plt_frames = []

    px_size = params.pixel_size
    fr_size = image_data.frame_size

    colors = list(mcolors.TABLEAU_COLORS.keys())

    if trajs:
        print(f"Displaying {len(trajs)} trajectories")
        for traj in trajs:
            x = []
            y = []
            for frame in range(traj.start_frame, traj.end_frame):
                x.append(traj.path[frame - traj.start_frame][0])
                y.append(traj.path[frame - traj.start_frame][1])

            x = np.array(x)
            y = np.array(y)
            x_scaled = (x+0.5) * px_size
            y_scaled = (fr_size[1]-y-0.5) * px_size
            plt.plot(x_scaled,y_scaled,"o-",c=colors[traj.id % len(colors)])

    if true_trajs:
        print(f"Displaying {len(true_trajs)} true trajectories")
        for traj in true_trajs:
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


    plts = []
    for frame in range(image_data.num_frames):
        plt_frame = plt.imshow(
                image_data.pixel_data[frame,:,:],
                vmin=0,
                animated=True,
                vmax=maxval, 
                cmap=plt.get_cmap("gray"),
                extent=[0, fr_size[0]*px_size, 0, fr_size[1]*px_size]
        )
        plts.append([plt_frame]) 

    ani = animation.ArtistAnimation(figure, plts, interval=50,)

    plt.title(f"Simulated spot data, frame {image_data.num_frames}")
    plt.xlabel("μm")
    plt.ylabel("μm")
    plt.colorbar()
    plt.show()
    
