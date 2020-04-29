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
        'dark': True,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : '-dark'}

histKeys = Keywords()

###################### First Tab Layout ######################
rootLayout1 = html.Div([
    html.Div(id='nirspec-summary-container', children=[
        html.Div(className='indicator-box', id='nirspec-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='nirspec-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box', id='nirspec-summary-container2', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='nirspec-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='nirspec-summary-container3', children=[
            html.H4('Power Check'),
            daq.Indicator(
                id='nirspec-power-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='nirspec-summary-container4', children=[
            html.H4('Temperature Check'),
            daq.Indicator(
                id='nirspec-temperature-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='nirspec-summary-container5', children=[
            html.H4('Pressure Check'),
            daq.Indicator(
                id='nirspec-pressure-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='nirspec-summary-container6', children=[
            html.H4('Mechanisms Check'),
            daq.Indicator(
                id='nirspec-mechanism-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ])
    ]),
    html.Br(),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box', children=[
            daq.StopButton(id='nirspec-stop-button')
        ]),
        html.Div(className='indicator-box', id='legend-status', children=[
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
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box', id='nirspec-welcome-link')
    ])
])
###################### Second Tab Layout ######################
###############################################################

###################### Check Servers/Computers Tab ######################
check_servers = Keywords()
serverUpQ = []
serverUpQ.append(['nspec','uptime'])
serverUpQ.append(['nscam','uptime'])
serverUpQ.append(['nsdewar','autoemis'])
serverUpQ.append(['nsheaders','uptime'])
serverUpQ.append(['nsmotor','xenon'])
serverUpQ.append(['nspower','DISP1CLK'])
serverUpQ.append(['nsmon','DEWARMECHREM'])

check_computers = Keywords()
computerUpQ = ['nirspecserver', 'nirspectarg-spec', 'nirspectarg-scam', 'vm-nirspec']

serversRoot2 = html.Div([
    html.Div(id='nirspec-servers-container', className='indicator-box', children=[
        html.H4('Servers'),
        html.Div(id='nirspec-servers-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='nspec-check',
                value=True,
                color='blue',height=30,
                label='nspec',
                width = 30
            ),
            daq.Indicator(
                id='nscam-check',
                value=True,
                color='blue',height=30,
                label='nscam',
                width = 30
            ),
            daq.Indicator(
                id='nsdewar-check',
                value=True,
                color='blue',height=30,
                label='nsdewar',
                width = 30
            ),
            daq.Indicator(
                id='nsheaders-check',
                value=True,
                color='blue',height=30,
                label='nsheaders',
                width = 30
            )
        ]),
        html.Div(id='nirspec-servers-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='nsmotor-check',
                value=True,
                color='blue',height=30,
                label='nsmotor',
                width = 30
            ),
            daq.Indicator(
                id='nspower-check',
                value=True,
                color='blue',height=30,
                label='nspower',
                width = 30
            ),
            daq.Indicator(
                id='nsmon-check',
                value=True,
                color='blue',height=30,
                label='nsmon',
                width = 30
            )
        ])
    ]),
    html.Div(id='nirspec-computer-container', className='indicator-box', children=[
        html.H4('Computers'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='nirspecserver-check',
                value=True,
                color='blue',height=30,
                label='nirspecserver',
                width = 30
            ),
            daq.Indicator(
                id='nirspectarg-spec-check',
                value=True,
                color='blue',height=30,
                label='nirspectarg-spec',
                width = 30
            ),
            daq.Indicator(
                id='nirspectarg-scam-check',
                value=True,
                color='blue',height=30,
                label='nirspectarg-scam',
                width = 30
            ),
            daq.Indicator(
                id='vm-nirspec-check',
                value=True,
                color='blue',height=30,
                label='vm-nirspec',
                width = 30
            )
        ])
    ])
])

###################### Power Tab ######################
check_power = Keywords()
powerOutlets = []
powerOutletNames = {}
for letter in ['a','b','c','d']:
    for number in range(1,9):
        key = '%s%s' % (letter,str(number))
        powerOutlets.append(['nspower', 'outlet_%s' % (key)])
        powerOutletNames[key] = check_power.get_keyword('nspower', 'outlet_%s_name' % (key))

