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
    return html.Div([html.H1("Single Molecule Tools")])

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
    filename = html.Label(params.seed_name, id='render-image-name')
    graph = dcc.Graph(id='render-image-graph')
    frame_number = html.Label('Frame 0', id='render-image-frame')
    slider = dcc.Slider(id='render-image-slider', min=0, max=params.num_frames, value=0)

    return html.Div(["File = ", filename, graph, html.Br(),frame_number, slider])

def build_right_pane(params):
    layout["task-tabs"] = build_task_tabs(params)
    return html.Div([layout["task-tabs"]])

def build_task_tabs(params):
    layout["simulation-tab"] = build_simulation_tab(params)
    layout["tracking-tab"] = build_tracking_tab()
    layout["postprocessing-tab"] = build_postprocessing_tab()
    return dcc.Tabs(
        id='task-tabs',
        children=[
            dcc.Tab(
                label='Simulation',
                value='simulation-tab',
                children=layout["simulation-tab"] ),

            dcc.Tab(
                label='Tracking',
                value='tracking-tab',
                children=layout["tracking-tab"] ),

            dcc.Tab(
                label='Postprocessing',
                value='postprocessing-tab',
                children=layout["postprocessing-tab"] ),
        ],
        value='simulation-tab'
    )

def build_simulation_tab(params):
    return html.Div([
            html.H2('Simulation paramters'),
            html.Label('Frame size'),
            html.Br(),
            dcc.Input(
                id='simulation-frame-size-x',
                type='number',
                debounce=True,
                placeholder=params.frame_size[0],
            ),
            html.Label('x'),
            dcc.Input(
                id='simulation-frame-size-y',
                type='number',
                debounce=True,
                placeholder=params.frame_size[1],
            ),
            html.Br(),
            html.Label('Number of frames: '),
            html.Br(),
            dcc.Input(
                id='simulation-num-frames',
                type='number',
                debounce=True,
                placeholder=params.num_frames,
            ),
            html.Br(),
            html.Br(),
            html.Label('Number of spots: '),
            html.Br(),
            dcc.Input(
                id='simulation-num-spots',
                type='number',
                debounce=True,
                placeholder=params.num_spots,
            ),
            html.Br(),
            html.Label('Isingle value: '),
            html.Br(),
            dcc.Input(
                id='simulation-isingle',
                type='number',
                debounce=True,
                placeholder=params.Isingle,
            ),
            html.Br(),
            html.Label('Diffusion coefficient: '),
            html.Br(),
            dcc.Input(
                id='simulation-diffusion-coeff',
                type='number',
                debounce=True,
                placeholder=params.diffusionCoeff,
            ),
            html.Br(),
            html.Br(),
            html.Button('Simulate', id='simulation-start', n_clicks=0),
        ],
        id="simulation-tab",
    )

def build_tracking_tab():
    return html.Div([html.P("Tracking tab not yet built")],
        id="tracking-tab")

def build_postprocessing_tab():
    return html.Div([html.P("Postprocessing tab not yet built")],
            id="postprocessing-tab")

