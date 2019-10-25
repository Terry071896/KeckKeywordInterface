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
from apps import main_page

theme = {
        'dark': True,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : '-dark'}

histKeys = Keywords()
##### Check Settings Tab
settings_keywords = Keywords()

rootLayout1 = html.Div([
    html.Div(id='dark-nirspec-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='dark-nirspec-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container2', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='dark-nirspec-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container3', children=[
            html.H4('Power Check'),
            daq.Indicator(
                id='dark-nirspec-power-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container4', children=[
            html.H4('Temperature Check'),
            daq.Indicator(
                id='dark-nirspec-temperature-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container5', children=[
            html.H4('Pressure Check'),
            daq.Indicator(
                id='dark-nirspec-pressure-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-summary-container6', children=[
            html.H4('Mechanisms Check'),
            daq.Indicator(
                id='dark-nirspec-mechanism-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ])
    ]),
    html.Br(),
    html.Div(id='dark-legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='dark-nirspec-stop-button')
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-legend-status', children=[
            html.H4("Legend"),
            daq.Indicator( width = 30,
                id='dark-legend-green',
                value=True,
                color='green',
                label='OK ='
            ),
            daq.Indicator( width = 30,
                id='dark-legend-yellow',
                value=True,
                color='yellow',height=20,
                label='Warning ='
            ),
            daq.Indicator( width = 30,
                height = 30,
                id='dark-legend-red',
                value=True,
                color='red',
                label='Off/Error ='
            ),
            daq.Indicator( width = 30,
                id='dark-legend-blue',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='dark-nirspec-welcome-link')
    ])
])

#### Check Servers/Computers Tab
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
    html.Div(id='dark-nirspec-servers-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Servers'),
        html.Div(id='dark-nirspec-servers-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-nspec-check',
                value=True,
                color='blue',height=30,
                label='nspec',
                width = 30
            ),
            daq.Indicator(
                id='dark-nscam-check',
                value=True,
                color='blue',height=30,
                label='nscam',
                width = 30
            ),
            daq.Indicator(
                id='dark-nsdewar-check',
                value=True,
                color='blue',height=30,
                label='nsdewar',
                width = 30
            ),
            daq.Indicator(
                id='dark-nsheaders-check',
                value=True,
                color='blue',height=30,
                label='nsheaders',
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-servers-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-nsmotor-check',
                value=True,
                color='blue',height=30,
                label='nsmotor',
                width = 30
            ),
            daq.Indicator(
                id='dark-nspower-check',
                value=True,
                color='blue',height=30,
                label='nspower',
                width = 30
            ),
            daq.Indicator(
                id='dark-nsmon-check',
                value=True,
                color='blue',height=30,
                label='nsmon',
                width = 30
            )
        ])
    ]),
    html.Div(id='dark-nirspec-computer-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Computers'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-nirspecserver-check',
                value=True,
                color='blue',height=30,
                label='nirspecserver',
                width = 30
            ),
            daq.Indicator(
                id='dark-nirspectarg-spec-check',
                value=True,
                color='blue',height=30,
                label='nirspectarg-spec',
                width = 30
            ),
            daq.Indicator(
                id='dark-nirspectarg-scam-check',
                value=True,
                color='blue',height=30,
                label='nirspectarg-scam',
                width = 30
            ),
            daq.Indicator(
                id='dark-vm-nirspec-check',
                value=True,
                color='blue',height=30,
                label='vm-nirspec',
                width = 30
            )
        ])
    ])
])

check_power = Keywords()
powerOutlets = []
powerOutletNames = {}
for letter in ['a','b','c','d']:
    for number in range(1,9):
        key = '%s%s' % (letter,str(number))
        powerOutlets.append(['nspower', 'outlet_%s' % (key)])
        powerOutletNames[key] = check_power.get_keyword('nspower', 'outlet_%s_name' % (key))

powerRoot2 = html.Div([
    html.Div(id='dark-nirspec-power-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Power Outlets'),
        html.Div(id='dark-nirspec-power-container1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[0][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a1'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[1][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a2'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[2][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a3'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[3][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a4'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[4][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a5'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[5][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a6'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[6][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a7'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[7][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['a8'],
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-power-container2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[8][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b1'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[9][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b2'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[10][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b3'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[11][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b4'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[12][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b5'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[13][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b6'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[14][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b7'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[15][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['b8'],
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-power-container3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[16][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c1'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[17][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c2'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[18][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c3'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[19][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c4'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[20][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c5'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[21][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c6'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[22][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c7'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[23][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['c8'],
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-power-container4', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[24][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d1'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[25][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d2'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[26][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d3'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[27][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d4'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[28][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d5'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[29][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d6'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[30][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d7'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (powerOutlets[31][1]),
                value=True,
                color='blue',height=30,
                label=powerOutletNames['d8'],
                width = 30
            )
        ])
    ])
])

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
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-detector-container', children=[
        html.H4('Detector and ASIC Temperature'),
        html.Div(id='dark-nirspec-detector1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[0]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[0]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[1]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[1]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[2]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[2]['KEYWORD'],
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-detector2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[3]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[3]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[4]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[4]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[5]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[5]['KEYWORD'],
                width = 30
            )
        ]),
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-nirspec-dewar-container', children=[
        html.H4('Dewar Internal Temperature'),
        html.Div(id='dark-nirspec-dewar1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[6]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[6]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[7]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[7]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[8]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[8]['KEYWORD'],
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-dewar2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[9]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[9]['KEYWORD'],
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (tempCheckQ[10]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label=tempCheckQ[10]['KEYWORD'],
                width = 30
            )
        ])
    ])
])

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
    html.Div(id='dark-nirspec-mechanism-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Individual Mechanisms'),
        html.Div(id='dark-nirspec-mechanism1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[0][1]),
                value=True,
                color='blue',height=30,
                label='Internal Rotator',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[1][1]),
                value=True,
                color='blue',height=30,
                label='SPEC Filter Wheel 1',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[2][1]),
                value=True,
                color='blue',height=30,
                label='SPEC Filter Wheel 2',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[3][1]),
                value=True,
                color='blue',height=30,
                label='SCAM Filter Wheel',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[4][1]),
                value=True,
                color='blue',height=30,
                label='Slit Wheel',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[5][1]),
                value=True,
                color='blue',height=30,
                label='Echelle Grating',
                width = 30
            )
        ]),
        html.Div(id='dark-nirspec-mechanism2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[6][1]),
                value=True,
                color='blue',height=30,
                label='Cross Disperser Grating',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[7][1]),
                value=True,
                color='blue',height=30,
                label='Calibration Mirror',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[8][1]),
                value=True,
                color='blue',height=30,
                label='Calibration Pin Hole Stage',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[9][1]),
                value=True,
                color='blue',height=30,
                label='Instrument Hatch',
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (mechanismCheckQ[10][1]),
                value=True,
                color='blue',height=30,
                label='FEU Flip mirror',
                width = 30
            )
        ])
    ])
])

