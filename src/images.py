#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
IMAGES
"""


from libtiff import TIFF
import sys

import numpy as np

class Image():
    def read(filename, params):
        im = Image()
        im.tif = TIFF.open(filename)

        iframe = 1
        for frame in im.tif.iter_images():
            if iframe == 1:
                im.frames = np.expand_dims(frame,axis=2)
            else:
                im.frames = np.append(im.frames,np.expand_dims(frame,axis=2),axis=2)
            iframe += 1


        im.num_frames = np.size(im.frames,axis=2)
        return im

    def frame(self, iframe):
        return self.frames[iframe]

    def rotate(self, angle):
        if angle % 270 == 0:
            for frame in self.frames:
                np.rot90(frame, angle//270)

        else:
            sys.exit("ERROR: Images can only be rotated by multiples of 90°")

    def calculate_frame_average(self, start_frames, params):
        frame_average = []
        if params.ALEX:
            frame_average.append(np.sum(self.frames[:,:,start_frames[0]:2*params.frame_avg_window:2], axis=2))
            frame_average.append(np.sum(self.frames[:,:,start_frames[1]:2*params.frame_avg_window:2], axis=2))
        else:
            start_frame = min(start_frames)
            frame_average.append(np.sum(self.frames[:,:,start_frame:start_frame+params.frame_avg_window], axis=2))
