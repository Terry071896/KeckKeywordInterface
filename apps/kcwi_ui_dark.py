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
from apps import main_page
import threading

binary_keywords = []
for i in range(0,13):
    binary_keywords.append('uptime')
binary_keywords.append('TESTINT1')
for i in ['A','B','C']:
    for j in range(1,9):
        binary_keywords.append('PWSTAT'+str(j)+i)
    for j in range(1,9):
        binary_keywords.append('PWNAME'+str(j)+i)

binary_keywords[0] = binary_keywords[0] +'kt1s'
binary_keywords[1] = binary_keywords[1] +'kt2s'
binary_keywords[2] = binary_keywords[2] +'kp1s'
binary_keywords[3] = binary_keywords[3] +'kp2s'
binary_keywords[4] = binary_keywords[4] +'kp3s'
binary_keywords[5] = binary_keywords[5] +'kbgs'
binary_keywords[6] = binary_keywords[6] +'kbvs'
binary_keywords[7] = binary_keywords[7] +'kbds'
binary_keywords[8] = binary_keywords[8] +'kfcs'
binary_keywords[9] = binary_keywords[9] +'kbes'
binary_keywords[10] = binary_keywords[10] +'kbms'
binary_keywords[11] = binary_keywords[11] +'kros'
binary_keywords[12] = binary_keywords[12] +'kcas'

allServers = ['kt1s',
'kt2s',
'kp1s',
'kp2s',
'kp3s',
'kbgs',
'kbvs',
'kbds',
'kfcs',
'kbes',
'kbms',
'kros',
'kcas',
'kcwi']

server = []
for i in allServers:
    server.append(i)

for i in range(1,4):
    for j in range(1,17):
        server.append('kp'+str(i)+'s')

kcwiKeywords = Keywords(server, binary_keywords)
histKeys = Keywords()



theme = {
        'dark': True,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : '-dark'}

rootLayout = html.Div([
        html.Div(id='dark-SERVER-container', children=[
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-temperature-servers', children=[
                html.H4('Temperature'),
                daq.Indicator( width = 30,
                    id='dark-kt1s-status',
                    value=True,
                    color='blue',height=30,
                    label='kt1s'
                ),
                daq.Indicator( width = 30,
                    id='dark-kt2s-status',
                    value=True,
                    color='blue',height=30,
                    label='kt2s'
                )
            ]),
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-power-servers', children=[
                html.H4("Power"),
                daq.Indicator( width = 30,
                    id='dark-kp1s-status',
                    value=True,
                    color='blue',height=30,
                    label='kp1s'
                ),
                daq.Indicator( width = 30,
                    id='dark-kp2s-status',
                    value=True,
                    color='blue',height=30,
                    label='kp2s'
                ),
                daq.Indicator( width = 30,
                    id='dark-kp3s-status',
                    value=True,
                    color='blue',height=30,
                    label='kp3s'
                )
            ]),
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-pressure-servers', children=[
                html.H4("Pressure"),
                daq.Indicator( width = 30,
                    id='dark-kbgs-status',
                    value=True,
                    color='blue',height=30,
                    label='kbgs'
                ),
                daq.Indicator( width = 30,
                    id='dark-kbvs-status',
                    value=True,
                    color='blue',height=30,
                    label='kbvs'
                )
            ]),
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-detector-servers', children=[
                html.H4("Detector"),
                daq.Indicator( width = 30,
                    id='dark-kbds-status',
                    value=True,
                    color='blue',height=30,
                    label='kbds'
                ),
                daq.Indicator( width = 30,
                    id='dark-kfcs-status',
                    value=True,
                    color='blue',height=30,
                    label='kfcs'
                )
            ]),
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-mechanism-servers', children=[
                html.H4("Mechanisms"),
                daq.Indicator( width = 30,
                    id='dark-kbes-status',
                    value=True,
                    color='blue',height=30,
                    label='kbes'
                ),
                daq.Indicator( width = 30,
                    id='dark-kbms-status',
                    value=True,
                    color='blue',height=30,
                    label='kbms'
                ),
                daq.Indicator( width = 30,
                    id='dark-kros-status',
                    value=True,
                    color='blue',height=30,
                    label='kros'
                ),
                daq.Indicator( width = 30,
                    id='dark-kcas-status',
                    value=True,
                    color='blue',height=30,
                    label='kcas'
                )
            ]),
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-global-servers', children=[
                html.H4("Global"),
                daq.Indicator( width = 30,
                    id='dark-kcwi-status',
                    value=True,
                    color='blue',height=30,
                    label='kcwi'
                )
            ])
        ])
])

