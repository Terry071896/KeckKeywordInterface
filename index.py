import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from datetime import datetime
#import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
import dash_katex

from app import app
from apps import kcwi_ui, nirspec_ui, nirc2_ui, deimos_ui, nires_ui, lris_ui, mosfire_ui, esi_ui, hires_ui, osiris_ui, main_page


app.layout = html.Div(id='full-page', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',  className='page-content-class')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kcwi':
        return kcwi_ui.layout
    elif pathname == '/nirspec':
        return nirspec_ui.layout
    elif pathname == '/nirc2':
        return nirc2_ui.layout
    elif pathname == '/deimos':
        return deimos_ui.layout
    elif pathname == '/nires':
        return nires_ui.layout
    elif pathname == '/lris':
        return lris_ui.layout
    elif pathname == '/mosfire':
        return mosfire_ui.layout
    elif pathname == '/esi':
        return esi_ui.layout
    elif pathname == '/hires':
        return hires_ui.layout
    elif pathname == '/osiris':
        return osiris_ui.layout
    else:
        return main_page.layout

if __name__ == '__main__':
    app.run_server(debug=True)
