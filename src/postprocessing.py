"""
Post processing trajectories and intensities

Routines for getting isingle and diffusion coefficient from lists of intensities

v0.1 Jack W Shepherd, University of York
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde

import trajectories

def postprocess(params, simulated=False):
    trajs = []
    name = params.get('general', 'name')
    if simulated:
        trajs = trajectories.read_trajectories(name + "_simulated_trajectories.tsv")
    else:
        trajs = trajectories.read_trajectories(name + "_trajectories.tsv")

    spots = trajectories.to_spots(trajs)
    print(f"Looking at {len(trajs)} trajectories across {len(spots)} frames")
    intensities = np.array([])
    snrs = np.array([])
    for i in range(len(spots)):
        tmp = spots[i].spot_intensity
        tmp_snr = spots[i].snr
        intensities = np.concatenate((intensities,tmp))
        snrs = np.concatenate((snrs,tmp_snr))

    calculated_snr = plot_snr(snrs)

    calculated_isingle = get_isingle(intensities)
    dc, lp = get_diffusion_coef(trajs, params)

    if simulated:
        print(f"Simulated diffusion coefficient: {np.mean(dc)}")
        print(f"Simulated Isingle:               {calculated_isingle[0]}")
    else:
        print(f"Tracked diffusion coefficient: {np.mean(dc)}")
        print(f"Tracked Isingle:               {calculated_isingle[0]}")

    plot_traj_intensities(trajs)
    get_stoichiometries(trajs, calculated_isingle, params)


def straightline(x, m, c):
    return m * x + c


def plot_snr(snr):
    bandwidth=0.07
    kde = gaussian_kde(snr[snr != 0], bw_method=bandwidth)
    x = np.linspace(0, np.amax(snr), 10000)
    pdf = kde.evaluate(x)
    fig, ax1 = plt.subplots()
    ax1.hist(snr[snr != 0], bins=np.arange(0,np.amax(snr)+2,0.05), label="Raw data")
    ax2 = ax1.twinx()
    ax2.plot(x, pdf, 'k-', label="Gaussian KDF")
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,2))
    plt.legend()
    plt.show()
    peak = x[np.where(pdf == np.amax(pdf))]
    return peak


def get_isingle(intensities):
    intensities = intensities[intensities > 1]
    bandwidth = 0.07
    kde = gaussian_kde(intensities, bw_method=bandwidth)
    x = np.linspace(0, np.amax(intensities), 10000)
    pdf = kde.evaluate(x)
    peak = x[np.where(pdf == np.amax(pdf))]
    fig, ax1 = plt.subplots()
    plt.xlabel("Intensity (a.u.)")
    plt.ylabel("N")
    ax1.hist(
        intensities,
        bins=np.arange(0, np.amax(intensities) + 100, 100),
        label="Raw data", color="gray"
    )
    ax2 = ax1.twinx()
    ax2.plot(x, pdf, "k-", label="Gaussian KDF")
    plt.ylabel("Probability")
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 2))
    ax1.plot([peak,peak],[0,8], 'r--', label="Isingle", lw=2)
    plt.legend()    
    plt.show()
    return peak


def get_diffusion_coef(traj_list, params):
    MSD_num_points = params.get('postprocessing', 'msd_num_points')
    pixel_size = params.get('image', 'pixel_size')
    frame_time = params.get('image', 'frame_time')
    diffusion_coefs = []
    loc_precisions = []
    for traj in traj_list:
        trajectory_length = traj.length
        if trajectory_length < MSD_num_points + 1:
            continue
        MSD = np.zeros(trajectory_length - 1)  # mean squared displacement
        n = np.zeros(
            trajectory_length - 1
        )  # used to measure number of trajectories of given length for weighting
        tau = np.zeros(trajectory_length - 1)  # times between MSDs
        track_lengths = np.zeros(trajectory_length - 1)
        x = np.array(traj.path)[:, 0] * pixel_size
        y = np.array(traj.path)[:, 1] * pixel_size
        for i in range(1, trajectory_length):
            sqd = (x[i:] - x[: trajectory_length - i]) ** 2 + (
                y[i:] - y[: trajectory_length - i]
            ) ** 2
            MSD[i - 1] = np.mean(sqd)
            track_lengths[i - 1] = len(sqd)
            tau[i - 1] = i * frame_time
        tau = tau[: MSD_num_points]
        MSD = MSD[: MSD_num_points]
        track_lengths = track_lengths[: MSD_num_points]
        weights = track_lengths[: MSD_num_points].astype("float32") / float(
            np.amax(track_lengths[: MSD_num_points])
        )
        plt.plot(tau, MSD)
        plt.xlabel(r"$\tau$")
        plt.ylabel("MSD ($\mu$m$^2$)")
        try:
            popt, pcov = curve_fit(straightline, tau, MSD, p0=[1, 0], sigma=weights)
            if popt[0] > 0:
                diffusion_coefs.append(popt[0] / 4.0)
            if popt[1] > 0:
                loc_precisions.append(np.sqrt(popt[1]) / 4.0)
        except:
            print("oh no")
    plt.show()
    plt.hist(diffusion_coefs)
    plt.xlabel("Diffusion coefficient ($\mu$m$^{2}$s$^{-1}$)")
    plt.ylabel("N")
    plt.show()
    return diffusion_coefs, loc_precisions


def plot_traj_intensities(trajs):
    for traj in trajs:
        t = traj.intensity[1:]
        plt.plot(t)
    plt.xlabel("Frame number")
    plt.ylabel("Intensity (a.u.)")
    plt.show()


def get_stoichiometries(trajs, isingle, params):
    stoic_method = params.get('postprocessing', 'stoic_method')
    num_stoic_frames = params.get('postprocessing', 'num_stoic_frames')
    frame_time = params.get('image', 'frame_time')
    # Let's do the easy part first - the ones where they do not start at the start
    stoics = []
    for traj in trajs:
        if traj.length == 1:
            continue
        if False: #traj.start_frame != 0:
            traj.stoichiometry = traj.intensity[0] / isingle
        else:
            if stoic_method == "Initial":
                # Initial intensity
                traj.stoichiometry = traj.intensity[0] / isingle
            elif stoic_method == "Mean":
                # Mean of first N frames
                traj.stoichiometry = (
                    np.mean(traj.intensity[: num_stoic_frames]) / isingle
                )
            elif stoic_method == "Linear":
                if traj.length <= num_stoic_frames:
                    xdata = (
                        np.arange(1, traj.length, dtype="float") * frame_time
                    )
                    ydata = traj.intensity[1: traj.length]
                    popt, pcov = curve_fit(straightline, xdata, ydata)
                else:
                    xdata = (
                        np.arange(1, num_stoic_frames + 1, dtype="float")
                        * frame_time
                    )
                    ydata = traj.intensity[1: num_stoic_frames+1]
                    popt, pcov = curve_fit(straightline, xdata, ydata)
                intercept = popt[1]
                if intercept > 0:
                    traj.stoichiometry = intercept / isingle
                else:
                    traj.stoichiometry = traj.intensity[0] / isingle
        stoics.append(traj.stoichiometry)
    stoics = np.array(stoics)
    plt.hist(np.round(stoics)) #, bins=np.arange(0, 10, 0.5))
    plt.xticks(range(0, 11))
    plt.xlabel("Rounded stoichiometry")
    plt.ylabel("N")
    plt.show()
    plt.scatter(range(len(stoics)), stoics)
    plt.xlabel("Spot #")
    plt.ylabel("Raw stoichiometry")
    plt.show()
    return 0
