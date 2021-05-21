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
    sidebar = html.Div(id="sidebar",
        children=[
            html.H1("Sidebar"), ])

    return sidebar
