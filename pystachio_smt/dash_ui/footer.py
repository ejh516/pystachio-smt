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
    footer = html.Div(id="footer",
        children=[
            """
DISCLAIMER: The views and opinions expressed on this web page are not necessarily those of the
author. It is more than likely that he wrote them on a whim one day when he was waiting for his 
code to compile, or his energy to converge, or his job to run on ARCHER, or something like
that...
            """])

    return footer
