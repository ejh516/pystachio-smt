# SMT-PYTHON

> **WARNING**
> 
> This codebase is still in early development and, as such, some of the
> documentation is writing cheques that the rest of the code can't cash. If you've
> been given access to this code by Ed Higgins then he's already explained this to
> you.  However if you've found your way here by any other means, do take what's
> written below with a pinch of salt. 
> 
> Rest assured, this document will be correct when the code is finally made
> available to the public, and this warning vanishes into the ether.

## Introduction
SMT-Python is, to a first approximation, a Python port of Adam Wollman's Single
Molecule Tools[1]. SMT-Python provides a utility for tracking and analysing
localisation microscopy data, providing features for spot tracking and spot
intensity & trajectory analysis.

## Synopsis
```{bash}
$ smtpy web
```
or
```{bash}
$ smtpy <task> <seed name> [<parameter>=<value>...]
```

For example:
```{bash}
$ smtpy track data/exp_data
$ smtpy simulate,view data/sim_data num_spots=10
```

## Overview
SMT-Python can be used in two ways: A Web GUI for interactive use, or a command
UI for terminal-based & scripted use. Both interfaces provide the following
functionality:

### Spot tracking
This allows input image data (either from experiment or simulation) to be
imported into the program and spots tracked across multiple frames.

### Simulation of experimental data
This allows pseudo-microscopy data to be simulated based on a number of
tunable parameters, such as the number of spots, number of frames, bleaching
time, Signal-Noise ratio etc...

### Post processing analysis
This allows spot physical parameters such as ISingle values and diffusions
coefficients to be extracted from tracked spots' trajectories & intensities.

## Installation
SMT-Python uses a few fairly common libraries, listed in `requirements.txt`
In short, these are:
- *Numpy* for array handling
- *OpenCV* for image processing
- *Dash/Plotly* for a web interface.

Installation of these can be performed as such:
```{bash}
$ pip install -r requirements.txt
```

After that, just make sure `smtpy` is in your `$PATH` somewhere, or just refer
to it directly using `/path/to/smtpy ...`.

Improved installation instructions will be included when an improved
installation method has been implemented.

## Usage

For the terminal UI, the command can be run as follows:
```{bash}
$ smtpy <tasks> <seedname> [parameters]
```

Here, `<seedname>` is used for telling the program which file(s) to read from
and write to; and `<tasks>` is a comma-separated list of the tasks you want to
be performed.  For example, if you want to track spots in a dataset and then
view the result, this can be done with `smtpy track,view ...`. 

For a given `<seedname>`, the files currently recognised are:
- `seedname.tif`: An input dataset saved as a multi-frame TIFF,
- `seedname.simulated.tif`: An output pseudo-dataset saved as a multi-frame TIFF,
- `seedname.trajectories.tsv`: A tab-separated value list containing predicted trajectories for `seedname.tif`
- `seedname.sim_trajectories.tsv`: A tab-separated value list containing simulated trajectories for  `seedname.simulated.tif`.

The complete list of tasks currently implemented is:
- `simulate`: Create a simulated psuedo-dataset based upon a set of parameters
- `track`: Track the spots in a given dataset and produce predicted trajectories for that dataset.
- `view`: View the dataset using the `Matplotlib` library.


## Contributing

Information on how to contribute to the SMT-Python project is available in
`doc/contributing.md`. In short, the process is:
- Clone the repository,
- Create a branch for your new changes (functionality, bug fixes, etc...),
- Develop your changes in your new branch, and
- Create a pull-request to merge the branch back into `master`.

If this seems daunting to you then good - you're going to learn a useful skill
today!

## Authors

This code has been developed by Edward Higgins in collaboration with the
Physics of Life group at the University of York. For more information, contact
Edward at [ed.higgins@york.ac.uk](ed.higgins@york.ac.uk).

## License

Copyright © 2021, Edward Higgins. Released under the MIT License.
