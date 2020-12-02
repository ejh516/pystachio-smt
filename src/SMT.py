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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tracking import track
from simulation import simulate
from parameters import Parameters
from images import Image

def main():
    params = Parameters()

    mode = sys.argv[1]
    if mode == "track":
        filename = sys.argv[2]
        track(filename, params)

    elif mode == "simulate":
        simulate(params)

    elif mode == "view":
        img = Image()
        filename = sys.argv[2]
        img.read(filename)


        fig = plt.figure()
        frames = []
        for frame in range(img.num_frames):
            im_frame = plt.imshow(img.data[frame,:,:], animated=True, vmin=0, vmax=np.max(img.data))
            frames.append([im_frame])

        
        video = animation.ArtistAnimation(fig, frames, interval=50)
        plt.show()



    else:
        print("//////////////////////////////")
        print("     Single Molecule Tools")
        print("   Construction in progress")
        print("//////////////////////////////")


if __name__ == "__main__":
    main()