powerRoot2 = html.Div([
    html.Div(id='nirspec-power-container', className='indicator-box', children=[
        html.H4('Power Outlets'),
        html.Div(id='nirspec-power-container1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (powerOutlets[0][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a1'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[1][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a2'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[2][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a3'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[3][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a4'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[4][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a5'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[5][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a6'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[6][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a7'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[7][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a8'],
                width = 30
            )
        ]),
        html.Div(id='nirspec-power-container2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (powerOutlets[8][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b1'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[9][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b2'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[10][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b3'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[11][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b4'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[12][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b5'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[13][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b6'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[14][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b7'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[15][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b8'],
                width = 30
            )
        ]),
        html.Div(id='nirspec-power-container3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (powerOutlets[16][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c1'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[17][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c2'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[18][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c3'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[19][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c4'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[20][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c5'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[21][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c6'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[22][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c7'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[23][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c8'],
                width = 30
            )
        ]),
        html.Div(id='nirspec-power-container4', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (powerOutlets[24][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d1'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[25][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d2'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[26][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d3'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[27][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d4'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[28][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d5'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[29][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d6'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[30][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d7'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (powerOutlets[31][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d8'],
                width = 30
            )
        ])
    ])
])

###################### Temperature Tab ######################
check_temperature = Keywords()
tempCheckQ = []
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'spectemp1val', 'MINVALUE':29, 'MAXVALUE':31, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'spectemp2val', 'MINVALUE':29, 'MAXVALUE':31, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'scamtemp1val', 'MINVALUE':29, 'MAXVALUE':31, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'scamtemp2val', 'MINVALUE':29, 'MAXVALUE':31, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'specasicval', 'MINVALUE':55, 'MAXVALUE':63, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'scamasicval', 'MINVALUE':49, 'MAXVALUE':55, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'optplateval', 'MINVALUE':49, 'MAXVALUE':61, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'bench1inval', 'MINVALUE':47, 'MAXVALUE':57, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'bench2inval', 'MINVALUE':47, 'MAXVALUE':57, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'ccr1050val', 'MINVALUE':40, 'MAXVALUE':52, 'GOODVALUE':'green', 'BADSTATUS':'red'})
tempCheckQ.append({'LIBRARY':'nsdewar', 'KEYWORD':'ccr350val', 'MINVALUE':12, 'MAXVALUE':19, 'GOODVALUE':'green', 'BADSTATUS':'red'})



temperatureRoot2 = html.Div([
    html.Div(className='indicator-box', id='nirspec-detector-container', children=[
        html.H4('Detector and ASIC Temperature'),
        html.Div(id='nirspec-detector1', className='indicator-box-no-border'+class_theme['dark'], children=[
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
            )
        ]),
        html.Div(id='nirspec-detector2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (tempCheckQ[3]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[3]['KEYWORD'],
                width = 30
            ),
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
            )
        ]),
    ]),
    html.Div(className='indicator-box', id='nirspec-dewar-container', children=[
        html.H4('Dewar Internal Temperature'),
        html.Div(id='nirspec-dewar1', className='indicator-box-no-border'+class_theme['dark'], children=[
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
            ),
            daq.Indicator(
                id='%s-check' % (tempCheckQ[8]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[8]['KEYWORD'],
                width = 30
            )
        ]),
        html.Div(id='nirspec-dewar2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (tempCheckQ[9]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[9]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (tempCheckQ[10]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[10]['KEYWORD'],
                width = 30
            )
        ])
    ])
])

###################### Mechanism Tab ######################
check_mechanism = Keywords()
mechanismCheckQ = []
mechanismCheckQ.append(['nsmotor', 'rotatorsta'])
mechanismCheckQ.append(['nsmotor', 'scifilt1sta'])
mechanismCheckQ.append(['nsmotor', 'scifilt2sta'])
mechanismCheckQ.append(['nsmotor', 'scamfiltsta'])
mechanismCheckQ.append(['nsmotor', 'slitsta'])
mechanismCheckQ.append(['nsmotor', 'echellesta'])
mechanismCheckQ.append(['nsmotor', 'xdispersersta'])
mechanismCheckQ.append(['nsmotor', 'calfoldsta'])
mechanismCheckQ.append(['nsmotor', 'pinholesta'])
mechanismCheckQ.append(['nsmotor', 'hatchsta'])
mechanismCheckQ.append(['nsmotor', 'feuflipsta'])