rootLayout1 = html.Div([
    html.Br(),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-settings-container1', children=[
        html.H4('Blue CCD Temperature Check'),
        daq.Indicator(
            id='dark-tmp1-check',
            value=True,
            color='blue',height=50,
            label='Loading...',
            width = 50
        ),
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-settings-container2', children=[
        html.H4('CCD Power Check'),
        daq.Indicator(
            id='dark-ccdpower-check',
            value=True,
            color='blue',height=50,
            label='Loading...',
            width = 50
        )
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-settings-container3', children=[
        html.H4('Ion Pump Check'),
        daq.Indicator(
            id='dark-hvon-check',
            value=True,
            color='blue',height=50,
            label='Loading...',
            width = 50
        )
    ]),
    html.Br(),
    html.Div(id='dark-legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='dark-stop-button')
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
                id='dark-legend-red',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ])
    ]),
    html.Br(),
    dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='dark-welcome-link')
])

temperature_layout_dark = go.Layout(
    yaxis=dict(
        title='K',
        range=[0, 273],
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    xaxis=dict(
        title='Date',
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    height=505,
    plot_bgcolor="#313336",
    paper_bgcolor="#303030",
    legend=go.layout.Legend(font=dict(color='white'))
)
temperature_layout = go.Layout(
    yaxis=dict(
        title='K',
        range=[0, 273]
    ),
    xaxis=dict(
        title='Date'
    ),
    height=505,
    plot_bgcolor="#f3f3f3"
)

temperatureRoot2 = html.Div(style={'overflow':'scroll'}, children=[
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-graph-container1', children=[
        html.H4('Blue CCD Temperature'),
        dcc.Graph(
            id='dark-temperature-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': temperature_layout_dark
            }),
        )
    ]),
    html.Div(id='dark-legend-container2', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-dropdown-container1', children=[
            html.H4('Temperature History'),
            html.Div(className='dropdown-theme'+class_theme['dark'], id='dark-dropdown1', children=[
                dcc.Dropdown(
                    id='dark-temperature-graph-dropdown',
                    options=[
                        {'label': '1 Day Ago', 'value': 'day'},
                        {'label': '1 Week Ago', 'value': 'week'},
                        {'label': '1 Month Ago', 'value': 'month'},
                        {'label': 'None', 'value': 'fake'}
                    ],
                    value='fake',
                    style=theme
                )
            ])
        ]),
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-tmp1-container', children=[
        html.H4("Blue CCD Temperature"),
        daq.Thermometer(id='dark-tmp1-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp1-k-temperature',
            value='000000',
            color='blue',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp1-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-tmp7-container', children=[
        html.H4("Cab Interior Temperature"),
        daq.Thermometer(id='dark-tmp7-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp7-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp7-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-tmp8-container', children=[
        html.H4("Blue Fill Temperature"),
        daq.Thermometer(id='dark-tmp8-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp8-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='dark-tmp8-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ])
])

