# !usr/bin/env python
# Author: Terry Cox
# GitHub: https://github.com/KeckObservatory/KeckKeywordInterface
# Email: tcox@keck.hawaii.edu, tfcox1703@gmail.com

__author__ = ['Terry Cox', 'Luca Rizzi']
__version__ = '1.0'
__email__ = ['tcox@keck.hawaii.edu', 'tfcox1703@gmail.com', 'lrizzi@keck.hawaii.edu']
__github__ = 'https://github.com/KeckObservatory/KeckKeywordInterface'

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from datetime import datetime
import plotly.graph_objs as go
import requests
import dash_katex

from KeckKeywordInterface.app import app
from KeckKeywordInterface.apps import kcwi_ui, nirspec_ui, nirc2_ui, deimos_ui, nires_ui, lris_ui, mosfire_ui, esi_ui, hires_ui, osiris_ui, main_page
from KeckKeywordInterface.apps import kcwi_ui_dark, nirspec_ui_dark, nirc2_ui_dark, deimos_ui_dark, nires_ui_dark, lris_ui_dark, mosfire_ui_dark, esi_ui_dark, hires_ui_dark, osiris_ui_dark



app.layout = html.Div(id='full-page', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',  className='page-content-class')
])


@app.callback([dash.dependencies.Output('page-content', 'children'),
                Output('page-content', 'style')],
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    '''
    A callback function scheduled print the correct layout from correct pathname

    Parameters
    ----------
    pathname : str
        the path for which is correlated to the page layout clicked.

    Returns
    -------
    list
        a list of 'dash' html components to build webpage layout.
    '''
    if pathname == '/kcwi':
        return [kcwi_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/nirspec':
        return [nirspec_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/nirc2':
        return [nirc2_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/deimos':
        return [deimos_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/nires':
        return [nires_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/lris':
        return [lris_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/mosfire':
        return [mosfire_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/esi':
        return [esi_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/hires':
        return [hires_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/osiris':
        return [osiris_ui.layout, {'background-color': 'white', 'color': 'black'}]
    elif pathname == '/kcwi-dark':
        return [kcwi_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/nirspec-dark':
        return [nirspec_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/nirc2-dark':
        return [nirc2_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/deimos-dark':
        return [deimos_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/nires-dark':
        return [nires_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/lris-dark':
        return [lris_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/mosfire-dark':
        return [mosfire_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/esi-dark':
        return [esi_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/hires-dark':
        return [hires_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    elif pathname == '/osiris-dark':
        return [osiris_ui_dark.layout, {'backgroundColor': '#303030', 'color': 'white'}]
    else:
        return [main_page.layout, {'background-color': 'white', 'color': 'black'}]

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8050, debug=True, threaded=True)
