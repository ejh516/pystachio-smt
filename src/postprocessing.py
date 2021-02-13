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

def plot_snr(snr):
    snr = snr[snr > 1]
    bandwidth=0.07
    kde = gaussian_kde(snr, bw_method=bandwidth)
    x = np.linspace(0, np.amax(snr), 10000)
    pdf = kde.evaluate(x)
    fig, ax1 = plt.subplots()
    ax1.hist(snr, bins=np.arange(0,np.amax(snr)+2,2), label="Raw data")
    ax2 = ax1.twinx()
    ax2.plot(x, pdf, 'k-', label="Gaussian KDF")
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,2))
    plt.legend()
    plt.show()
    peak = x[np.where(pdf == np.amax(pdf))]
    return peak


def get_isingle(intensities):
    intensities = intensities[intensities > 1]
    bandwidth=0.07
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
        trajectory_length = traj.length
        if trajectory_length<params.MSD_num_points+1:
            continue       
        MSD = np.zeros(trajectory_length-1) # mean squared displacement
        n = np.zeros(trajectory_length-1) # used to measure number of trajectories of given length for weighting
        tau = np.zeros(trajectory_length-1) # times between MSDs
        track_lengths = np.zeros(trajectory_length-1)
        x = np.array(traj.path)[:,0]*params.pixelSize
        y = np.array(traj.path)[:,1]*params.pixelSize      
        for i in range(1,trajectory_length):
            sqd = (x[i:]-x[:trajectory_length-i])**2 + (y[i:]-y[:trajectory_length-i])**2
            MSD[i-1] = np.mean(sqd)
            track_lengths[i-1] = len(sqd)
            tau[i-1] = i*params.frameTime
        tau = tau[:params.MSD_num_points]
        MSD = MSD[:params.MSD_num_points]        
        track_lengths = track_lengths[:params.MSD_num_points]
        weights = track_lengths[:params.MSD_num_points].astype('float32') / float(np.amax(track_lengths[:params.MSD_num_points]))
        plt.plot(tau, MSD)
        try:
            popt, pcov = curve_fit(straightline, tau, MSD, p0=[1,0], sigma=weights)
            if popt[0]>0: diffusion_coefs.append(popt[0]/4.)
            if (popt[1]>0): loc_precisions.append(np.sqrt(popt[1])/4.)
        except:
            print("oh no")
    plt.show()
    plt.hist(diffusion_coefs)
    plt.show()
    return diffusion_coefs, loc_precisions


def plot_traj_intensities(trajs):
    for traj in trajs:
        plt.plot(traj.intensity)
    plt.show()
    
def get_stoichiometries(trajs, isingle, params):
    # Let's do the easy part first - the ones where they do not start at the start
    stoics = []
    for traj in trajs:
        if traj.length ==1: continue
        if traj.start_frame != 0:
            traj.stoichiometry = traj.intensity[0] / isingle
        else:
            if params.stoic_method == "initial":
                #Initial intensity
                traj.stoichiometry = traj.intensity[0] / isingle
            elif params.stoic_method == "mean":
                # Mean of first N frames
                traj.stoichiometry = np.mean(traj.intensity[:params.num_stoic_frames]) / isingle
            elif params.stoic_method == "linear_fit":
                if traj.length < params.num_stoic_frames:
                    xdata = np.arange(1,traj.length+1,dtype='float')*params.frameTime
                    ydata = traj.intensity[:traj.length]
                    popt, pcov = curve_fit(straightline, xdata, ydata)
                else:
                    xdata = np.arange(1,params.num_stoic_frames+1,dtype='float')*params.frameTime
                    ydata = traj.intensity[:params.num_stoic_frames]
                    popt, pcov = curve_fit(straightline, xdata, ydata)
                intercept = popt[1]
                if intercept > 0:
                    traj.stoichiometry = intercept / isingle
                else:
                    traj.stoichiometry = traj.intensity[0] / isingle
        stoics.append(traj.stoichiometry)
    stoics=np.array(stoics)
    plt.hist(np.round(stoics), bins=np.arange(0,10,0.5))
    plt.xticks(range(0,11))
    plt.show()
    plt.scatter(range(len(stoics)),  stoics)
    plt.show()
    return 0