powerRoot2 = html.Div([
    html.Div(id='dark-PWSTATA-container', children=[
            html.Div(className='indicator-box'+class_theme['dark'], id='dark-pwstata-status', children=[
                html.H4("Power Bank A"),
                daq.Indicator( width = 30,
                    id='dark-pwa1-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 1'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa2-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 2'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa3-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 3'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa4-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 4'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa5-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 5'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa6-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 6'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa7-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 7'
                ),
                daq.Indicator( width = 30,
                    id='dark-pwa8-status',
                    value=True,
                    color='blue',height=30,
                    label='Port 8'
                )
            ])
        ]),
    html.Div(id='dark-PWSTATB-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-pwstatb-status', children=[
            html.H4("Power Bank B"),
            daq.Indicator( width = 30,
                id='dark-pwb1-status',
                value=True,
                color='blue',height=30,
                label='Port 1'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb2-status',
                value=True,
                color='blue',height=30,
                label='Port 2'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb3-status',
                value=True,
                color='blue',height=30,
                label='Port 3'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb4-status',
                value=True,
                color='blue',height=30,
                label='Port 4'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb5-status',
                value=True,
                color='blue',height=30,
                label='Port 5'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb6-status',
                value=True,
                color='blue',height=30,
                label='Port 6'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb7-status',
                value=True,
                color='blue',height=30,
                label='Port 7'
            ),
            daq.Indicator( width = 30,
                id='dark-pwb8-status',
                value=True,
                color='blue',height=30,
                label='Port 8'
            )
        ])
    ]),
    html.Div(id='dark-PWSTATC-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-pwstatc-status', children=[
            html.H4("Power Bank C"),
            daq.Indicator( width = 30,
                id='dark-pwc1-status',
                value=True,
                color='blue',height=30,
                label='Port 1'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc2-status',
                value=True,
                color='blue',height=30,
                label='Port 2'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc3-status',
                value=True,
                color='blue',height=30,
                label='Port 3'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc4-status',
                value=True,
                color='blue',height=30,
                label='Port 4'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc5-status',
                value=True,
                color='blue',height=30,
                label='Port 5'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc6-status',
                value=True,
                color='blue',height=30,
                label='Port 6'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc7-status',
                value=True,
                color='blue',height=30,
                label='Port 7'
            ),
            daq.Indicator( width = 30,
                id='dark-pwc8-status',
                value=True,
                color='blue',height=30,
                label='Port 8'
            )
        ])
    ])
])

pressure_layout_dark = go.Layout(
    yaxis=dict(
        title='\'Pressure\' (Torr)',
        range=[0, 0.001],
        tickvals=[0.0000001, 0.0001, 0.001],
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    xaxis=dict(
        title='Date',
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    height=505,
    plot_bgcolor="#313336",
    paper_bgcolor="#303030",
    legend=go.layout.Legend(font=dict(color='white'))
)
pressure_layout = go.Layout(
    yaxis=dict(
        title='\'Pressure\' (Torr)',
        range=[0, 0.001],
        tickvals=[0.0000001, 0.0001, 0.001]
    ),
    xaxis=dict(
        title='Date'
    ),
    height=505,
    plot_bgcolor="#f3f3f3"
)

pressureRoot2 = html.Div([
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-graph-container', children=[
        html.H4(kcwiKeywords.get_keyword('kbvs', 'prname')),
        dcc.Graph(
            id='dark-pressure-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': pressure_layout if class_theme['dark'] == '' else pressure_layout_dark
            }),
        )
    ]),
    html.Div(id='dark-legend-container1', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-dropdown-container', children=[
            html.H4('Pressure History'),
            html.Div(className='dropdown-theme'+class_theme['dark'], id='dark-dropdown', children=[
                dcc.Dropdown(
                    id='dark-pressure-graph-dropdown',
                    options=[
                        {'label': '1 Day Ago', 'value': 'day'},
                        {'label': '1 Week Ago', 'value': 'week'},
                        {'label': '1 Month Ago', 'value': 'month'},
                        {'label': 'None', 'value': 'fake'}
                    ],
                    value='fake',
                    style=theme
                )
            ])
        ])
    ]),
    html.Br(),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-pgpress-container', children=[
        html.H4('Blue Pressure Gauge'),
        daq.Gauge(
            id='dark-pgpress-status',
            logarithmic=True,
            min=-4, max=1,
            units="Torr",
            showCurrentValue=True,
        ),
        html.Div([
            daq.Gauge(
                id='dark-pgpress-status1',
                min=0, max=20,
                units="Torr",
                showCurrentValue=True,
                color={
                    "gradient": True,
                    "ranges": {
                        "green": [0, 7],
                        "yellow": [7, 14],
                        "red": [14, 20]
                    }
                },
            ),
            dash_katex.DashKatex(expression='\\textrm{x } 10^{-4}')
        ])
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-thePressure-container', children=[
        html.H4('Blue Vac Ion'),
        daq.Gauge(
            id='dark-thePressure-status',
            logarithmic=True,
            min=-8, max=-5,
            units="Torr",
            showCurrentValue=True,
        ),
        html.Div([
            daq.Gauge(
                id='dark-thePressure-status1',
                min=0, max=100,
                units="Torr",
                showCurrentValue=True,
                color={
                    "gradient": True,
                    "ranges": {
                        "green": [0, 30],
                        "yellow": [30, 70],
                        "red": [70, 100]
                    }
                },
            ),
            dash_katex.DashKatex(expression='\\textrm{x } 10^{-7}')
        ])
    ])
])

