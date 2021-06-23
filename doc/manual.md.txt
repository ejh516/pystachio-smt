# PySTACHIO: Python Single molecule TrAcking, stoiCHiometry, Intensity and simulatiOn
# Manual

## Introduction

PySTACHIO is a single-particle tracking and analysis program written in Python 3 using standard free libraries such as numpy. It is based on earlier implementations usually known in our publications as ADEMSCode. 

In this manual we will look at the overall workflow and the key changeable parameters for using the software on the command line. Although we have a GUI with most of the same functionality, we expect that most serious users will prefer the flexibility and power of the command line interface which, when learned, will be trivially scriptable and therefore quicker to analyse large datasets. As a consequence, this manual focuses largely on command line operation. Most of the same parameters may be set via the GUI however, and their descriptions, functions, and caveats all remain the same.

However you wish to use PySTACHIO, it is of vital importance to get parameters set correctly to avoid false positives during tracking, so in practice for each set of experiments it is necessary to explore parameter space. While we have set sensible (for our lab) defaults they should not be trusted blindly. There are some key questions you should probably ask yourself before you get started:

* What is my frame size and image sequence length?
* What is the exposure time?
* What is my expected SNR for a single molecule? (This is usually set with some sort of trial-and-improvement or convergence test but it usually makes sense to have a sensible initial guess)
* What outputs am I wanting to measure/what do I expect?
* Is PySTACHIO the right package for me?
* Can my data be spatially trimmed to improve performance, e.g. by cropping the frame to only contain the laser-illuminated spot or remove an unused colour channel?

Similarly, once you have run PySTACHIO you would do well to ask another set of questions:

* If calculated, does that Isingle make sense? This is fairly easily checked by manually selected a spot in ImageJ and working it out by hand
* Does that diffusion coefficient make sense?
* Do those trajectories seem to agree with what my eyes see?

If the answer to any of those is 'no' then you should tweak the parameter set and rerun. This is why command line operation and scripting is so useful - you can decide in advance one parameter to vary, and write a trivial script to do it for you. For example, if I needed to check the effect of changing SNR\_filter\_cutoff from 0.4 to 1.0 in steps of 0.1, in `bash` I would write:

	#!/usr/bin/env bash
	froot='/path/to/my/data' # Note: no .tif extension, just the file root
	for snr in `seq 0.4 0.1 1.0`; do
	    python3 pystachio-smt track,postprocess $froot SNR_filter_cutoff=$snr
	    dir="SNR_"$snr
	    rm -rf $dir; mkdir $dir
	    mv *tsv *png $dir
    done

After running this script it is then possible to evaluate the right SNR\_filter\_cutoff to use in one go rather than changing the value blindly. With SNR\_filter\_cutoff then set, one can move on to converging another parameter if needed such as MAX_DISPLACEMENT. 

## Citing PySTACHIO
If you use PySTACHIO please cite our paper available at https://arxiv.org/abs/2103.10164 

Bibtex citation:

    @misc{shepherd2021pystachio,
      title={PySTACHIO: Python Single-molecule TrAcking stoiCHiometry Intensity and simulatiOn, a flexible, extensible, beginner-friendly and optimized program for analysis of single-molecule microscopy}, 
      author={Jack W Shepherd and Ed J Higgins and Adam J M Wollman and M C Leake},
      year={2021},
      eprint={2103.10164},
      archivePrefix={arXiv},
      primaryClass={q-bio.BM}
    }
    
Plain text citation:

Shepherd, Jack W., et al. "PySTACHIO: Python Single-molecule TrAcking stoiCHiometry Intensity and simulatiOn, a flexible, extensible, beginner-friendly and optimized program for analysis of single-molecule microscopy." arXiv preprint arXiv:2103.10164 (2021).

## Workflow

We assume you have read the quick-start guide - if not please do so before you jump in to this manual. Briefly, the PySTACHIO workflow is split into `tasks`, the most important of which for command line operation are simulation, tracking, and postprocessing. It is possible to do any one of these without the others providing the requisite data already exists, i.e. if you have tracked some data with the `track` task and which to reanalyse it later with modified `postprocess` task parameters this is easy to do. Imagining I want to do this two-step analysis, I could write in the terminal:

	$python3 pystachio-smt track /path/to/my/data
	$python3 pystachio-smt postprocess /path/to/my/data

