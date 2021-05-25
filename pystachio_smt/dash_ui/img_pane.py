#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from dash_ui.app import app
from parameters import Parameters
from trajectories import read_trajectories
import images

render_options = [
        {'label': 'Raw image', 'value': 'render-raw'},
        {'label': 'All trajectories', 'value': 'render-all-trajectories'},
        {'label': 'Current trajectories', 'value': 'render-current-trajectories'},
]

def layout(params):
    selection = dcc.Dropdown(
        id = "image-selection",
        options = render_options,
        value = render_options[0]['value'],
        clearable = False
    )

    img_pane = html.Div(id="img_pane",
        children=[
            selection,
            dcc.Graph(id='image-graph', className='img-graph'),
            html.Label('Frame 0', id='image-frame'),
            dcc.Slider(id='image-slider', min=0, max=params.num_frames, value=0),
        ])

    return img_pane

@app.callback(
        Output('image-graph', 'figure'),
        Output('image-frame', 'children'),
        Input('image-selection','value'),
        Input('image-slider','value'),
        Input('session-active-file-store', 'data'))
def update_slider(render_selection, vis_frame, active_file):
    params = Parameters()
    params.name = active_file.replace('.tif','')
    print(f"Opening {active_file}")
    image_data = images.ImageData()
    image_data.read(active_file, params)
    fig = px.imshow(
        image_data.pixel_data[vis_frame,:,:],
        color_continuous_scale='gray',
        zmin = 0,
        zmax = np.max(image_data[vis_frame].pixel_data)
    )
    if (render_selection == "render-all-trajectories" or
        render_selection == "render-current-trajectories"):
        print(f"Using trajectories {params.name + '_trajectories.tsv'}")
        trajs = read_trajectories(params.name + "_trajectories.tsv")
        colors = px.colors.qualitative.Plotly
        for traj in trajs:
            if (render_selection == "render-current-trajectories" and
               (vis_frame < traj.start_frame or vis_frame > traj.end_frame)):
                continue
            Xs = []
            Ys = []
            color = colors[traj.id % len(colors)]
            for frame in range(traj.start_frame, traj.end_frame):
                Xs.append(traj.path[frame - traj.start_frame][0])
                Ys.append(traj.path[frame - traj.start_frame][1])
            fig.add_trace(go.Scatter(x=Xs, y=Ys, marker=dict(color=color, size=5)))
            fig.update_layout(showlegend=False)


    label = f"Frame {vis_frame}"
    return fig, label