serverRoot2 = html.Div([rootLayout])



layout = [
    dcc.Tabs(id="dark-tabs", value='tab-1', children=[
        dcc.Tab(id='dark-tab1', label='KCWI Settings', value='tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Br(),
            html.Div(id='dark-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='dark-polling-interval',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='dark-tab2', label='KCWI Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Div(id='dark-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='dark-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='dark-subtab4', label='All Servers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=serverRoot2)),
                        dcc.Tab(id='dark-subtab1', label='Temperature Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='dark-subtab2', label='Power Servers', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='dark-subtab3', label='Pressure Servers', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='dark-polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='dark-tabs-content')
]


@app.callback(
    [Output('dark-polling-interval', 'disabled'),
     Output('dark-stop-button', 'buttonText')],
    [Input('dark-stop-button', 'n_clicks')],
    state=[State('dark-polling-interval', 'disabled')]
)
def stop_production(_, current):
    return not current, "stop" if current else "start"

kcwi_semaphore = threading.Semaphore()
@app.callback(
    [Output('dark-temperature-graph', 'figure'),
    Output('dark-pressure-graph', 'figure')],
    [Input('dark-pressure-graph-dropdown', 'value'),
    Input('dark-temperature-graph-dropdown', 'value')],
    state=[State('dark-pressure-graph', 'figure'),
    State('dark-temperature-graph', 'figure')]
)
def change_class_name(valueP, valueT, current_figP, current_figT):
    with kcwi_semaphore:
        bVw = list()

        current_data = current_figT['data'][0]
        new_data = [histKeys.get_keyword_history('kt1s', 'tmp1', valueT)]
        current_figT['data'] = new_data
        bVw.append(current_figT)

        current_data = current_figP['data'][0]
        new_data = [histKeys.get_keyword_history('kbvs', 'pressure', valueP)]
        current_figP['data'] = new_data
        bVw.append(current_figP)
        return bVw


kcwi_semaphore1 = threading.Semaphore()
@app.callback(
    [Output('dark-pgpress-status', 'value'),
     Output('dark-pgpress-status1', 'value'),
     Output('dark-thePressure-status', 'value'),
     Output('dark-thePressure-status1', 'value'),
     Output('dark-tmp1-temp', 'value'),
     Output('dark-tmp1-k-temperature', 'value'),
     Output('dark-tmp1-c-temperature', 'value'),
     Output('dark-tmp7-temp', 'value'),
     Output('dark-tmp7-k-temperature', 'value'),
     Output('dark-tmp7-c-temperature', 'value'),
     Output('dark-tmp8-temp', 'value'),
     Output('dark-tmp8-k-temperature', 'value'),
     Output('dark-tmp8-c-temperature', 'value')],
     [Input('dark-polling-interval2', 'n_intervals')]
)
def update_stats2(n_intervals):
    with kcwi_semaphore1:
        print('started update_stats2')
        stats=[]
        pgpress = float(kcwiKeywords.get_keyword('kbgs', 'pgpress'))
        stats.append(pgpress)
        stats.append(pgpress*10**4)
        pressure = float(kcwiKeywords.get_keyword('kbvs', 'pressure'))
        stats.append(pressure)
        stats.append(pressure*10**7)
        tmp1 = round(float(kcwiKeywords.get_keyword('kt1s', 'tmp1')),3)
        tmp7 = round(float(kcwiKeywords.get_keyword('kt2s', 'tmp7')),3)
        tmp8 = round(float(kcwiKeywords.get_keyword('kt2s', 'tmp8')),3)

        for tmp in [tmp1, tmp7, tmp8]:
            stats.append(tmp)
            stats.append(str(tmp))
            stats.append(str(round(tmp-273,3)))
        print('ended update_stats2')
        return stats


kcwi_semaphore2 = threading.Semaphore()
@app.callback(
    [Output('dark-tmp1-check', 'color'),
     Output('dark-tmp1-check', 'label'),
     Output('dark-tmp1-check', 'height'),
     Output('dark-ccdpower-check', 'color'),
     Output('dark-ccdpower-check', 'label'),
     Output('dark-ccdpower-check', 'height'),
     Output('dark-hvon-check', 'color'),
     Output('dark-hvon-check', 'label'),
     Output('dark-hvon-check', 'height'),
     Output('dark-tab1', 'disabled')],
    [Input('dark-polling-interval', 'n_intervals')]
)
def update_stats1(n_intervals):
    with kcwi_semaphore2:
        stats=[]
        print('start update_stats1')
        tmp1 = float(kcwiKeywords.get_keyword('kt1s', 'tmp1'))
        if 161 <= tmp1 <= 165:
            stats.append('green')
            stats.append('Good')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('OFF')
            stats.append(50)

        vals = [kcwiKeywords.get_keyword('kbds', 'ccdpower'),
            kcwiKeywords.get_keyword('kbvs', 'hvon')]
        for val in vals:
            if val == '1':
                stats.append('green')
                stats.append('Good')
                stats.append(0)
            else:
                stats.append('red')
                stats.append('OFF')
                stats.append(50)
        stats.append(False)
        print('ended update_stats1')
        return stats

kcwi_semaphore3 = threading.Semaphore()
@app.callback(
    [Output('dark-kt1s-status', 'color'),
    Output('dark-kt2s-status', 'color'),
    Output('dark-kp1s-status', 'color'),
    Output('dark-kp2s-status', 'color'),
    Output('dark-kp3s-status', 'color'),
    Output('dark-kbgs-status', 'color'),
    Output('dark-kbvs-status', 'color'),
    Output('dark-kbds-status', 'color'),
    Output('dark-kfcs-status', 'color'),
    Output('dark-kbes-status', 'color'),
    Output('dark-kbms-status', 'color'),
    Output('dark-kros-status', 'color'),
    Output('dark-kcas-status', 'color'),
    Output('dark-kcwi-status', 'color'),
    Output('dark-pwa1-status', 'color'),
    Output('dark-pwa2-status', 'color'),
    Output('dark-pwa3-status', 'color'),
    Output('dark-pwa4-status', 'color'),
    Output('dark-pwa5-status', 'color'),
    Output('dark-pwa6-status', 'color'),
    Output('dark-pwa7-status', 'color'),
    Output('dark-pwa8-status', 'color'),
    Output('dark-pwa1-status', 'label'),
    Output('dark-pwa2-status', 'label'),
    Output('dark-pwa3-status', 'label'),
    Output('dark-pwa4-status', 'label'),
    Output('dark-pwa5-status', 'label'),
    Output('dark-pwa6-status', 'label'),
    Output('dark-pwa7-status', 'label'),
    Output('dark-pwa8-status', 'label'),
    Output('dark-pwb1-status', 'color'),
    Output('dark-pwb2-status', 'color'),
    Output('dark-pwb3-status', 'color'),
    Output('dark-pwb4-status', 'color'),
    Output('dark-pwb5-status', 'color'),
    Output('dark-pwb6-status', 'color'),
    Output('dark-pwb7-status', 'color'),
    Output('dark-pwb8-status', 'color'),
    Output('dark-pwb1-status', 'label'),
    Output('dark-pwb2-status', 'label'),
    Output('dark-pwb3-status', 'label'),
    Output('dark-pwb4-status', 'label'),
    Output('dark-pwb5-status', 'label'),
    Output('dark-pwb6-status', 'label'),
    Output('dark-pwb7-status', 'label'),
    Output('dark-pwb8-status', 'label'),
    Output('dark-pwc1-status', 'color'),
    Output('dark-pwc2-status', 'color'),
    Output('dark-pwc3-status', 'color'),
    Output('dark-pwc4-status', 'color'),
    Output('dark-pwc5-status', 'color'),
    Output('dark-pwc6-status', 'color'),
    Output('dark-pwc7-status', 'color'),
    Output('dark-pwc8-status', 'color'),
    Output('dark-pwc1-status', 'label'),
    Output('dark-pwc2-status', 'label'),
    Output('dark-pwc3-status', 'label'),
    Output('dark-pwc4-status', 'label'),
    Output('dark-pwc5-status', 'label'),
    Output('dark-pwc6-status', 'label'),
    Output('dark-pwc7-status', 'label'),
    Output('dark-pwc8-status', 'label'),
    Output('dark-kt1s-status', 'height'),
    Output('dark-kt2s-status', 'height'),
    Output('dark-kp1s-status', 'height'),
    Output('dark-kp2s-status', 'height'),
    Output('dark-kp3s-status', 'height'),
    Output('dark-kbgs-status', 'height'),
    Output('dark-kbvs-status', 'height'),
    Output('dark-kbds-status', 'height'),
    Output('dark-kfcs-status', 'height'),
    Output('dark-kbes-status', 'height'),
    Output('dark-kbms-status', 'height'),
    Output('dark-kros-status', 'height'),
    Output('dark-kcas-status', 'height'),
    Output('dark-kcwi-status', 'height'),
    Output('dark-pwa1-status', 'height'),
    Output('dark-pwa2-status', 'height'),
    Output('dark-pwa3-status', 'height'),
    Output('dark-pwa4-status', 'height'),
    Output('dark-pwa5-status', 'height'),
    Output('dark-pwa6-status', 'height'),
    Output('dark-pwa7-status', 'height'),
    Output('dark-pwa8-status', 'height'),
    Output('dark-pwb1-status', 'height'),
    Output('dark-pwb2-status', 'height'),
    Output('dark-pwb3-status', 'height'),
    Output('dark-pwb4-status', 'height'),
    Output('dark-pwb5-status', 'height'),
    Output('dark-pwb6-status', 'height'),
    Output('dark-pwb7-status', 'height'),
    Output('dark-pwb8-status', 'height'),
    Output('dark-pwc1-status', 'height'),
    Output('dark-pwc2-status', 'height'),
    Output('dark-pwc3-status', 'height'),
    Output('dark-pwc4-status', 'height'),
    Output('dark-pwc5-status', 'height'),
    Output('dark-pwc6-status', 'height'),
    Output('dark-pwc7-status', 'height'),
    Output('dark-pwc8-status', 'height'),
    Output('dark-tab2', 'disabled')],
    [Input('dark-polling-interval2', 'n_intervals')],
    state=[State('dark-tabs', 'children'),
    State('dark-annotations-storage2', 'data')]
)
def update(n_intervals, tab, current_annotations):
    with kcwi_semaphore3:
        print('power and server update started')
        newBinVal = kcwiKeywords.get_keywords()
        #print(newBinVal)
        stats = [newBinVal[keyword] for keyword in binary_keywords]
        #print(stats)
        color_list = []
        counter = 0
        for val in stats:
            if binary_keywords[counter][1:6] == 'RANGE':
                if val == '0':
                    color_list.append('red')
                elif val == '1':
                    color_list.append('yellow')
                else:
                    color_list.append('green')
            else:
                if val == '0':
                    color_list.append('red')
                elif val == '1':
                    color_list.append('green')
                else:
                    color_list.append(val)
            counter = counter + 1
        len_color_list = len(color_list)
        for x in range(len_color_list):
            if color_list[x] =='green':
                color_list.append(0)
            elif color_list[x] =='yellow':
                color_list.append(20)
            elif color_list[x] =='red':
                color_list.append(30)
        stats.append(False)
        print('power and server update done')
        return color_list
