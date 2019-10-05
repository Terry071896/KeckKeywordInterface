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
from apps import kcwi_ui, app2, main_page


app.layout = html.Div(id='full-page', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',  className='page-content-class')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return kcwi_ui.layout
    elif pathname == '/page-2':
        return app2.layout
    else:
        return main_page.layout

if __name__ == '__main__':
    app.run_server(debug=True)
