#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

import simulation
import images

layout = {}

render_options = [
        {'label': 'Raw image', 'value': 'render-raw'},
        {'label': 'All trajectories', 'value': 'render-all-trajectories'},
        {'label': 'Current trajectories', 'value': 'render-current-trajectories'},
]

def build_layout(params):
    print("LAYING OUT PAGE")
    layout["header-bar"] = build_header_bar()
    layout["left-pane"] = build_left_pane(params)
    layout["right-pane"] = build_right_pane(params)
    return html.Div([
        dbc.Row(dbc.Col(layout["header-bar"])),
        dbc.Row([
            dbc.Col(layout["left-pane"]),
            dbc.Col(layout["right-pane"])
        ])
    ])

def build_header_bar():
    return html.Div([html.H1("PySTACHIO")])

def build_left_pane(params):
    layout["render-selection"] = build_render_selection()
    layout["render-image"] = build_render_image(params)
    return html.Div([
        layout["render-selection"],
        html.Br(),
        layout["render-image"],
    ])

def build_render_selection():
    return dcc.Dropdown(
        id = "render-selection",
        options = render_options,
        value = render_options[0]['value'],
        clearable = False
    )

def build_render_image(params):
    filename = html.Label(params.name, id='render-image-name')
    graph = dcc.Graph(id='render-image-graph')
    frame_number = html.Label('Frame 0', id='render-image-frame')
    slider = dcc.Slider(id='render-image-slider', min=0, max=params.num_frames, value=0)

    return html.Div(["File = ", filename, graph, html.Br(), slider, frame_number])

def build_right_pane(params):
    layout["task-tabs"] = build_task_tabs(params)
    return html.Div([layout["task-tabs"]])

def build_task_tabs(params):
    layout["files-tab"] = build_files_tab(params)
    layout["tracking-tab"] = build_tracking_tab(params)
    layout["simulation-tab"] = build_simulation_tab(params)
    layout["postprocessing-tab"] = build_postprocessing_tab()
    return dcc.Tabs(
        id='task-tabs',
        children=[
            dcc.Tab(
                label='Files',
                value='files-tab',
                children=layout["files-tab"] ),

            dcc.Tab(
                label='Tracking',
                value='tracking-tab',
                children=layout["tracking-tab"] ),

            dcc.Tab(
                label='Simulation',
                value='simulation-tab',
                children=layout["simulation-tab"] ),

            dcc.Tab(
                label='Postprocessing',
                value='postprocessing-tab',
                children=layout["postprocessing-tab"] ),
        ],
        value='files-tab'
    )

def build_files_tab(params):
    return html.Div(
    [
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Upload TIF File"]
            ),
            style={
                "width": "80%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H2("File List"),
        html.Ul(id="file-list"),
    ])

def build_tracking_tab(params):
    tracking_params = params.param_dict('tracking')
    table = []
    for param in tracking_params.keys():
        label, input_box = get_param_input(param, tracking_params[param], 'tracking')
        cols = [dbc.Col(label), dbc.Col(input_box)]
        table.append(dbc.Row(cols, no_gutters=True))
    table.append(dbc.Row([html.Br()]))
    table.append(dbc.Row(html.Button('Track', id='tracking-task-run', n_clicks=0)))

    return html.Div(table, id="tracking-tab")

def build_simulation_tab(params):
    simulation_params = params.param_dict('simulation')
    table = []
    for param in simulation_params.keys():
        label, input_box = get_param_input(param, simulation_params[param], 'simulation')
        cols = [dbc.Col(label), dbc.Col(input_box)]
        table.append(dbc.Row(cols, no_gutters=True))
    table.append(dbc.Row([html.Br()]))
    table.append(dbc.Row(html.Button('Track', id='simulation-task-run', n_clicks=0)))

    return html.Div(table, id="simulation-tab")

def build_postprocessing_tab():
    return html.Div([html.P("Postprocessing tab not yet built")],
            id="postprocessing-tab")

def get_param_input(name, param, param_class):
    param_type =  type(param["default"])
    label = html.Label(name),
    input_box = None
    if param_type is int or param_type is float:
        input_box = dcc.Input(
            id = param_class + "-" + name,
            type='number',
            debounce=True,
            placeholder=param['value'],
            style={'width':'100%'},
        )
    if param_type is str:
        if 'options' in param.keys():
            input_box = dcc.Dropdown(
                id = param_class + "-" + name,
                options = list(map( lambda x:{'label': x, 'value': x}, param["options"])),
                value = param["options"][0],
                clearable = False,
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
