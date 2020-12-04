#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Single Molecule Tools
"""
import sys
import numpy as np

import tracking
import simulation
import parameters
import images

def main():
    params = parameters.Parameters()
    params.read(sys.argv)

    if params.task == "track":
        pixel_data = PixelData()
        pixel_data.read(params.filename)

        if params.verbose:
            print(f"Loaded {pixel_data.num_frames} frames from {filename}")
            print(f"Resolution: {pixel_data.resolution}")

        spots = tracking.track(filename, params)

    elif params.task == "simulate":
        image_data = simulation.simulate(params)
#EJH#         spot_data.write(params)
        image_data.write(params)

    elif params.task == "view":
        img = images.ImageData()
        img.read(params.filename)
        img.render()

    else:
        print("//////////////////////////////")
        print("     Single Molecule Tools")
        print("   Construction in progress")
        print("//////////////////////////////")


if __name__ == "__main__":
    main()
