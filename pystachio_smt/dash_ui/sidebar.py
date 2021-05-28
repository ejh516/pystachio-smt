#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""

"""
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output

from dash_ui.app import app
import dash_ui.tabs

def layout(params):
    sidebar = html.Div(id="sidebar",
        children=[
            dcc.Tabs(id='control-tabs', value='session-tab', children=[
                dcc.Tab(id='session-tab', value='session-tab', label='Session', children=dash_ui.tabs.session.layout(params)),
                dcc.Tab(id='tracking-tab', value='tracking-tab', label='Tracking', children=dash_ui.tabs.tracking.layout(params)),
                dcc.Tab(id='postprocessing-tab', value='postprocesing-tab', label='Analysis', children=dash_ui.tabs.postprocessing.layout(params)),
            ]),
        ]
    )

    return sidebar

def tracking_tab():
    return dcc.Tab(id='tracking-tab', label='Tracking', children=[])


