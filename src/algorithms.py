#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import numpy as np

def fwhm(hist):
    x = np.linspace(0, 255, 256).astype(int)

    hist = hist / np.max(hist)
    N = hist.size-1

    lev50 = 0.5
    if hist[0] < lev50:
        centre_index = np.argmax(hist)
        Pol = +1
    else:
        centre_index = np.argmin(hist)
        Pol = -1

    extremum_val = x[centre_index]

    i = 1
    while np.sign(hist[i]-lev50) == np.sign(hist[i-1]-lev50):
        i += 1

    interp = (lev50-hist[i-1]) / (hist[i]-hist[i-1])
    lead_t = x[i-1] + interp*(x[i]-x[i-1])

    i = centre_index+1
    while (np.sign(hist[i]-lev50) == np.sign(hist[i-1]-lev50)) and (i <= N-1):
        i += 1

    if i != N:
        p_type  = 1
        interp  = (lev50-hist[i-1]) / (hist[i]-hist[i-1])
        trail_t = x[i-1] + interp*(x[i]-x[i-1])
        x_width = trail_t - lead_t
    else:
        p_type = 2
        trail_t = None
        x_width = None

    return (x_width, extremum_val)
