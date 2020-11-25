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
from spots import Spots

def simulate(params):
    # Initialise
    noSpots = 2
    Isingle = 10000
    BGmean = 500 # mean background pixel intensity
    BGstd = 120 # standard deviation of background pixels
    noFrames = 5
    sizeN = 50
    sizeM = 50
    bleachTime = 10 # in frames, if 0 then no bleaching
    diffusionCoeff = 1# um2/s
    nDiffPoints = 4 # number of MSD points to calculate diffusion const
    frameTime = 0.005 # seconds
    pixelSize = 0.120 # microns
    PSFwidth = 0.160/pixelSize # Sigma of a Gaussian, ~2/3 airy disk diameter
    saveImage = 1
    fileName = 'tdiffusingSpots.tif'

    # Make a spot array the same size as normal
    real_spots = [Spots.new(noSpots*noFrames)] * noFrames
    real_spots[:].spot_intensity = Isingle

    # initialise the spot co-ords
    real_spots[0].positions[:,0] = random.rand(noSpots) * sizeN
    real_spots[0].positions[:,1] = random.rand(noSpots) * sizeM
    real_spots[:].first_frame = 0
    real_spots[:].traj_num = range(0, noSpots)

    # Simulate diffusion
    S = np.sqrt(2*diffusionCoeff*frameTime)/pixelSize
    currentTrajNo = range(noSpots)
    frame_start = 0
    frame_end = noSpots

    for frame in range(1,noFrames):
        prev_frame_start = frame_start
        prev_frame_end = frame_end
        frame_start += noSpots
        frame_end   += noSpots
        spotsReal[frame_start:frame_end,8] = frame
        spotsReal[frame_start:frame_end,9] = currentTrajNo
        spotsReal[frame_start:frame_end,0:2] = random.normal(spotsReal[prev_frame_start:prev_frame_end,0:2],S,(noSpots,2))

        if bleachTime>0:
            bleachedSpots=filter(random.rand(noSpots)<1/bleachTime, currentTrajNo)
            for b=1:length(bleachedSpots)
                spotsReal(spotsReal(:,9)==t+1 & spotsReal(:,9)==bleachedSpots(b),1)=rand(1)*sizeN
                spotsReal(spotsReal(:,9)==t+1 & spotsReal(:,9)==bleachedSpots(b),2)=rand(1)*sizeM
                spotsReal(spotsReal(:,9)==t+1 & spotsReal(:,9)==bleachedSpots(b),9)=max(spotsReal(:,9))+1            

        currentTrajNo = spotsReal[frame_start:frame_end,9]
    print("Positions:")
    print(spotsReal[:,0:2])


#
#
#    # Simulate image stack and save
