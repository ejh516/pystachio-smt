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

tabs_style = {
    "height": "32px",
}

tab_style = {
    'background': 'transparent',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
}

selected_tab_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}

def layout(params):
    sidebar = html.Div(id="sidebar",
            children=[
                dcc.Tabs(id='control-tabs', value='session-tab',
                    parent_className='sidebar-tabs',
                    className='sidebar-tabs-container',
                    style=tabs_style,
                    children=[
                    dcc.Tab(id='session-tab', 
                        value='session-tab', 
                        label='Session', 
                        className='sidebar-tab',
                        selected_className='sidebar-tab-selected',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        children=dash_ui.tabs.session.layout(params)),
                    dcc.Tab(id='images-tab',
                        value='images-tab',
                        label='Images',
                        className='sidebar-tab',
                        selected_className='sidebar-tab-selected',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        children=dash_ui.tabs.images.layout(params)),
                    dcc.Tab(id='tracking-tab',
                        value='tracking-tab',
                        label='Tracking',
                        className='sidebar-tab',
                        selected_className='sidebar-tab-selected',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        children=dash_ui.tabs.tracking.layout(params)),
                    dcc.Tab(id='postprocessing-tab',
                        value='postprocesing-tab',
                        label='Analysis',
                        className='sidebar-tab',
                        selected_className='sidebar-tab-selected',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        children=dash_ui.tabs.postprocessing.layout(params)),
                    ]),
                ]
            )

    return sidebar

def tracking_tab():
    return dcc.Tab(id='tracking-tab', label='Tracking', children=[])


