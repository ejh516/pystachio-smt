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

import postprocessing
from parameters import Parameters
from dash_ui.app import app
from dash_ui.tabs.common import get_param_input

def layout(params):
    postprocessing_params = params.param_dict('postprocessing')
    table = []
    for param in postprocessing_params.keys():
        label, input_box = get_param_input(param, postprocessing_params[param], 'postprocessing')
        table.append(html.Tr([
            html.Td(label),
            html.Td(input_box)
        ]))

    return html.Div([
            html.H2("Postprocessing parameters"),
            html.Table(table),
            html.Button('Analyse', id='postprocessing-task-run', n_clicks=0),
            dcc.Loading(id='postprocessing-task-loading',
                        type='default',
                        children=html.Div(id="postprocessing-task-loading-output")),
        ], id="postprocessings-tab-container")


@app.callback([
        Output('postprocessing-task-loading-output', 'children'), 
        Output('session-files-update-postprocess-store', 'data')],
    [
        Input('postprocessing-task-run', 'n_clicks')],
    [
        State('session-active-img-file-store', 'data'),
        State('session-parameters-store', 'data'),
        State('session-files-update-postprocess-store', 'data')],
    prevent_initial_call=True
    )
def run_postprocessing_task(nclicks, active_file, params_json, post_update):
    params = Parameters(json.loads(params_json))
    params.display_figures = False
    if ".tif" in active_file:
        params.name = active_file.replace('.tif','')

    postprocessing.postprocess(params)

    return ["", post_update+1]
