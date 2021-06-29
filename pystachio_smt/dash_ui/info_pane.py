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
import dash_table
from dash.dependencies import Input,Output
import pandas as pd


from dash_ui.app import app
import dash_ui.tabs.session


def layout():
    info_pane = html.Div(id="info-pane",
        children=[
            html.H1("Information"),
            html.Div(id='info-content', children=[])
        ])

    return info_pane

@app.callback(Output('info-content', 'children'),
    Input('session-active-info-file-store', 'data'))
def update_info(filename):
    if '.png' in filename:
        return [html.Img(src=filename)]
    elif '.tsv' in filename:
        df = pd.read_csv(filename, delimiter="\t")

        return [
            dash_table.DataTable(
                id='info-datatable',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
            )
        ]
