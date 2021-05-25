"""
Post processing trajectories and intensities

Routines for getting isingle and diffusion coefficient from lists of intensities

v0.1 Jack W Shepherd, University of York
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
from scipy.spatial import distance_matrix
import os
import trajectories, images
import cv2

def postprocess(params, simulated=False, stepwise=False):
    if not params.ALEX:
        trajs = []
        if False: #simulated:
            trajs = trajectories.read_trajectories(params.seed_name + "_simulated_trajectories.tsv")
        else:
            trajs = trajectories.read_trajectories(params.seed_name + "_trajectories.tsv")
        spots = trajectories.to_spots(trajs)
        print(f"Looking at {len(trajs)} trajectories across {len(spots)} frames")

        intensities = np.array([])
        snrs = np.array([])
        for i in range(len(spots)):
            tmp = spots[i].spot_intensity
            tmp_snr = spots[i].snr
            intensities = np.concatenate((intensities,tmp))
            snrs = np.concatenate((snrs,tmp_snr))

        if params.calculate_isingle:
            calculated_isingle = get_isingle(params,intensities)
        else:
            calculated_isingle = params.Isingle
        calculated_snr = plot_snr(params,snrs)
        dc, lp = get_diffusion_coef(trajs, params)
        if simulated:
            print(f"Simulated diffusion coefficient: {np.mean(dc)}")
            print(f"Simulated Isingle:               {calculated_isingle[0]}")
        else:
            print(f"Tracked diffusion coefficient: {np.mean(dc)}")
            #print(f"Tracked Isingle:               {calculated_isingle[0]}")

        plot_traj_intensities(params, trajs)
        get_stoichiometries(trajs, calculated_isingle, params, stepwise_sim=stepwise)
        if params.copy_number==True: get_copy_number(params, calculated_isingle)
        
        overtrack(params, trajs)

    elif params.ALEX:
        if params.colocalise==True:
            Rtrajs = trajectories.read_trajectories(params.seed_name + "_Rchannel_trajectories.tsv")
            Ltrajs = trajectories.read_trajectories(params.seed_name + "_Lchannel_trajectories.tsv")
            Rspots = trajectories.to_spots(Rtrajs)
            Lspots = trajectories.to_spots(Ltrajs)

            Rintensities= np.array([])
            Rsnrs = np.array([])
            Rintensities= np.array([])
            Rsnrs = np.array([])
            Lintensities= np.array([])
            Lsnrs = np.array([])
            Lintensities= np.array([])
            Lsnrs = np.array([])         
            for i in range(len(Rspots)):
                Rintensities = np.concatenate((Rintensities,Rspots[i].spot_intensity))
                Rsnrs = np.concatenate((Rsnrs,Rspots[i].snr))
            for i in range(len(Lspots)):
                Lintensities = np.concatenate((Lintensities,Lspots[i].spot_intensity))
                Lsnrs = np.concatenate((Lsnrs,Lspots[i].snr))            
            if params.calculate_isingle:
                R_isingle = get_isingle(params,Rintensities, channel="R")
                L_isingle = get_isingle(params,Lintensities, channel="L")
            else:
                R_isingle = params.R_isingle
                L_isingle = params.L_isingle

            L_calculated_snr = plot_snr(params,Lsnrs, channel="L")
            R_calculated_snr = plot_snr(params,Rsnrs, channel="R")
            Ldc, Llp = get_diffusion_coef(Ltrajs, params, channel="L")
            Rdc, Rlp = get_diffusion_coef(Rtrajs, params, channel="R")
            plot_traj_intensities(params, Ltrajs, channel="L")
            plot_traj_intensities(params, Rtrajs, channel="R")
            get_stoichiometries(Ltrajs, L_isingle, params, stepwise_sim=stepwise, channel="L")
            get_stoichiometries(Rtrajs, R_isingle, params, stepwise_sim=stepwise, channel="R")
            
            if params.copy_number==True: 
                get_copy_number(params, Lcalculated_isingle, channel="L")
                get_copy_number(params, Rcalculated_isingle, channel="R")

            if params.colocalise: colocalise(params, Ltrajs, Rtrajs)

    else: sys.exit("ERROR: look do you want ALEX or not?\nSet params.ALEX=True or False")

def overtrack(params, trajs):
    image_data = images.ImageData()
    image_data.read(params)
    outfile = params.seed_name+"_overtracked_trajectory_intensities.tsv"
    f = open(outfile, 'w')
    f.write("Trajectory ID\tFrame\tIntensity\n")
    for traj in trajs:
        ints = traj.intensity
        final_position = traj.path[-1]
        x = round(final_position[0])
        y = round(final_position[1])
        final_frame = traj.end_frame
        for frame in range(final_frame+1,final_frame+11):
            image = image_data.pixel_data[frame,:,:]
            # Create a tmp array with the centre of the spot in the centre
            tmp = image[
                y - params.subarray_halfwidth : y + params.subarray_halfwidth+1, 
                x - params.subarray_halfwidth : x + params.subarray_halfwidth + 1
            ] 
            spotmask = np.zeros(tmp.shape)
            cv2.circle(spotmask, 
                    (params.subarray_halfwidth, params.subarray_halfwidth),
                    params.inner_mask_radius,
                    1,
                    -1
            )
            bgintensity = np.mean(tmp[spotmask == 0])
            tmp = tmp - bgintensity
            intensity = np.sum(tmp[spotmask == 1])
            ints.append(intensity/10**5)
        # for i in range(len(ints)):
        #     outstr = str(traj.id) + "\t" + str(traj.start_frame+i) + "\t" + str(ints[i]) + "\n"
        #     f.write(outstr)
        plt.plot(ints, lw=1, label="Trajectory "+str(traj.id))
    plt.title("Overtracked trajectories")
    plt.xlabel("Trajectory frame number")
    plt.ylabel("Intensity (a.u.)")
    # plt.legend()
    plt.savefig(params.seed_name+"overtracked_trajectory_intensities_plot.png", dpi=300)
            
    
def colocalise(params, Ltrajs, Rtrajs):
    image_data = images.ImageData()
    image_data.read(params)
    imageL=np.zeros((image_data.num_frames//2,image_data.frame_size[1],image_data.frame_size[0]//2))
    imageR=np.zeros((image_data.num_frames//2,image_data.frame_size[1],image_data.frame_size[0]//2))
    if params.start_channel=='L':
        for i in range(0,image_data.num_frames-1,2):
            imageL[i//2,:,:] = image_data.pixel_data[i,:,:image_data.frame_size[0]//2]
            imageR[i//2,:,:] = image_data.pixel_data[i+1,:,image_data.frame_size[0]//2:]
    else:
        for i in range(0,image_data.num_frames-1,2):
            imageR[i//2,:,:] = image_data.pixel_data[i,:,:image_data.frame_size[0]//2]
            imageL[i//2,:,:] = image_data.pixel_data[i+1,:,image_data.frame_size[0]//2:]
    Llinks = []
    Rlinks = []
    nlinks = []
    for i in range(params.num_frames):
        s1 = []
        s2 = []
        for traj in Ltrajs:
            if traj.start_frame<=i and traj.end_frame>=i:
                s1.append([traj.path[i-traj.start_frame],traj.width,traj.id])
        for traj in Rtrajs:
            if traj.start_frame<=i and traj.end_frame>=i:
                s2.append([traj.path[i-traj.start_frame],traj.width,traj.id])
        id1, id2 = linker(params,s1,s2)
        for j in range(len(id1)):
            found = False
            if id1[i] in Llinks:
                indices = np.where(Llinks==id1)
                for index in indices:
                    if Rlinks[index]==id2[j]:
                        nlinks[index] += 1
                        found = True
            if found == False:
                Llinks.append(id1[j])
                Rlinks.append(id2[j])
                nlinks.append(1)
    outfile = params.seed_name + "_colocalized_trajectories.tsv"
    f = open(outfile, 'w')
    f.write("Left_traj\tRight_traj\n_frames")
    for i in range(len(Llinks)):
        if nlinks[i]>=params.colocalize_n_frames:
            f.write("$i\t%i\t%i"%(Llinks[i], Rlinks[i], nlinks[i]))
            
                        
                        
    colors = ['r','b','g','m','y','c']
    c = 0
    z, y, x = imageL.shape
    disp_frame = np.zeros((y,2*x))
    disp_frame[:,:x] = imageL[1,:,:]
    disp_frame[:,x:] = imageR[1,:,:]
    plt.imshow(disp_frame, cmap="Greys_r")
    plt.plot([x,x],[0,x], 'w--')
    plt.xticks([])
    plt.yticks([])
    plt.ylim([0,x])
    plt.show()
    plt.imshow(disp_frame, cmap="Greys_r")
    for traj in Ltrajs:
        if traj.id in id1:
            plt.scatter(traj.path[0][0], traj.path[0][1], 10, marker='x', color=colors[c])
            for t2 in Rtrajs:
                index = np.where(id1==traj.id)[0][0]
                if t2.id == id2[index]:
                    plt.scatter(t2.path[0][0]+x, t2.path[0][1], 10, marker='x', color=colors[c])
            c+=1
    plt.yticks([])
    plt.xticks([])
    plt.plot([x,x],[0,x], 'w--')
    plt.ylim([0,x])
    plt.savefig("colocalised_spots.png", dpi=300)
    plt.show()

def linker(params, spots1, spots2): #spots1 and spots2 are arrays going xpos, ypos, xwidth, ywidth, traj#
    s1_pos = []
    s2_pos = []
    s1_width = []
    s2_width = []
    for i in range(len(spots1[:])): 
        s1_pos.append(spots1[i][0])
        s1_width.append(spots1[i][1])
    for i in range(len(spots2[:])): 
        s2_pos.append(spots2[i][0])
        s2_width.append(spots2[i][1])
    dm = distance_matrix(s1_pos,s2_pos)
    dm[dm>params.colocalise_distance]=-1
    overlap = np.zeros(dm.shape)
    for i in range(len(s1_pos)):
        for j in range(len(s2_pos)):
            if dm[i,j] >= 0:
                overlap[i,j] = np.exp(-dm[i,j]**2 / (2.*((0.5*(s1_width[i][0][0]+s1_width[i][0][1])**2+(0.5*(s2_width[i][0][0]+s2_width[i][0][1])**2 )))))
    overlap[overlap<0.75]=0
    indices = np.where(overlap!=0)
    id1=[];id2=[]
    for i in range(len(indices[0])):
        id1.append(spots1[indices[0][i]][2])
        id2.append(spots2[indices[0][i]][2])
    return np.array(id1), np.array(id2)


def straightline(x, m, c):
    return m * x + c

def get_copy_number(params, calculated_isingle, channel=None):
    image_data = images.ImageData()
    image_data.read(params)
    frame =image_data.pixel_data[spots.laser_on_frame,:,:]
    copy_nums = []
    f = open(params.seed_name + "_copy_numbers.tsv")
    f.write("Cell\tCopy number\n")
    bg = np.mean(frame[image_data.mask==0])
    for i in range(1,np.amax(image_data.mask_data)+1):
        copy_nums.append(np.sum(frame[image_data.mask_data==i])/calculated_isingle)
        f.write(str(i)+"\t"+str(copy_nums[i-1])+"\n")
    f.close()
    # import tifffile as tiff
    # copy_nums = []
    # f = open(params.seed_name + "_copy_numbers.tsv", 'w')
    # f.write("Cell\tCopy number\n")
    # for sim in range(1,11):
    #     image_data = tiff.imread("../data/Data4Jack/simImages/"+str(sim)+".tif")
    #     mask = tiff.imread("../data/Data4Jack/simImages/"+str(sim)+"_mask.tif")
    #     bg = np.mean(image_data[mask==0])
    #     copy_nums.append(np.sum(image_data[mask>0]-bg)/calculated_isingle)
    # for i in range(1,11):
    #     f.write(str(i)+"\t"+str(copy_nums[i-1])+"\n")
    # f.close()

def plot_snr(params,snr,channel=None):
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
    if channel=="L": 
        plt.title("Left hand channel SNR plot")
        outseed = params.seed_name + "Lchannel_SNR"
    elif channel=="R":
        plt.title("Right hand channel SNR plot")
        outseed = params.seed_name + "Rchannel_SNR"
    else:
        plt.title("Whole frame SNR plot")
        outseed = params.seed_name + "_SNR"
    plt.savefig(outseed+"_plot.png", dpi=300)
    plt.show()
    peak = x[np.where(pdf == np.amax(pdf))]
    ofile = params.seed_name + "_data.tsv"
    f = open(ofile, 'w')
    for i in range(len(snr)):
        f.write(str(snr[i])+"\n")
    f.close()
    return peak


def get_isingle(params, intensities, channel=None):
    scale = 5
    intensities = intensities[intensities > 1]
    bandwidth = 0.07
    kde = gaussian_kde(intensities, bw_method=bandwidth)
    x = np.linspace(0, np.amax(intensities), 10000)
    pdf = kde.evaluate(x)
    peak = x[np.where(pdf == np.amax(pdf))].astype('int')
    peakval = np.amax(pdf)
    fig, ax1 = plt.subplots()
    plt.xlabel("Intensity (camera counts per pixel x$10^%i$)"%(scale))
    plt.ylabel("Number of foci")
    l1 = ax1.hist(
        intensities/10**scale,
        bins=np.arange(0, np.amax(intensities/10**scale) + 100/10**scale, 100/10**scale),
        label="Raw data", color="gray"
    )
    ax2 = ax1.twinx()
    l2 = ax2.plot(x/10**scale, pdf*10**scale, "k-", label="Gaussian KDE")
    plt.ylabel("Probability density (a.u.)")
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 2))
    l3 = ax1.plot([peak/10**scale,peak/10**scale],[0,10], 'r--', label="Isingle", lw=2)
    if channel=="L": 
        plt.title("Left hand channel intensity plot\nIsingle = %i"%(np.round(peak)))
        outseed = params.seed_name + "Lchannel_intensities"
    elif channel=="R":
        plt.title("Right hand channel intensities plot\nIsingle = %i"%(np.round(peak)))
        outseed = params.seed_name + "Rchannel_intensity"
    else:
        plt.title("Whole frame intensities\nIsingle = %i"%(np.round(peak)))
        outseed = params.seed_name + "_intensity"
    lns = l2+l3
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    plt.savefig(outseed+"_plot.png", dpi=300)   
    plt.show()
    ofile = outseed + "_data.tsv"
    f = open(ofile, 'w')
    for i in range(len(intensities)):
        f.write(str(intensities[i])+"\n")
    f.close()
    return peak


def get_diffusion_coef(traj_list, params, channel=None):
    diffusion_coefs = []
    loc_precisions = []
    for traj in traj_list:
        trajectory_length = traj.length
        if trajectory_length < params.MSD_num_points + 1:
            continue
        MSD = np.zeros(trajectory_length - 1)  # mean squared displacement
        n = np.zeros(
            trajectory_length - 1
        )  # used to measure number of trajectories of given length for weighting
        tau = np.zeros(trajectory_length - 1)  # times between MSDs
        track_lengths = np.zeros(trajectory_length - 1)
        x = np.array(traj.path)[:, 0] * params.pixelSize
        y = np.array(traj.path)[:, 1] * params.pixelSize
        for i in range(1, trajectory_length):
            sqd = (x[i:] - x[: trajectory_length - i]) ** 2 + (
                y[i:] - y[: trajectory_length - i]
            ) ** 2
            MSD[i - 1] = np.mean(sqd)
            track_lengths[i - 1] = len(sqd)
            tau[i - 1] = i * params.frameTime
        tau = tau[: params.MSD_num_points]
        MSD = MSD[: params.MSD_num_points]
        track_lengths = track_lengths[: params.MSD_num_points]
        weights = track_lengths[: params.MSD_num_points].astype("float32") / float(
            np.amax(track_lengths[: params.MSD_num_points])
        )
        plt.plot(tau, MSD)
        plt.xlabel(r"$\tau$")
        plt.ylabel("MSD ($\mu$m$^2$)")
        try:
            popt, pcov = curve_fit(straightline, tau, MSD, p0=[1, 0], sigma=weights)
            # if popt[0] > 0:
            diffusion_coefs.append(popt[0] / 4.0)
            if popt[1] > 0:
                loc_precisions.append(np.sqrt(popt[1]) / 4.0)
        except:
            print("oh no")
    plt.show()
    plt.hist(diffusion_coefs)
    plt.xlabel("Diffusion coefficient ($\mu$m$^{2}$s$^{-1}$)")
    plt.ylabel("Number of foci trajectories")
    if channel=="L":
        plt.title("Left channel diffusion coefficients\nMean = %3.2f"%(np.mean(diffusion_coefs)))
        ofile = params.seed_name+"_Lchannel_diff_coeff.png"
    elif channel=="R":
        plt.title("Right channel diffusion coefficients\nMean = %3.2f"%(np.mean(diffusion_coefs)))
        ofile = params.seed_name+"_Rchannel_diff_coeff.png"
    else:
        plt.title("Whole frame diffusion coefficients\nMean = %3.2f"%(np.mean(diffusion_coefs)))
        ofile = params.seed_name+"_diff_coeff.png"
    plt.savefig(ofile, dpi=300)
    plt.show()
    f = open(params.seed_name + "_diff_coeff_data.tsv", "w")
    for i in range(len(diffusion_coefs)):
        f.write(str(float(diffusion_coefs[i]))+"\n")
    f.close()
    f = open(params.seed_name + "_diff_coeff_loc_precision_data.tsv", "w")
    for i in range(len(loc_precisions)):
        f.write(str(float(loc_precisions[i]))+"\n")
    f.close()
    return diffusion_coefs, loc_precisions


def plot_traj_intensities(params, trajs, channel=None):
    for traj in trajs:
        t = traj.intensity
        for i in range(len(t)):
            t[i] /= 10**5
        plt.plot(t)
    plt.xlabel("Frame number")
    plt.ylabel("Intensity (camera counts per pixel x$10^5$)")
    if channel=="L":
        plt.title("Left channel trajectory intensity")
        ofile = params.seed_name+"_Lchannel_trajectory_intensities.png"
    elif channel=="R":
        plt.title("Right channel trajectory intensity")
        ofile = params.seed_name+"_Rchannel_trajectory_intensities.png"
    else:
        # plt.title("Whole frame trajectory intensity")
        ofile = params.seed_name+"_trajectory_intensities.png"
    plt.savefig(ofile, dpi=300)
    plt.show()


def get_stoichiometries(trajs, isingle, params, stepwise_sim=False, channel=None):
    # Let's do the easy part first - the ones where they do not start at the start
    stoics = []
    startframe = 100000
    for traj in trajs:
        if traj.start_frame<startframe and traj.length>=params.num_stoic_frames: startframe=traj.start_frame
        print(startframe)
    for traj in trajs:
        if traj.length <params.num_stoic_frames:
            continue
        if params.stoic_method == "initial":
            # Initial intensity
            traj.stoichiometry = traj.intensity[0] / isingle
        elif params.stoic_method == "mean":
            # Mean of first N frames
            traj.stoichiometry = (
                np.mean(traj.intensity[: params.num_stoic_frames]) / isingle
                )
        elif params.stoic_method == "linear_fit":
            if traj.start_frame-startframe>4:
                continue #stoics.append(traj.intensity[0] / isingle)
            else:
                xdata = (
                    np.arange(0, params.num_stoic_frames , dtype="float")
                    # * params.frameTime
                )
                ydata = traj.intensity[0: params.num_stoic_frames]
                popt, pcov = curve_fit(straightline, xdata, ydata)
                intercept = popt[1]
                if intercept > 0 and popt[0]<0 and startframe!=100000:
                    traj.stoichiometry = (intercept + abs((traj.start_frame-startframe)*popt[0])) / isingle
                    # traj.stoichiometry = intercept/isingle
                else:
                    continue 
                    # traj.stoichiometry = traj.intensity[0] / isingle
                stoics.append(traj.stoichiometry)
    stoics = np.array(stoics)
    max_stoic = int(np.amax(np.round(stoics)))
    plt.hist(np.round(stoics), bins=np.arange(0, np.amax(np.round(stoics)+1), 1))
    plt.xticks(range(0,max_stoic+1))
    plt.xlabel("Rounded stoichiometry")
    plt.ylabel("N")
    if channel=="L":
        plt.title("Left channel stoichiometry")
        oseed = params.seed_name+"_Lchannel_stoichiometry"
    elif channel=="R":
        plt.title("Right channel stoichiometry")
        oseed = params.seed_name+"_Rchannel_stoichiometry"
    else:
        plt.title("Whole frame stoichiometry")
        oseed = params.seed_name+"_stoichiometry"
    plt.savefig(oseed+"_histogram.png", dpi=300)
    plt.show()
    plt.scatter(range(len(stoics)), stoics)
    plt.xlabel("Spot #")
    plt.ylabel("Raw stoichiometry")
    if channel=="L":
        plt.title("Left channel stoichiometry")
        oseed = params.seedname+"_Lchannel_stoichiometry"
    elif channel=="R":
        plt.title("Right channel stoichiometry")
        oseed = params.seedname+"_Rchannel_stoichiometry"
    else:
        plt.title("Whole frame stoichiometry")
        oseed = params.seed_name+"_stoichiometry"
    plt.savefig(oseed+"_scatter.png", dpi=300)
    plt.show()
    f = open(oseed + "_data.tsv", "w")
    for i in range(len(stoics)):
        f.write(str(float(stoics[i]))+"\n")
    f.close()
    return 0
