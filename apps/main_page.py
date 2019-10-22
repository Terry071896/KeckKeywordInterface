#tabs-to-spaces:untabify-all
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

from keywords import Keywords
from app import app

theme = {
        'dark': False,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

layout = html.Div(id='page-content-main', className='page-content-class', children=[
    html.H1('Welcome', style={'text-align': 'center', 'font-size':'75px'}),
    html.P('This web page provides a user interface for each of the Keck Instruments.', style={'text-align': 'center', 'font-size':'20px'}),
    html.P('Each page is to communicate the diagnoses of the health of the instrument.', style={'text-align': 'center', 'font-size':'20px'}),
    html.Div(id='keck1-links', className='indicator-box', children=[
        html.H4('Keck I'),
        html.P(dcc.Link('HIRES', href='/hires', style={'color': 'white'})),
        html.P(dcc.Link('LRIS', href='/lris', style={'color': 'white'})),
        html.P(dcc.Link('MOSFIRE', href='/mosfire', style={'color': 'white'})),
        html.P(dcc.Link('OSIRIS', href='/osiris', style={'color': 'white'}))
    ]),
    html.Div(id='keck2-links', className='indicator-box', children=[
        html.H4('Keck II'),
        html.P(dcc.Link('DEIMOS', href='/deimos', style={'color': 'white'})),
        html.P(dcc.Link('ESI', href='/esi', style={'color': 'white'})),
        html.P(dcc.Link('KCWI', href='/kcwi', style={'color': 'white'})),
        html.P(dcc.Link('NIRES', href='/nires', style={'color': 'white'})),
        html.P(dcc.Link('NIRC2', href='/nirc2', style={'color': 'white'})),
        html.P(dcc.Link('NIRSPEC', href='/nirspec', style={'color': 'white'}))
    ])
])
