"""
Post processing trajectories and intensities

Routines for getting isingle and diffusion coefficient from lists of intensities

v0.1 Jack W Shepherd, University of York
"""

import numpy as np
from scipy.stats import gaussian_kde
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def straightline(x,m,c):
    return m*x + c

def get_isingle(intensities):
    intensities = intensities[intensities > 1]
    bandwidth=0.7
    kde = gaussian_kde(intensities, bw_method=bandwidth)
    x = np.linspace(0, np.amax(intensities), 10000)
    pdf = kde.evaluate(x)
    fig, ax1 = plt.subplots()
    ax1.hist(intensities, bins=np.arange(0,np.amax(intensities)+100,100), label="Raw data")
    ax2 = ax1.twinx()
    ax2.plot(x, pdf, 'k-', label="Gaussian KDF")
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,2))
    plt.legend()
    plt.show()
    peak = x[np.where(pdf == np.amax(pdf))]
    return peak

def get_diffusion_coef(traj_list, params):
    diffusion_coefs = []
    loc_precisions = []
    for traj in traj_list:
        if len(traj.path[:,0])<3:
            continue
        trajectory_length = len(traj.path[:,0])
        MSD = np.zeros(trajectory_length) # mean squared displacement
        n = np.zeros(trajectory_length) # used to measure number of trajectories of given length for weighting
        tau = np.zeros(trajectory_length) # times between MSDs
        track_lengths = np.zeros(trajectory_length)
        for i in range(trajectory_length-1):
            x = traj.path[:,0]*params.pixelSize
            y = traj.path[:,1]*params.pixelSize            
            square_diffs = (x[1+i:]-x[:trajectory_length-(i+1)])**2 + (y[1+i:]-y[:trajectory_length-(i+1)])**2
            MSD[i] = np.mean(square_diffs)
            track_lengths[i] = len(square_diffs)
            tau[i] = i*params.frameTime
        tau = tau[MSD!=0]
        track_lengths = track_lengths[MSD!=0]
        MSD = MSD[MSD!=0]
        if len(track_lengths)<3:
            continue
        weights = track_lengths.astype('float32') / float(np.amax(track_lengths))
        plt.plot(tau, MSD)
        # plt.show()
        popt, pcov = curve_fit(straightline, tau[:-1], MSD[:-1], p0=None, sigma=weights[:-1])
        diffusion_coefs.append(popt[0]/4.)
        if (popt[1]>0): loc_precisions.append(np.sqrt(popt[1])/4.)
    plt.show()
    return diffusion_coefs, loc_precisions


def plot_traj_intensities(spots):
    trajnums = []
    for spot in spots: trajnums.append(spot.traj_num)
    print(trajnums)
    ntraj = np.amax(trajnums[1]) #np.amax(np.amax(trajnums))
    for traj in range(ntraj):
        intensity = []
        for spot in spots:
            for k in range(len(spot.traj_num)):
                if spot.traj_num[k] == traj: intensity.append(spot.spot_intensity[k])
        plt.plot(intensity)
    plt.show()