layout = [
    dcc.Tabs(id="nirspec-tabs", value='nirspec-tabs', children=[
        dcc.Tab(id='dark-nirspec-tab1', label='NIRSPEC Summary', value='nirspec-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=False, children=[
            html.Br(),
            html.Div(id='dark-nirspec-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='dark-nirspec-polling-interval',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-nirspec-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='dark-nirspec-tab2', label='NIRSPEC Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=False, children=[
            html.Div(id='dark-nirspec-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='dark-nirspec-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='dark-nirspec-subtab4', label='All Servers/Computers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=serversRoot2)),
                        dcc.Tab(id='dark-nirspec-subtab1', label='Power Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='dark-nirspec-subtab2', label='Temperatures', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='dark-nirspec-subtab3', label='Mechanisms', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=mechanismRoot2))
                    ])
                ]),
            dcc.Interval(id='dark-nirspec-polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-nirspec-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='dark-nirspec-tabs-content')
]

inputs_intervals = [Input('dark-nirspec-polling-interval', 'n_intervals'), Input('dark-nirspec-polling-interval2', 'n_intervals')]
outputs = []
for x in serverUpQ:
    outputs.append(Output('dark-%s-check' % (x[0]), 'color'))
    outputs.append(Output('dark-%s-check' % (x[0]), 'height'))
for x in computerUpQ:
    outputs.append(Output('dark-%s-check' % (x), 'color'))
    outputs.append(Output('dark-%s-check' % (x), 'height'))

outputs.append(Output('dark-nirspec-server-check', 'color'))
outputs.append(Output('dark-nirspec-server-check', 'height'))
outputs.append(Output('dark-nirspec-server-check', 'label'))

outputs.append(Output('dark-nirspec-computer-check', 'color'))
outputs.append(Output('dark-nirspec-computer-check', 'height'))
outputs.append(Output('dark-nirspec-computer-check', 'label'))
@app.callback(
    outputs,
    inputs_intervals
)
def populate_servers_computers(n_intervals1, n_intervals2):
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
        if check_computers.ping_computer(x):
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
    outputs.append(Output('dark-%s-check' % (x[1]), 'color'))
    outputs.append(Output('dark-%s-check' % (x[1]), 'height'))

outputs.append(Output('dark-nirspec-power-check', 'color'))
outputs.append(Output('dark-nirspec-power-check', 'height'))
outputs.append(Output('dark-nirspec-power-check', 'label'))
@app.callback(
    outputs,
    inputs_intervals
)
def populate_power(n_intervals1, n_intervals2):
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
    outputs.append(Output('dark-%s-check' % (x['KEYWORD']), 'color'))
    outputs.append(Output('dark-%s-check' % (x['KEYWORD']), 'height'))
outputs.append(Output('dark-nirspec-temperature-check', 'color'))
outputs.append(Output('dark-nirspec-temperature-check', 'height'))
outputs.append(Output('dark-nirspec-temperature-check', 'label'))
@app.callback(
    outputs,
    inputs_intervals
)
def populate_temperatures(n_intervals1, n_intervals2):
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
    outputs.append(Output('dark-%s-check' % (x[1]), 'color'))
    outputs.append(Output('dark-%s-check' % (x[1]), 'height'))
outputs.append(Output('dark-nirspec-mechanism-check', 'color'))
outputs.append(Output('dark-nirspec-mechanism-check', 'height'))
outputs.append(Output('dark-nirspec-mechanism-check', 'label'))
@app.callback(
    outputs,
    inputs_intervals
)
def populate_mechanisms(n_intervals1, n_intervals2):
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

@app.callback(
    [Output('dark-nirspec-pressure-check', 'color'),
    Output('dark-nirspec-pressure-check', 'height'),
    Output('dark-nirspec-pressure-check', 'label')],
    [Input('dark-nirspec-polling-interval', 'n_intervals')]
)
def populate_pressure(n_intervals):
    stats = []
    if 10**(-9) <= float(check_servers.get_keyword('nsdewar', 'vacuum')) <= 10**(-7):
        stats.append('green')
        stats.append(0)
        stats.append('OK')
    else:
        stats.append('red')
        stats.append(50)
        stats.append('ERROR')
    return stats
