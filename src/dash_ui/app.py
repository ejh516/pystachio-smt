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
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
import numpy as np

import dash_ui.layout
import images
from parameters import Parameters
from trajectories import read_trajectories

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

def launch_app(params):
    app.title = "PyNACHE"
    params.write(params.get('general', 'name') + '.json')
    app.layout = dash_ui.layout.build_layout(params)
    app.run_server(debug=False)

@app.callback(
        Output('render-image-graph', 'figure'),
        Output('render-image-frame', 'children'),
        Input('render-selection','value'),
        Input('render-image-slider','value'),
        Input('render-image-name','children'))
def update_slider(render_selection, vis_frame, seedname):
    params = Parameters()
    params.read(seedname + ".json")
    image_data = images.ImageData()
    image_data.read(seedname + ".tif", params)
    fig = px.imshow(
        image_data.pixel_data[vis_frame,:,:],
        color_continuous_scale='gray',
        zmin = 0,
        zmax = np.max(image_data[vis_frame].pixel_data)
    )
    if (render_selection == "render-all-trajectories" or
        render_selection == "render-current-trajectories"):
        trajs = read_trajectories(seedname + "_trajectories.tsv")
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
