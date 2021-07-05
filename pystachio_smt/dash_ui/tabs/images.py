#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""

import json
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State

import images
from parameters import Parameters
from dash_ui.app import app
from dash_ui.tabs.common import get_param_input

def layout(params):
    image_params = params.param_dict('image')
    table = []
    for param in image_params.keys():
        label, input_box = get_param_input(param, image_params[param], 'image')
        cols = [dbc.Col(label), dbc.Col(input_box)]
        table.append(html.Tr([
            html.Td(label),
            html.Td(input_box)
        ]))

    return html.Div([
            html.H2("Image parameters"),
            html.Table(table),
        ], id="images-tab-container")
