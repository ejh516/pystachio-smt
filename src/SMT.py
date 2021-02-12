#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" SMT - Single Molecule Tools program

Description:
    SMT.py contains the main program used for running SMT-Python
 
Contains:
    function main

Author:
    Edward Higgins

Version: 0.2.0
"""

import sys

import numpy as np

import images
import parameters
import postprocessing
import simulation
import tracking


def main():
    params = parameters.Parameters()
    params.read(sys.argv)

    for task in params.task:
        if task == "track":
            image_data = images.ImageData()
            image_data.read(params.seed_name + ".tif")

            if params.verbose:
                print(f"Loaded {image_data.num_frames} frames from {params.seed_name}")
                print(f"Resolution: {image_data.frame_size}")

            spots, trajs = tracking.track(image_data, params)
            intensities = np.array([])
            for i in range(len(spots)):
                tmp = spots[i].spot_intensity
                intensities = np.concatenate((intensities, tmp))
            calculated_isingle = postprocessing.get_isingle(intensities)
            dc, lp = postprocessing.get_diffusion_coef(trajs, params)
            print(np.mean(dc))
            postprocessing.plot_traj_intensities(trajs)
            postprocessing.get_stoichiometries(trajs, calculated_isingle, params)

        elif task == "simulate":
            image_data = simulation.simulate(params)
            # EJH#             spot_data.write(params)
            image_data.write(params)

        elif task == "simulate_stepwise":
            image_data = simulation.simulate_stepwise_bleaching(params)
            image_data.write(params)

        elif task == "view":
            img = images.ImageData()
            img.read(params.seed_name + ".tif")
            img.render(params)

        else:
            sys.exit(f"ERROR: Task {task} is not yet implemented. Aborting...")


if __name__ == "__main__":
    main()