mechanismRoot2 = html.Div([
    html.Div(id='nirspec-mechanism-container', className='indicator-box', children=[
        html.H4('Individual Mechanisms'),
        html.Div(id='nirspec-mechanism1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[0][1]),
                value=True,
                color='blue',height=30,
                label='Internal Rotator',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[1][1]),
                value=True,
                color='blue',height=30,
                label='SPEC Filter Wheel 1',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[2][1]),
                value=True,
                color='blue',height=30,
                label='SPEC Filter Wheel 2',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[3][1]),
                value=True,
                color='blue',height=30,
                label='SCAM Filter Wheel',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[4][1]),
                value=True,
                color='blue',height=30,
                label='Slit Wheel',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[5][1]),
                value=True,
                color='blue',height=30,
                label='Echelle Grating',
                width = 30
            )
        ]),
        html.Div(id='nirspec-mechanism2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[6][1]),
                value=True,
                color='blue',height=30,
                label='Cross Disperser Grating',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[7][1]),
                value=True,
                color='blue',height=30,
                label='Calibration Mirror',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[8][1]),
                value=True,
                color='blue',height=30,
                label='Calibration Pin Hole Stage',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[9][1]),
                value=True,
                color='blue',height=30,
                label='Instrument Hatch',
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (mechanismCheckQ[10][1]),
                value=True,
                color='blue',height=30,
                label='FEU Flip mirror',
                width = 30
            )
        ])
    ])
])

###################### OVERALL LAYOUT ######################
layout = [
    dcc.Tabs(id="nirspec-tabs", value='nirspec-tabs', children=[
        dcc.Tab(id='nirspec-tab1', label='NIRSPEC Summary', value='nirspec-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Br(),
            html.Div(id='nirspec-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='nirspec-polling-interval',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='nirspec-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='nirspec-tab2', label='NIRSPEC Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Div(id='nirspec-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='nirspec-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='nirspec-subtab4', label='All Servers/Computers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=serversRoot2)),
                        dcc.Tab(id='nirspec-subtab1', label='Power Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='nirspec-subtab2', label='Temperatures', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='nirspec-subtab3', label='Mechanisms', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=mechanismRoot2))
                    ])
                ]),
            dcc.Interval(id='nirspec-polling-interval2',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='nirspec-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='nirspec-tabs-content')
]

inputs_intervals = [Input('nirspec-polling-interval', 'n_intervals'), Input('nirspec-polling-interval2', 'n_intervals')]
outputs = []
for x in serverUpQ:
    outputs.append(Output('%s-check' % (x[0]), 'color'))
    outputs.append(Output('%s-check' % (x[0]), 'height'))
for x in computerUpQ:
    outputs.append(Output('%s-check' % (x), 'color'))
    outputs.append(Output('%s-check' % (x), 'height'))

outputs.append(Output('nirspec-server-check', 'color'))
outputs.append(Output('nirspec-server-check', 'height'))
outputs.append(Output('nirspec-server-check', 'label'))

outputs.append(Output('nirspec-computer-check', 'color'))
outputs.append(Output('nirspec-computer-check', 'height'))
outputs.append(Output('nirspec-computer-check', 'label'))

