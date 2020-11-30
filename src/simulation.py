#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Simulator
"""
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import reduce

from spots import Spots
from images import Image

def simulate(params):
    # Initialise
    num_spots = 10
    Isingle = 10000
    BGmean = 500 # mean background pixel intensity
    BGstd = 120 # standard deviation of background pixels
    num_frames = 30
    sizeN = 64
    sizeM = 64
    bleach_time = 10 # in frames, if 0 then no bleaching
    diffusionCoeff = 1# um2/s
    nDiffPoints = 4 # number of MSD points to calculate diffusion const
    frameTime = 0.005 # seconds
    pixelSize = 0.120 # microns
    PSFwidth = 0.160/pixelSize # Sigma of a Gaussian, ~2/3 airy disk diameter
    saveImage = 1
    fileName = 'tdiffusingSpots.tif'

    # Make a spot array the same size as normal
    real_spots = [Spots(num_spots) for i in range(num_frames)]

    # initialise the spot co-ords
    real_spots[0].positions[:,0] = random.rand(num_spots) * sizeN
    real_spots[0].positions[:,1] = random.rand(num_spots) * sizeM
    real_spots[0].spot_intensity[:] = Isingle
    real_spots[0].frame = 1

    # Simulate diffusion
    S = np.sqrt(2*diffusionCoeff*frameTime)/pixelSize
    frame_start = 0
    frame_end = num_spots

    for frame in range(1,num_frames):
        real_spots[frame].frame = frame
        real_spots[frame].spot_intensity[:] = Isingle
        real_spots[frame].traj_num = real_spots[frame-1].traj_num[:]
        real_spots[frame].positions = random.normal(real_spots[frame-1].positions, S, (num_spots,2))

        if bleach_time > 0:
            bleached_spots = filter(lambda x: random.rand() < 1/bleach_time, range(num_spots))
            for spot in bleached_spots:
                real_spots[frame].positions[spot,0] = random.rand(1)*sizeN
                real_spots[frame].positions[spot,1] = random.rand(1)*sizeM
                next_traj_num = np.max(real_spots[frame].traj_num) + 1
                real_spots[frame].traj_num[spot] = next_traj_num


    # Simulate the image stack and save
    img_frames = np.zeros([num_frames, sizeN, sizeM])
    x_pos, y_pos = np.meshgrid(range(sizeN), range(sizeM))
    for frame in range(num_frames):
        for spot in range(num_spots):
            img_frames[frame,:,:] += (real_spots[frame].spot_intensity[spot]/(2*np.pi*PSFwidth)) \
                                   * np.exp(-( (x_pos - real_spots[frame].positions[spot,0])**2  \
                                              +(y_pos - real_spots[frame].positions[spot,1])**2  \
                                             ) / (2*PSFwidth**2) \
                                           )

    img_frames = img_frames.astype(np.uint16)

    for frame in range(num_frames):
        img_frames[frame,:,:] = random.poisson(img_frames[frame,:,:])
        img_frames[frame,:,:] += random.normal(BGmean, BGstd, [sizeN, sizeM]).astype(np.uint16)

    print("Min = ", np.min(img_frames))
    print("Max = ", np.max(img_frames))

    im = Image(fileName, img_frames)
    im.write()

    new_im = Image()
    new_im.read(fileName)


    fig = plt.figure()
    frames = []
    for frame in range(num_frames):
        im_frame = plt.imshow(new_im.data[frame,:,:], animated=True, vmin=0, vmax=np.max(new_im.data))
        frames.append([im_frame])

    
    video = animation.ArtistAnimation(fig, frames, interval=20)
    plt.show()

#
#
#    # Simulate image stack and save
