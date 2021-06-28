#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import os
import base64
import json
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output,State

from datetime import datetime

from parameters import Parameters, default_parameters
from dash_ui.app import app

full_data_folder=os.path.join(os.getcwd(),'web_data')
web_data_folder='/web_data'

input_list = []
for param in default_parameters:
    if (default_parameters[param]['class'] in ["tracking", "image", "postprocessing"]):
        input_list.append('{}-{}'.format(default_parameters[param]['class'], param))

def layout(params):
    return html.Div(id='session-tab-container', children=[
        html.H2("Session management"),
        html.Button('New Session', id='new-session-button', n_clicks=0),
        html.H3("Files"),
        dcc.Dropdown(id='files-dropdown',
            options=[],
            clearable=False,
        ),
        dcc.Upload(id='data-file-upload',
            children=html.Div(
                ["Upload File"]
            ),
            style={
                "width": "80%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "position": "center",
                "margin": "auto",
                "marginTop": "10px",
                "marginBottom": "10px",
            },
            multiple=False,
        ),
        html.Div([
            html.Button("Download file", id="file-download-button"),
            dcc.Download(id="file-download")
            ]),
        dcc.Store(id='session-id-store', data='default'),
        dcc.Store(id='session-files-update-upload-store'),
        dcc.Store(id='session-files-update-track-store'),
        dcc.Store(id='session-files-update-postprocess-store', data=0),
        dcc.Store(id='session-files-update-image-store', data=0),
        dcc.Store(id='session-parameters-store', data=str(json.dumps(params._params))),
        dcc.Store(id='session-active-img-file-store', data=""),
        dcc.Store(id='session-active-info-file-store', data=""),
    ])

@app.callback([
        Output('session-active-img-file-store', 'data'),
        Output('session-active-info-file-store', 'data')
    ], [
        Input('files-dropdown', 'value'),
        State('session-active-img-file-store', 'data'),
        State('session-active-info-file-store', 'data'),
        State("session-id-store", "data"),
    ])
def set_active_file(filename, img_file, info_file, session_id):
    if filename:
        full_filename=""
        if ".tif" in filename:
            print(f"Setting active image file to {filename}")
            img_file = os.path.join(full_data_folder, session_id, filename)
        elif ".tsv" in filename:
            print(f"Setting active info file to {filename}")
            info_file = os.path.join(full_data_folder, session_id, filename)
        elif ".png" in filename:
            print(f"Setting active info file to {filename}")
            info_file = os.path.join(web_data_folder, session_id, filename)
    else:
        img_file = ""
        info_file = ""

    return [img_file, info_file] 

@app.callback([
    Output('files-dropdown', 'options'),
    Output('files-dropdown', 'value')],
    [
        Input('session-id-store', 'data'),
        Input('session-files-update-upload-store', 'data'),
        Input('session-files-update-track-store', 'data'),
        Input('session-files-update-postprocess-store', 'data'),
        ])
def update_file_options(session_id, update_upload, update_track, update_post):
    absolute_filename = os.path.join(full_data_folder, session_id)
    print(f"Updating options {absolute_filename}")
    options = [{'label': f, 'value': f} for f in os.listdir(absolute_filename)]
    first_element = ""
    if options:
        first_element = options[0]["value"]

    return options, first_element

@app.callback(Output('file-download', 'data'),
              Input('file-download-button', 'n_clicks'),
              State('files-dropdown', 'value'),
              State('session-id-store', 'data'),
              prevent_initial_call=True,
             )
def download_file(n_clicks,filename, session_path):
    return dcc.send_file(os.path.join(full_data_folder, session_path, filename))

@app.callback([
        Output('session-files-update-upload-store', 'data'),
    ], [
        Input("data-file-upload", "filename"),
        Input("data-file-upload", "contents"),
        State('session-active-img-file-store', 'data'),
        State('session-active-info-file-store', 'data'),
        State("session-id-store", "data"),
    ])
def upload_file(filename, file_contents, img_file, info_file, session_id):
    print("Called")
    full_filename=""
    if filename:
        full_filename = os.path.join(full_data_folder, session_id, filename)

    if filename is not None and file_contents is not None:
        print(f"Uploading file to {full_filename}")
        data = file_contents.encode("utf8").split(b";base64,")[1]

        with open(full_filename, 'wb') as fp:
            fp.write(base64.decodebytes(data))
    else:
        file_path=""

    now = datetime.now()
    time = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return [time]

@app.callback(
        [
            Output('session-id-store', 'data'),
        ], [
            Input('new-session-button', 'n_clicks'),
        ]
    )
def new_session(n_clicks):
    now = datetime.now()
    session_id = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    session_folder = os.path.join(full_data_folder, session_id)

    print(f"Active data folder: {session_folder}")
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    else:
        print("Session already exists!")
        os.exit()

    return [session_id]

@app.callback(
        Output('session-parameters-store', 'data'),
        [Input('session-parameters-store', 'data')] +
        [Input(input_box, 'value') for input_box in input_list]
)
def update_parameters(input_json, *args):
    params = Parameters(json.loads(input_json))
    params._params = json.loads(input_json)
    for i in range(len(input_list)):
        param_class, param = input_list[i].split('-')
        if params._params[param]['value'] != args[i]:
            print(f"Setting {param} from {params._params[param]['value']} to {args[i]}")
            params._params[param]['value'] = args[i]

    params_json = str(json.dumps(params._params))

    return params_json
