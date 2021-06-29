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
            html.Button('Apply', id='images-task-run', n_clicks=0),
        ], id="images-tab-container")

@app.callback([
        Output('session-files-update-image-store', 'data')],
    [
        Input('images-task-run', 'n_clicks'), ],
    [
        State('session-active-img-file-store', 'data'),
        State('session-parameters-store', 'data')],
    prevent_initial_call=True
    )
def apply_image_params(nclicks, active_file, params_json):
    params = Parameters(json.loads(params_json))
    if ".tif" in active_file:
        params.name = active_file.replace('.tif','')

    return [True]
