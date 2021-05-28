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

def layout():
    graphs_pane = html.Div(id="graphs_pane",
        children=[
            html.H2("Graphs"), ])

    return graphs_pane