which is exactly equivalent to:

	$python3 pystachio-smt track,postprocess /path/to/my/data
	
Note here that for postprocessing only, you  still only specify the path to the TIF file. PySTACHIO will then assume the locations and names of the tracking output files for postprocessing, so if you do this two-step method don't move or change files in between.

For example, imagining I want this time to observe the effect of MSD\_NUM\_POINTS on the diffusion coefficient I could write a bash script like this:

    #!/usr/bin/env bash
    	#!/usr/bin/env bash
	froot='/path/to/my/data'
	python3 pystachio-smt track $froot #converged keyword args here...
	for msd in `seq 3 6`; do
	    python3 pystachio-smt postprocess $froot MSD_NUM_POINTS=$msd
	    dir="MSD_"$msd
	    rm -rf $dir; mkdir $dir
	    mv *tsv *png $dir
    done

Here because the tracking and posprocessing are separated, I can track once and then postprocess many times, which can mean a big time saving depending on the dataset.

## Keyword Arguments

### General Parameters

**NUM_PROCS**: The number of CPU processes to run PySTACHIO on. Parallelism is done in a way analagous to OpenMP  
Default: 1  
Class: general  
Level: basic

**TASKS**: Which task(s) to perform. This is a list of tasks for PySTACHIO to execute and is made up of one or more tasks taken from simulate track postprocess view app where each task is separated by a comma but no space, e.g. track,postprocess. Note here that order matters! Tasks are executed left to right so simulate,track is different from track,simulate. In the former, you simulate data and then track it. In the latter, you look for a file, track it if it exists (crash if it doesn't) and then simulate data *and overwrite whatever it was you just tracked* – beware! If you run `pystachio-smt app` you launch the web app and can navigate to `localhost:8050` to use the GUI - this is in fact all the clickable shortcuts do.  
Default: []  
Class: general  
Level: basic

**NAME**: Name prefixing all files associated with this run  
Default:  
Class: general  
Level: basic

**I\_SINGLE**: I\_single value. For simulations, this is the Isingle for simulated spots. If tracking/postprocessing and this is set but calculate_isingle is False, this value will be used for stoichiometry and copy number analysis.  
Default: 10000.0  
Class: simulation  
Level: basic

**MASK_FILE**: Filename of an image mask for filtering spots. If not specified, no mask is used.  
Default:  
Class: general  
Level: basic

### Image Parameters

**FRAME_TIME**: Frame exposure time in seconds.  
Default: 0.005  
Class: image  
Level: basic

**PIXEL_SIZE**: Length of a pixel side expressed in &mu;m  
Default: 0.120  
Class: image  
Level: basic

**PSF_WIDTH**: Initial guess for the half width at half maximum of the Gaussian point spread function to fit to spots, expressed in &mu;m  
Default: 0.120  
Class: image  
Level: advanced

### Simulation Parameters

**NUM_FRAMES**: Number of frames to simulate  
Default: 10  
Class: image  
Level: basic

**FRAME_SIZE**: Size of frame to simulate ([x,y]) in pixels  
Default: [100, 100]   
Class: image   
Level: basic

**NUM_SPOTS**: Number of spots to simulate  
Default: 10  
Class: simulation  
Level: basic

**PHOTOBLEACH**: Perform photobleaching during simulations (alias for `max_spot_molecules=10, p_bleach_per_frame=0.05`)  
Default: False  
Class: simulation  
Level: basic

**DIFFUSION_COEFF**: Diffusion coefficient to simulate for non-static simulations  
Default: 1.0  
Class: simulation  
Level: basic

**BG_MEAN**: Mean of the Gaussian part of the background intensity to simulate  
Default: 500.0  
Class: simulation  
Level: advanced

**BG_STD**: Standard deviation of the Gaussian part of the background pixel intensity to simulate  
Default: 120.0  
Class: simulation  
Level: advanced

**SPOT_WIDTH**: Width of the simulated Gaussian point spread function in &mu;m  
Default: 1.33  
Class: simulation  
Level: advanced

**MAX\_SPOT\_MOLECULES**: Maximum number of dye molecules to simulate per spot  
Default: 1  
Class: simulation  
Level: advanced

**P\_BLEACH\_PER\_FRAME**: Probability of a spot bleaching in a given simulated frame  
Default: 0.0  
Class: simulation  
Level: advanced

### Tracking Parameters

**START_FRAME**: The first frame of the image stack to analyse  
Default: 0  
Class: image  
Level: basic

**END_FRAME**: The last frame of the image stack to analyse (-1 = use all frames)  
Default: -1  
Class: image  
Level: basic

**CHANNEL_SPLIT** If/how the frames are split spatially  
Default: None  
Class: image  
Level: basic

**ALEX**: Perform Alternating-Laser experiment analysis. If set, you must also set CHANNEL_SPLIT  
Default: False  
Class: image  
Level: basic

**START_CHANNEL**: If ALEX=True, this sets which channel (L or R) is illuminated in the first frame.  
Default: L  
Class: image  
Level: basic

**SNR\_FILTER\_CUTOFF**: Cutoff value when filtering spots by signal/noise ratio. Defined as  
Default: 0.4  
Class: tracking  
Level: basic

**BW\_THRESHOLD\_TOLERANCE**: Threshold for generating the black/white image relative to the peak intensity  
Default: 1.0  
Class: tracking  
Level: advanced

**FILTER_IMAGE**: Method for filtering the input image pre-analysis  
Options: 'Gaussian', 'None'  
Default: 'Gaussian'  
Class: tracking  
Level: advanced

**MAX_DISPLACEMENT**: Maximum displacement allowed for spots to be linked between successive frames, expressed in pixels  
Default: 5.0  
Class: tracking  
Level: advanced

**STRUCT\_DISK\_RADIUS**: Radius of the disk structural element, expressed in pixels  
Default: 5.0  
Class: tracking  
Level: advanced

**MIN\_TRAJ\_LEN**: Minimum number of frames needed to define a trajectory. Trajectories shorter than this will be discarded and not analysed. Expressed in frames  
Default: 3  
Class: tracking  
Level: advanced

**INNER\_MASK\_RADIUS**: Radius of the circle assumed to include the entire spot fluorescence, expressed in pixels  
Default: 5.0  
Class: tracking  
Level: advanced

**SUBARRAY\_HALFWIDTH** Halfwidth of the sub-image constructed around putative spots, expressed in pixels. Pixels outside INNER\_MASK\_RADIUS but within SUBARRAY\_HALFWIDTH will be used to calculate the local background.  
Default: 8  
Class: tracking  
Level: advanced

**GAUSS\_MASK\_SIGMA**: Width of the Gaussian used for iterative centre refinement of detected spots, expressed in pixels  
Default: 2  
Class: tracking  
Level: advanced

**GAUSS\_MASK\_ITER**: Maximum number of iterations for iterative spot centre refinement  
Default: 1000  
Class: tracking  
Level: advanced

### Postprocessing Parameters

**MSD\_NUM\_POINTS**: Number of points calculated for the mean squared displacement when estimating diffusion coefficients.  
Default: 4  
Class: postprocessing  
Level: basic 

**CALCULATE\_ISINGLE**: Logical flag whether to calculate Isingle from the input image. If False, postprocessing will proceed using the value of Isingle as specified above (default 10000). If you are specifying CALCULATE_ISINGLE=False you must specify Isingle to be a known good value.  
Default: True  
Class: postprocessing  
Level: basic

**STOIC_METHOD**: Method used for extrapolating the “true” initial intensity of detected spots to compensate for the first exposed frame not being as bright as the others because of e.g. shutter opening delay etc.  
Options: 'Linear', 'Mean', 'Initial'  
Default: Linear  
Class: postprocessing  
Level: advanced

**NUM\_STOIC\_FRAMES**: Number of frames used for the linear fit if STOIC_METHOD='Linear'  
Default: 3  
Class: postprocessing  
Level: advanced

**COLOCALIZE**: True/False switch to control whether colocalization analysis is used if the image is ALEX or two-channel  
Default: False  
Class: postprocessing  
Level: advanced

**COLOCALIZE\_N\_FRAMES**: Number of frames that spots need to be colocalized for that colocalization pairing to be accepted.  
Default: 5  
Class: postprocessing  
Level: advanced

**COPY_NUMBER**: Boolean switch to determine whether to calculate whole-cell in-field-of-view copy number according to initial fluorescence and Isingle. Must be used with an image mask where the background is 0 and the cells are given by integers, one integer for each cell, i.e. all mask pixels with value 1 belong to cell 1, all mask pixels with value 2 belong to cell 2, etc.  
Default: False  
Class: postprocessing  
Level: advanced