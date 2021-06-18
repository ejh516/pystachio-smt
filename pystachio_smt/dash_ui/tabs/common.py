#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

import dash_html_components as html
import dash_core_components as dcc

def get_param_input(name, param, param_class):
    param_type =  type(param["default"])
    label = html.Label(name, title=param["description"]),
    input_box = None
    if param_type is int or param_type is float:
        input_box = dcc.Input(
            id = param_class + "-" + name,
            type='number',
            debounce=True,
            placeholder=param['value'],
            style={'width':'200px'},
        )
    elif param_type is str:
        if 'options' in param.keys():
            input_box = dcc.Dropdown(
                id = param_class + "-" + name,
                options = list(map( lambda x:{'label': x, 'value': x}, param["options"])),
                value = param["options"][0],
                clearable = False,
                style={'width':'200px'},
            )
        else:
            input_box = dcc.Input(
                id = param_class + "-" + name,
                type='text',
                debounce=True,
                placeholder=param['value'],
                size = '100%',
            )
    elif param_type is bool:
        input_box = dcc.RadioItems(
            id = param_class + "-" + name,
            options = [
                {'label': 'True', 'value': 'True'},
                {'label': 'False', 'value': 'False'},
            ],
            value = str(param["value"]),
#EJH#             labelStyle={'display': 'inline-block'},
        )

    else:
#EJH#     elif param_type is list:
        input_box = html.Label('Error processing', style={'color': '#fff', 'width': '100px'}),

#EJH#     elif param_type is list:
#EJH#         input_box = dcc.Dropdown(
#EJH#             id = param_class + "-" + name,
#EJH#             options = param["options"],
#EJH#             value = param["options"][0],
#EJH#             clearable = False
#EJH#         )
#EJH# 
    return label, input_box
