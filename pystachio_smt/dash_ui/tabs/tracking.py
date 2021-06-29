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

import tracking
from parameters import Parameters
from dash_ui.app import app
from dash_ui.tabs.common import get_param_input

def layout(params):
    tracking_params = params.param_dict('tracking')
    table = []
    for param in tracking_params.keys():
        label, input_box = get_param_input(param, tracking_params[param], 'tracking')
        cols = [dbc.Col(label), dbc.Col(input_box)]
        table.append(html.Tr([
            html.Td(label),
            html.Td(input_box)
        ]))

    return html.Div([
            html.H2("Tracking parameters"),
            html.Table(table),                      
            html.Button('Track', id='tracking-task-run', n_clicks=0),
            dcc.Loading(id='tracking-task-loading',
                        type='default',
                        children=html.Div(id="tracking-task-loading-output")),
        ], id="tracking-tab-container")

    return html.Div(table, id="tracking-tab-container")

@app.callback([
        Output('tracking-task-loading-output', 'children'), 
        Output('image-slider', 'value'),
        Output('session-files-update-track-store', 'data')],
    [
        Input('tracking-task-run', 'n_clicks'), ],
    [
        State('session-active-img-file-store', 'data'),
        State('session-parameters-store', 'data')],
    prevent_initial_call=True
    )
def run_tracking_task(nclicks, active_file, params_json):
    params = Parameters(json.loads(params_json))
    params._params = json.loads(params_json)
    print(f"Running tracking on {params.name}")
    if ".tif" in active_file:
        params.name = active_file.replace('.tif','')

    tracking.track(params)

    return ["", 1, True]