nirspec_semaphore = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_servers_computers(n_intervals1, n_intervals2):
    '''
    Server and Computer indicator value checks, update values

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
    with nirspec_semaphore:
        stats = []
        counter1 = 0
        for x in serverUpQ:
            if check_servers.server_up(x[0],x[1]):
                stats.append('green')
                stats.append(0)
                counter1 += 1
            else:
                stats.append('red')
                stats.append(30)
        counter2 = 0
        for x in computerUpQ:
            if check_computers.ping_computer('nirspec', x):
                stats.append('green')
                stats.append(0)
                counter2 += 1
            else:
                stats.append('red')
                stats.append(30)
        if counter1 == len(serverUpQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('OFF/ERROR')

        if counter2 == len(computerUpQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('OFF/ERROR')

        return stats

outputs = []
for x in powerOutlets:
    outputs.append(Output('%s-check' % (x[1]), 'color'))
    outputs.append(Output('%s-check' % (x[1]), 'height'))

outputs.append(Output('nirspec-power-check', 'color'))
outputs.append(Output('nirspec-power-check', 'height'))
outputs.append(Output('nirspec-power-check', 'label'))

nirspec_semaphore1 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_power(n_intervals1, n_intervals2):
    '''
    Power indicator value checks, update values

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
    with nirspec_semaphore1:
        stats = []
        counter = 0
        for x in powerOutlets:
            if check_power.get_keyword(x[0],x[1]) == 'On':
                stats.append('green')
                stats.append(0)
                counter += 1
            else:
                stats.append('red')
                stats.append(30)

        if counter == len(powerOutlets):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('OFF/ERROR')
        return stats

outputs = []
for x in tempCheckQ:
    outputs.append(Output('%s-check' % (x['KEYWORD']), 'color'))
    outputs.append(Output('%s-check' % (x['KEYWORD']), 'height'))
outputs.append(Output('nirspec-temperature-check', 'color'))
outputs.append(Output('nirspec-temperature-check', 'height'))
outputs.append(Output('nirspec-temperature-check', 'label'))

nirspec_semaphore2 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_temperatures(n_intervals1, n_intervals2):
    '''
    Temperature indicator value checks, update values

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
    with nirspec_semaphore2:
        stats = []
        counter = 0
        for x in tempCheckQ:
            if x['MINVALUE'] <= float(check_temperature.get_keyword(x['LIBRARY'], x['KEYWORD'])) <= x['MAXVALUE']:
                stats.append(x['GOODVALUE'])
                stats.append(0)
                counter += 1
            else:
                stats.append(x['BADSTATUS'])
                stats.append(30)
        if counter == len(tempCheckQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('OFF/ERROR')
        return stats

outputs = []
for x in mechanismCheckQ:
    outputs.append(Output('%s-check' % (x[1]), 'color'))
    outputs.append(Output('%s-check' % (x[1]), 'height'))
outputs.append(Output('nirspec-mechanism-check', 'color'))
outputs.append(Output('nirspec-mechanism-check', 'height'))
outputs.append(Output('nirspec-mechanism-check', 'label'))

nirspec_semaphore3 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_mechanisms(n_intervals1, n_intervals2):
    '''
    Mechanism indicator value checks, update values

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
    with nirspec_semaphore3:
        stats = []
        counterG = 0
        counterY = 0
        for x in mechanismCheckQ:
            temp = check_mechanism.get_keyword(x[0],x[1])
            if temp == 'Ready':
                stats.append('green')
                stats.append(0)
                counterG += 1
            elif temp == 'Halted':
                stats.append('yellow')
                stats.append(20)
                counterY += 1
            else:
                stats.append('red')
                stats.append(30)
        if counterG == len(mechanismCheckQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        elif counterG + counterY == len(mechanismCheckQ):
            stats.append('yellow')
            stats.append(40)
            stats.append('Halted')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('OFF/ERROR')
        return stats

nirspec_semaphore4 = threading.Semaphore()
@app.callback(
    [Output('nirspec-pressure-check', 'color'),
    Output('nirspec-pressure-check', 'height'),
    Output('nirspec-pressure-check', 'label'),
    Output('nirspec-tab1', 'disabled'),
    Output('nirspec-tab2', 'disabled')],
    [Input('nirspec-polling-interval', 'n_intervals')]
)
def populate_pressure(n_intervals):
    '''
    Pressure indicator value checks, update values

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
    with nirspec_semaphore4:
        stats = []
        if 10**(-9) <= float(check_servers.get_keyword('nsdewar', 'vacuum')) <= 10**(-7):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('ERROR')
        stats.append(False)
        stats.append(False)
        return stats
