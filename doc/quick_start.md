# PySTACHIO: Quick-Start Guide

## Installation

The easiest way to install PySTACHIO is by using pip - but note the package name is pystachio-smt and will only work with the Python 3 version of pip. As usual, pip will automatially resolve, download, and install dependencies.

If you prefer not to use pip for some reason, you can install manually. Requirements are found in requirements.txt in the PySTACHIO directory. There is no Makefile for PySTACHIO so after unpacking the download and installing dependencies you can start straight away.

## Running PySTACHIO

PySTACHIO has two user modes: GUI via a web app built with plotly and a command line interface that is suitable for use with Linux, Mac, or a Python interpreter in Windows. Probably it works OK with PowerShell too but we haven't tried it because none of us know PowerShell. In general we believe that the command line interface is the best, most flexible way to use PySTACHIO. The GUI is useful for testing analysis parameters and visualizing PySTACHIO's performance, but for a large data set or convergence testing it will almost always be necessary to write a script to call PySTACHIO recursively with modified parameters or different data files, unless you like clicking the same few buttons every few minutes for an entire day.

### From the GUI

The GUI is built on plotly and runs as a web app. You can start the web app by double clicking ``PySTACHIO_LINUX`` or ``PySTACHIO_WIN`` in the PySTACHIO directory. This will launch a server instance you may connect with by opening a web browser and navigating to `localhost:8050`.

The opening screen is shown below with annotations. Briefly, choose a file from your computer with the select file button in the “track” tab, change the parameters you want to change (default values are already loaded so no need to specify everything) and click track. Once this is done you may switch to the analysis pane to perform postprocessing analysis on the tracks file you have just generated. To do this, select the ... from the drop down box and click analyze - again defaults are preloaded so only modify what you want. By default PySTACHIO does all its analysis on all datasets as the analysis is cheap - on the other than that may mean you end up with graphs and analysis files which are unwanted or nonsensical. You should be careful that the analysis you use you actually trust.

### From the command line

PySTACHIO on the command line has a relatively straightforward syntax which should be trivially scriptable (here square brackets indicate a required argument and curly braces indicate optional arguments):

    pystachio-smt [TASK_LIST] [IMAGE_FILE] {KEYWORD_ARGUMENTS}

We will take each of these in order:

**TASK_LIST** This is a list of tasks for PySTACHIO to execute and is made up of one or more tasks taken from simulate track postprocess view app where each task is separated by a comma but no space, e.g. track,postprocess. Note here that order matters! Tasks are executed left to right so simulate,track is different to track,simulate. In the former, you simulate data and then track it. In the latter, you look for a file, track it if it exists (crash if it doesn't) and then simulate data __and overwrite whatever it was you just tracked_. Beware! If you run ``pystachio-smt app`` you launch the web app and can navigate to `localhost:8050` to use the GUI - this is in fact all the clickable shortcuts do. 

**IMAGE_FILE** This is the path (full or relative) to the image file for analysis. If you are simulating data, this specifies the location and root filename for the simulated data to be saved to. You should specify the filename without the .tif extension. PySTACHIO at this time only supports TIF files.

**KEYWORD\_ARGUMENTS** These are optional and overwrite the defaults found in parameters.py. To use them, specify the keyword and a new value separated by = e.g.: `SNR_min=0.6`. Multiple keyword arguments should be separated by spaces. For a full list of keyword arguments see the manual.

For tracking or postprocessing, analysis files will be written to the same directory as the image file is found, as will graphs of the analysis. Probably you will need to replot the data but we hope that the default generated files are helpful at least as an indication or to begin more involved analysis.