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

from KeckKeywordInterface.keywords import Keywords
from KeckKeywordInterface.app import app

dark = True

part1 = [html.H1('Welcome', style={'text-align': 'center', 'font-size':'75px'}),
    html.P('This web page provides a user interface for each of the Keck Instruments.', style={'text-align': 'center', 'font-size':'20px'}),
    html.P('Each page is to communicate the diagnoses of the health of the instrument.', style={'text-align': 'center', 'font-size':'20px'}),
    html.Br(),
    daq.ToggleSwitch(
        id='daq-light-dark-theme',
        label=['Light', 'Dark'],
        style={'width': '250px', 'margin': 'auto'},
        value=False,
        disabled=True
    ),
    html.Div(id='keck1-links', className='indicator-box', children=[
        html.H4('Keck I'),
        html.P(dcc.Link('HIRES', href='/hires', style={'color': 'grey'})),
        html.P(dcc.Link('LRIS', href='/lris', style={'color': 'grey'})),
        html.P(dcc.Link('MOSFIRE', href='/mosfire', style={'color': 'grey'})),
        html.P(dcc.Link('OSIRIS', href='/osiris', style={'color': 'grey'}))
    ]),
    html.Div(id='keck2-links', className='indicator-box', children=[
        html.H4('Keck II'),
        html.P(dcc.Link('DEIMOS', href='/deimos', style={'color': 'white'})),
        html.P(dcc.Link('ESI', href='/esi', style={'color': 'white'})),
        html.P(dcc.Link('KCWI', href='/kcwi', style={'color': 'white'})),
        html.P(dcc.Link('NIRES', href='/nires', style={'color': 'grey'})),
        html.P(dcc.Link('NIRC2', href='/nirc2', style={'color': 'grey'})),
        html.P(dcc.Link('NIRSPEC', href='/nirspec', style={'color': 'white'}))
    ]
)]

part2 = [html.H1('Welcome', style={'text-align': 'center', 'font-size':'75px'}),
    html.P('This web page provides a user interface for each of the Keck Instruments.', style={'text-align': 'center', 'font-size':'20px'}),
    html.P('Each page is to communicate the diagnoses of the health of the instrument.', style={'text-align': 'center', 'font-size':'20px'}),
    html.Br(),
    daq.ToggleSwitch(
        id='daq-light-dark-theme',
        label=['Light', 'Dark'],
        style={'width': '250px', 'margin': 'auto'},
        value=True
    ),
    html.Div(id='keck1-links', className='indicator-box-dark', children=[
        html.H4('Keck I'),
        html.P(dcc.Link('HIRES', href='/hires-dark', style={'color': 'white'})),
        html.P(dcc.Link('LRIS', href='/lris-dark', style={'color': 'white'})),
        html.P(dcc.Link('MOSFIRE', href='/mosfire-dark', style={'color': 'white'})),
        html.P(dcc.Link('OSIRIS', href='/osiris-dark', style={'color': 'white'}))
    ]),
    html.Div(id='keck2-links', className='indicator-box-dark', children=[
        html.H4('Keck II'),
        html.P(dcc.Link('DEIMOS', href='/deimos-dark', style={'color': 'white'})),
        html.P(dcc.Link('ESI', href='/esi-dark', style={'color': 'white'})),
        html.P(dcc.Link('KCWI', href='/kcwi-dark', style={'color': 'white'})),
        html.P(dcc.Link('NIRES', href='/nires-dark', style={'color': 'white'})),
        html.P(dcc.Link('NIRC2', href='/nirc2-dark', style={'color': 'white'})),
        html.P(dcc.Link('NIRSPEC', href='/nirspec-dark', style={'color': 'white'}))
    ]
)]

layout = html.Div(id='page-content-main', className='page-content-class', children=part1)

@app.callback(
    [Output('page-content-main', 'children')],
    [Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        dark = True
        return [part2]
    else:
        dark = False
        return [part1]
