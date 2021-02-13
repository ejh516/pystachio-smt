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

import tracking
import simulation
import parameters
import images
import postprocessing
import state

def main():
    params = parameters.Parameters()
    params.read(sys.argv)

    st = state.State(params)

    for task in params.task:
        if task == "track":
            st.image_data = images.ImageData()
            st.image_data.read(params.seed_name)

            st.spots, st.trajectories = tracking.track(st.image_data, st.parameters)

        elif task == "simulate":
            st.image_data = simulation.simulate(st.parameters)
#EJH#             spot_data.write(params)
            st.image_data.write(st.parameters)

        elif task=="simulate_stepwise":
            st.image_data = simulation.simulate_stepwise_bleaching(st.parameters)
            st.image_data.write(st.parameters)

        elif task == "postprocess":
            intensities = np.array([])
            snrs = np.array([])
            for i in range(len(st.spots)):
                tmp = st.spots[i].spot_intensity
                intensities = np.concatenate((intensities,tmp))
                snrs = np.concatenate((snrs,st.spots[i].snr))

            calculated_snr = postprocessing.plot_snr(snrs)
            calculated_isingle = postprocessing.get_isingle(intensities)
            dc, lp = postprocessing.get_diffusion_coef(st.trajectories, st.parameters)

            print(np.mean(dc))
            postprocessing.plot_traj_intensities(st.trajectories)
            postprocessing.get_stoichiometries(st.trajectories, calculated_isingle, st.parameters)

        elif task == "view":
            if not st.image_data.exists:
               sys.exit(f"ERROR: No file loaded to view")

            st.render()

        else:
            sys.exit(f"ERROR: Task {task} is not yet implemented. Aborting...")


if __name__ == "__main__":
    main()

