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
import tifffile
import sys

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

frames = tifffile.imread(sys.argv[1])
frame_id = 0

figs = []
for i in range(frames.shape[0]):
    fig = px.imshow(frames[i,:,:], color_continuous_scale='gray',zmin=0,zmax=255)
    figs.append(fig)

app.layout = html.Div([
    dbc.Row(dbc.Col(html.Div([html.H1('Single Molecule Tools')]))),
    dbc.Row([
        dbc.Col(
            html.Div([  
                dcc.Dropdown(options=[
                    {'label':'Raw image', 'value':'raw'},
                    {'label':'Binary map', 'value':'binary'},
                    {'label':'Ultimate erosion', 'value':'uerode'} ],
                    value='raw'),
                dcc.Graph( id='image-data'),
                html.Label('Frame 0', id='frame-label'),
                dcc.Slider(id='frame-slider', min=0, max=len(frames)-1, value=0)
            ], id='view-div'),width=6), 
        dbc.Col(
            html.Div([  
                dcc.Tabs([
                    dcc.Tab(label='Parameters', value='params-tab'),
                    dcc.Tab(label='Simulation', value='sim-tab'),
                    dcc.Tab(label='Statistics', value='stats-tab')])
            ],id='tabs-div'),width=6)])

])

@app.callback(
        dash.dependencies.Output('image-data', 'figure'),
        dash.dependencies.Input('frame-slider','value'))
def update_slider(value):
    frame_id = value
    return figs[frame_id]

@app.callback(
        dash.dependencies.Output('frame-label', 'children'),
        dash.dependencies.Input('frame-slider','value'))
def update_slider(value):
    return f"Frame {value+1} of {frames.shape[0]}"

if __name__ == '__main__':
    app.run_server(debug=True)
