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

def layout(params):
    postprocessing_params = params.param_dict('postprocessing')
    table = []
    for param in postprocessing_params.keys():
        label, input_box = get_param_input(param, postprocessing_params[param], 'postprocessing')
        cols = [dbc.Col(label), dbc.Col(input_box)]
        table.append(dbc.Row(cols, no_gutters=True))
    table.append(dbc.Row([html.Br()]))
    table.append(dbc.Row(html.Button('Run analysis', id='postprocessing-task-run', n_clicks=0)))
    table.append(dbc.Row(dcc.Loading(id='postprocessing-task-loading',
                                     type='default',
                                     children=html.Div(id="postprocessing-task-loading-output"))))

    return html.Div(table, id="postprocessing-tab-container")

@app.callback([
        Output('postprocessing-task-loading-output', 'children'), 
        Output('session-files-update-postprocess-store', 'data')],
    [
        Input('postprocessing-task-run', 'n_clicks'), ],
    [
        State('session-active-file-store', 'data'),
        State('session-parameters-store', 'data')],
    prevent_initial_call=True
    )
def run_postprocessing_task(nclicks, active_file, params_json):
    print(f"Running postprocessing on params.name")
    params = Parameters(json.loads(params_json))
    if ".tif" in active_file:
        params.name = active_file.replace('.tif','')

    postprocessing.postprocess(params)

    return ["", True]
def get_param_input(name, param, param_class):
    param_type =  type(param["default"])
    label = html.Label(name, style={'color': '#fff', 'width': '100px'}),
    input_box = None
    if param_type is int or param_type is float:
        input_box = dcc.Input(
            id = param_class + "-" + name,
            type='number',
            debounce=True,
            placeholder=param['value'],
            style={'width':'200px'},
        )
    if param_type is str:
        if 'options' in param.keys():
            input_box = dcc.Dropdown(
                id = param_class + "-" + name,
                options = list(map( lambda x:{'label': x, 'value': x}, param["options"])),
                value = param["options"][0],
                clearable = False,
                style={'width':'200px'},
            )
        else:
            input_box = dcc.Input(
                id = param_class + "-" + name,
                type='text',
                debounce=True,
                placeholder=param['value'],
                size = '100%',
            )
    elif param_type is bool:
        input_box = dcc.RadioItems(
            id = param_class + "-" + name,
            options = [
                {'label': 'True', 'value': 'True'},
                {'label': 'False', 'value': 'False'},
            ],
            value = str(param["value"]),
#EJH#             labelStyle={'display': 'inline-block'},
        )

    elif param_type is list:
        input_box = dcc.Dropdown(
            id = param_class + "-" + name,
            options = param["options"],
            value = param["options"][0],
            clearable = False
        )

    return label, input_box
