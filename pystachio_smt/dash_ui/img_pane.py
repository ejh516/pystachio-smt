#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
from pathlib import Path
import tifffile
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

    logo_path = f"{Path(__file__).parent}/assets/pystachio_logo.tif"
    logo_tif = tifffile.imread(logo_path)
    logo_fig = px.imshow(
        logo_tif[:,:,0],
        color_continuous_scale='gray',
        zmin = 0,
        zmax = np.max(logo_tif[:,:,:]),
    )

    img_pane = html.Div(id="img-pane",
        children=[
            selection,
            dcc.Graph(id='image-graph', className='img-graph', figure=logo_fig),
            html.Label('Frame 1 of 1', id='image-frame'),
            dcc.Slider(id='image-slider', min=1, max=params.num_frames, value=0),
        ])

    return img_pane

@app.callback(
        Output('image-graph', 'figure'),
        Output('image-frame', 'children'),
        Output('image-slider', 'max'),
        Input('image-selection','value'),
        Input('image-slider','value'),
        Input('session-active-img-file-store', 'data'))
def update_slider(render_selection, vis_frame, active_file):
    if active_file:
        params = Parameters()
        params.name = active_file.replace('.tif','')
        print(f"Imaging {active_file}")
        image_data = images.ImageData()
        image_data.read(active_file, params)
        fig = px.imshow(
            image_data.pixel_data[vis_frame-1,:,:],
            color_continuous_scale='gray',
            zmin = 0,
            zmax = np.max(image_data.pixel_data[:,:,:]),
        )
        if (render_selection == "render-all-trajectories" or
            render_selection == "render-current-trajectories"):
            print(f"Using trajectories {params.name + '_trajectories.tsv'}")
            trajs = read_trajectories(params.name + "_trajectories.tsv")
            colors = px.colors.qualitative.Plotly
            if trajs:
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


        print(f"Setting slider max to {image_data.num_frames}")
        label = f"Frame {vis_frame} of {image_data.num_frames}"
        num_frames = image_data.num_frames


    else:
        logo_path = f"{Path(__file__).parent}/assets/pystachio_logo.tif"
        logo_tif = tifffile.imread(logo_path)
        fig = px.imshow(
            logo_tif[:,:,0],
            color_continuous_scale='gray',
            zmin = 0,
            zmax = np.max(logo_tif[:,:,:]),
        )
        label = f"Upload a file to get started..."
        num_frames = 1

    return fig, label, num_frames
