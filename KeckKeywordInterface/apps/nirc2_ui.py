# Author: Terry Cox
# GitHub: https://github.com/KeckObservatory/KeckKeywordInterface
# Email: tcox@keck.hawaii.edu, tfcox1703@gmail.com

__author__ = ['Terry Cox', 'Luca Rizzi']
__version__ = '1.0.1'
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

from KeckKeywordInterface.keywords import Keywords
from KeckKeywordInterface.app import app
from KeckKeywordInterface.apps import main_page
import threading

theme = {
        'dark': False,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : ''}


###################### First Tab Layout ######################
summaryCheck = []
check_summary = Keywords()

summaryCheck.append({'id':'nirc2-alad-keys-check', 'LIBRARY':'alad', 'KEYWORD':'itime'})
summaryCheck.append({'id':'nirc2-motor-daemon-check', 'LIBRARY':'nirc2', 'KEYWORD':'lock'})
summaryCheck.append({'id':'nirc2-motor-key-check', 'LIBRARY':'nirc2', 'KEYWORD':'camraw'})
summaryCheck.append({'id':'nirc2-io-daemon-check', 'LIBRARY':'nirc2', 'KEYWORD':'tm_temp3'})

rootLayout1 = html.Div([
    html.Div(id='nirc2-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-summary-container1', children=[
            html.H4('Alad Keys Check'),
            daq.Indicator(
                id='nirc2-alad-keys-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-summary-container2', children=[
            html.H4('Motor Daemon Check'),
            daq.Indicator(
                id='nirc2-motor-daemon-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-summary-container3', children=[
            html.H4('Motor Key Check'),
            daq.Indicator(
                id='nirc2-motor-key-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-summary-container6', children=[
            html.H4('IO Daemon Check'),
            daq.Indicator(
                id='nirc2-io-daemon-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ])
    ]),
    html.Br(),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='nirc2-stop-button')
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='legend-status', children=[
            html.H4("Legend"),
            daq.Indicator( width = 30,
                id='legend-green',
                value=True,
                color='green',
                label='OK ='
            ),
            daq.Indicator( width = 30,
                id='legend-yellow',
                value=True,
                color='yellow',height=20,
                label='Warning ='
            ),
            daq.Indicator( width = 30,
                height = 30,
                id='legend-red',
                value=True,
                color='red',
                label='Off/Error ='
            ),
            daq.Indicator( width = 30,
                id='legend-blue',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='nirc2-welcome-link')
    ])
])


###################### Second Tab Layout ######################
###############################################################

###################### Temperature Tab ######################
check_temperature = Keywords()
tempCheckQ = []
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tdetblck'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tgetter'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'thead2lo'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tcamera'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tcoll'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tbench'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tshield'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'thead1'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tc_setpa'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tempdet'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'tc_setpb'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'thead2hi'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'htrdetblck'})
tempCheckQ.append({'NAME':'', 'LIBRARY':'nirc2', 'KEYWORD':'htrhead2hi'})

indicatorList = []
for x in tempCheckQ:
    indicatorList.append(daq.Indicator(
        id='%s-check' % (tempCheckQ[0]['KEYWORD']),
        value=True,
        color='blue',height=30,
        label=tempCheckQ[0]['KEYWORD'],
        width = 30
    ))

temperatureRoot2 = html.Div([
    html.Div(id='nirc2-temperatures-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Temperatures'),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-temperatures-1', children=[
            html.Div(id='nirc2-temperatures-1.1', className='indicator-box-no-border'+class_theme['dark'], children=[
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[0]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[0]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[1]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[1]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[2]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[2]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[3]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[3]['KEYWORD'],
                    width = 30
                )
            ]),
            html.Div(id='nirc2-temperatures-1.2', className='indicator-box-no-border'+class_theme['dark'], children=[
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[4]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[4]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[5]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[5]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[6]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[6]['KEYWORD'],
                    width = 30
                ),
                daq.Indicator(
                    id='%s-check' % (tempCheckQ[7]['KEYWORD']),
                    value=True,
                    color='blue',height=30,
                    label=tempCheckQ[7]['KEYWORD'],
                    width = 30
                )
            ])
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-temperatures-2', children=[
            daq.Indicator(
                id='%s-check' % (tempCheckQ[8]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[8]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (tempCheckQ[9]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[9]['KEYWORD'],
                width = 30
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-temperatures-3', children=[
            daq.Indicator(
                id='%s-check' % (tempCheckQ[10]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[10]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (tempCheckQ[11]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[11]['KEYWORD'],
                width = 30
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='nirc2-temperatures-4', children=[
            daq.Indicator(
                id='%s-check' % (tempCheckQ[12]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[12]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (tempCheckQ[13]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[13]['KEYWORD'],
                width = 30
            )
        ])
    ])
])


###################### OVERALL LAYOUT ######################

layout = [
    dcc.Tabs(id="nirc2-tabs", value='nirc2-tabs', children=[
        dcc.Tab(id='nirc2-tab1', label='NIRC2 Summary', value='nirc2-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Br(),
            html.Div(id='nirc2-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='nirc2-polling-interval',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='nirc2-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='nirc2-tab2', label='NIRC2 Temperatures', value='nirc2-tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Div(id='nirc2-dark-theme-component-demo2',
                children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
            dcc.Interval(id='nirc2-polling-interval2',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='nirc2-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='nirc2-tabs-content')
]

inputs_intervals = [Input('nirc2-polling-interval', 'n_intervals'), Input('nirc2-polling-interval2', 'n_intervals')]
outputs = []
for x in summaryCheck:
    outputs.append(Output(x['id'], 'color'))
    outputs.append(Output(x['id'], 'label'))
    outputs.append(Output(x['id'], 'height'))

nirc2_semaphore = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_servers_computers(n_intervals1, n_intervals2):
    '''
    Server indicator value checks, update values

    Parameters
    ----------
    n_intervals1 : int
        number of milliseconds passed since start updates for page 1.
    n_intervals2 : int
        number of milliseconds passed since start updates for page 2.

    Returns
    -------
    list
        list of values in order expressed in Output callback list.
    '''
    with nirc2_semaphore:
        stats = []
        for x in summaryCheck:
            if check_summary.server_up(x['LIBRARY'], x['KEYWORD']):
                stats.append('green')
                stats.append('Good')
                stats.append(0)
            else:
                stats.append('red')
                stats.append('ERROR')
                stats.append(50)
        return stats
