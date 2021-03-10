#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

""" PARAMETERS - Program parameters module

Description:
    parameters.py contains the Parameters class that holds all the program
    parameters, along with the default value for each parameter and routines
    for setting those parameters.

Contains:
    class Parameters

Author:
    Edward Higgins

Version: 0.2.0
"""

import sys
import json
from copy import deepcopy


class Parameters:
    def __init__(self):
        self._options = {
            # Runtime parameters
            'general': {
                'num_procs':
                    { 'description': 'The number of CPU processes to run with',
                      'level': 'basic',
                      'default': 0 },
                'tasks':
                    { 'description': 'Which task(s) to perform in the run',
                      'level': 'basic',
                      'default': [],
                      'options': ['simulate', 'track', 'postprocess', 'view', 'app'] },
                'name':
                    { 'description': 'Name prefixing all files associated with this run',
                      'level': 'basic',
                      'default': '' },
                'mask_file':
                    { 'description': 'Filename of an image mask for filtering spots',
                      'level': 'basic',
                      'default':  ''},
            },

            # Image parameters
            'image': {
                'num_frames':
                    { 'description': 'Number of frames to simulate',
                      'level': 'basic',
                      'default': 10 },
                'frame_size':
                    { 'description': 'Size of frame to simulate ([x,y])',
                      'level': 'basic',
                      'default': [100,100] },
                'frame_time':
                    { 'description': 'Time per frame in seconds',
                      'level': 'advanced',
                      'default': 0.005 },
                'pixel_size':
                    { 'description': 'Length of a single pixel in μm',
                      'level': 'advanced',
                      'default': 0.120 },
                'start_frame':
                    { 'description': 'The first frame of the image stack to analyse',
                      'level': 'basic',
                      'default':  0},
                'end_frame':
                    { 'description': 'The last frame of the image stack to analyse (-1 = use all frames)',
                      'level': 'basic',
                      'default':  -1},
                'channel_split':
                    { 'description': 'If/how the frames are split spatially',
                      'level': 'basic',
                      'default': 'None',
                      'options': ['None', 'Vertical', 'Horizontal'] },
            },

            # Simulation parameters
            'simulation': {
                'num_spots':
                    { 'description': 'Number of spots to simulate',
                      'level': 'basic',
                      'default': 10 },
                'I_single':
                    { 'description': 'I_single value for simulated spots',
                      'level': 'basic',
                      'default': 10000.0 },
                'bg_mean':
                    { 'description': 'Mean of the background pixlel intensity',
                      'level': 'advanced',
                      'default': 500.0 },
                'bg_std':
                    { 'description': 'Standard deviation of the background pixel intensity',
                      'level': 'advanced',
                      'default': 120.0 },
                'diffusion_coeff':
                    { 'description': 'Diffusion coefficient of the diffusing spots',
                      'level': 'basic',
                      'default': 1.0 },
                'spot_width':
                    { 'description': 'Width of the simulated Gaussian spot',
                      'level': 'advanced',
                      'default':  1.33},
                'max_spot_molecules':
                    { 'description': 'Maximum number of dye molecules per spot',
                      'level': 'advanced',
                      'default': 1 },
                'p_bleach_per_frame':
                    { 'description': 'Probability of a spot bleaching in a given frame',
                      'level': 'advanced',
                      'default': 0.0 },
                'photobleach':
                    { 'description': 'Perform photobleaching (alias for max_spot_molecules=10, p_bleach_per_frame=0.05)',
                      'level': 'basic',
                      'default': False },
            },

            'tracking': {
                'bw_threshold_tolerance':
                    { 'description': 'Threshold for generating the b/w image relative to the peak intensity',
                      'level': 'advanced',
                      'default': 1.0 },
                'snr_filter_cutoff':
                    { 'description': 'Cutoff value when filtering spots by signal/noise ratio',
                      'level': 'basic',
                      'default': 0.4 },
                'filter_image':
                    { 'description': 'Method for filtering the input image pre-analysis',
                      'level': 'advanced',
                      'default': 'Gaussian',
                      'options': ['Gaussian', 'None']},
                'max_displacement':
                    { 'description': 'Maximum displacement allowed for spots between frames',
                      'level': 'advanced',
                      'default': 5.0 },
                'struct_disk_radius':
                    { 'description': 'Radius of the Disk structural element',
                      'level': 'advanced',
                      'default': 5 },
                'struct_disk_radius':
                    { 'description': 'Radius of the Disk structural element',
                      'level': 'advanced',
                      'default': 5 },
                'min_traj_len':
                    { 'description': 'Minimum number of frames needed to define a trajectory',
                      'level': 'advanced',
                      'default': 3 },
                'spot_halfwidth':
                    { 'description': 'Halfwidth of the sub-image for analysing individual spots',
                      'level': 'advanced',
                      'default': 8 },
                'gauss_mask_sigma':
                    { 'description': 'Width of the Gaussian used for the iterative centre refinement',
                      'level': 'advanced',
                      'default': 2.0 },
                'gauss_mask_max_iter':
                    { 'description': 'Max number of iterations for the iterative centre refinement',
                      'level': 'advanced',
                      'default': 1000 },
                'inner_mask_radius':
                    { 'description': 'Radius of the mask used for calculating spot intensities',
                      'level': 'advanced',
                      'default': 5 },
            },
            
            # Postprocessing parameters
            'postprocessing': {
                'msd_num_points':
                    { 'description': 'Number of points used to calculate the mean-squared displacement',
                      'level': 'basic',
                      'default': 4 },
                'stoic_method':
                    { 'description': 'Method used for determining the stoichiometry of each trajectory',
                      'level': 'advanced',
                      'default': 'Linear',
                      'options': ['Linear', 'Mean', 'Initial'] },
                'num_stoic_frames': {
                      'level': 'advanced',
                      'description': 'Number of frames used to determine the stoichiometry',
                      'default': 3 },
            },
        }

        # Set all the values to be the default values
        for param_class in self._options.keys():
            for param in self._options[param_class].keys():
                self._options[param_class][param]['value'] = self._options[param_class][param]['default']


    def get(self, param_class, param_name = None):
        if param_name:
            return self._options[param_class][param_name]['value']
        else:
            return self._options[param_class]

    def read(self, filename):
        with open(filename) as json_file:
            contents = dict(json.load(json_file))
            for param_class in contents:
                for param in contents[param_class]:
                    if not self._options[param_class][param]:
                        sys.exit(f'No such parameter {param} in {param_class}')
                    if type(self._options[param_class][param]['default']) is not type(contents[param_class][param]):
                        sys.exit(f'Invalid type for {param} in {param_class}')

                    self._options[param_class][param]['value'] = contents[param_class][param]


    def write(self, filename):
        contents = deepcopy(self._options)
        for key in contents:
            for k,v in contents[key].items():
                contents[key][k] = v['value']

        with open(filename, 'w') as json_file:
            json_file.write( json.dumps(contents, indent=2, sort_keys=True))

