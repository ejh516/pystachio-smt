#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" SIMULATION - Dataset simulation module

Description:
    simulation.py contains the code for the simulation task, which simulates
    pseudo-experimental datasets as characterised by the relevant parameters.

Contains:
    function simulate

Author:
    Edward Higgins

Version: 0.2.0
"""

from functools import reduce

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random

from images import ImageData
from spots import Spots
import trajectories


def simulate(params):
    # Get the parameters
    file_prefix = params.get('general', 'name')
    num_frames = params.get("image", "num_frames")
    frame_size = params.get("image", "frame_size")
    pixel_size = params.get("image", "pixel_size")
    frame_time = params.get("image", "frame_time")
    num_spots = params.get("simulation", "num_spots")
    I_single = params.get("simulation", "I_single")
    diffusion_coeff = params.get("simulation", "diffusion_coeff")
    max_spot_molecules = params.get("simulation", "max_spot_molecules")
    p_bleach_per_frame = params.get("simulation", "p_bleach_per_frame")
    psf_width = params.get("simulation", "spot_width")
    bg_mean = params.get("simulation", "bg_mean")
    bg_std = params.get("simulation", "bg_std")

    # Make a spot array the same size as normal
    real_spots = [Spots(num_spots) for i in range(num_frames)]
    if max_spot_molecules == 1:
        n_mols = [1] * num_spots
    else:
        n_mols = random.randint(1, max_spot_molecules, num_spots)

    # initialise the spot co-ords
    real_spots[0].positions[:, 0] = random.rand(num_spots) * frame_size[0]
    real_spots[0].positions[:, 1] = random.rand(num_spots) * frame_size[1]
    real_spots[0].spot_intensity[:] = I_single
    real_spots[0].frame = 1

    # Simulate diffusion
    S = np.sqrt(2 * diffusion_coeff * frame_time) / pixel_size
    frame_start = 0
    frame_end = num_spots

    for frame in range(1, num_frames):
        real_spots[frame].frame = frame
        real_spots[frame].spot_intensity[:] = I_single * np.array(n_mols)
        real_spots[frame].traj_num = real_spots[frame - 1].traj_num[:]
        real_spots[frame].positions = random.normal(
            real_spots[frame - 1].positions, S, (num_spots, 2)
        )

        # Photobleah some spots
        for i in range(num_spots):
            if n_mols[i] > 0:
                for j in range(n_mols[i]):
                    if random.rand() < p_bleach_per_frame:
                        n_mols[i] -= 1

    # Simulate the image stack and save
    image = ImageData()
    image.initialise(num_frames, frame_size)

    x_pos, y_pos = np.meshgrid(range(frame_size[0]), range(frame_size[1]))
    for frame in range(num_frames):
        frame_data = np.zeros([frame_size[1], frame_size[0]]).astype(np.uint16)

        for spot in range(num_spots):
            spot_data = (
                (real_spots[frame].spot_intensity[spot] / (2 * np.pi * psf_width**2))
                * np.exp(
                    -(
                        (x_pos - real_spots[frame].positions[spot, 0]) ** 2
                        + (y_pos - real_spots[frame].positions[spot, 1]) ** 2
                    )
                    / (2 * psf_width ** 2)
                )
            ).astype(np.uint16)
            frame_data += spot_data
            real_spots[frame].spot_intensity[spot]=np.sum(spot_data)

        frame_data = random.poisson(frame_data)
        bg_noise = random.normal(bg_mean, bg_std, [frame_size[1], frame_size[0]])
        frame_data += np.where(bg_noise > 0, bg_noise.astype(np.uint16), 0)
        image[frame] = frame_data

    real_trajs = trajectories.build_trajectories(real_spots, params)

    image.write(file_prefix + ".tif")
    trajectories.write_trajectories(real_trajs, file_prefix + '_simulated.tsv')
    return image, real_trajs


