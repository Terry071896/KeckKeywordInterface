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
        'dark': False,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : ''}

rootLayout = html.Div([
        html.Div(id='SERVER-container', children=[
            html.Div(className='indicator-box', id='temperature-servers', children=[
                html.H4('Temperature'),
                daq.Indicator( width = 30,
                    id='kt1s-status',
                    value=True,
                    color='blue',
                    label='kt1s'
                ),
                daq.Indicator( width = 30,
                    id='kt2s-status',
                    value=True,
                    color='blue',
                    label='kt2s'
                )
            ]),
            html.Div(className='indicator-box', id='power-servers', children=[
                html.H4("Power"),
                daq.Indicator( width = 30,
                    id='kp1s-status',
                    value=True,
                    color='blue',
                    label='kp1s'
                ),
                daq.Indicator( width = 30,
                    id='kp2s-status',
                    value=True,
                    color='blue',
                    label='kp2s'
                ),
                daq.Indicator( width = 30,
                    id='kp3s-status',
                    value=True,
                    color='blue',
                    label='kp3s'
                )
            ]),
            html.Div(className='indicator-box', id='pressure-servers', children=[
                html.H4("Pressure"),
                daq.Indicator( width = 30,
                    id='kbgs-status',
                    value=True,
                    color='blue',
                    label='kbgs'
                ),
                daq.Indicator( width = 30,
                    id='kbvs-status',
                    value=True,
                    color='blue',
                    label='kbvs'
                )
            ]),
            html.Div(className='indicator-box', id='detector-servers', children=[
                html.H4("Detector"),
                daq.Indicator( width = 30,
                    id='kbds-status',
                    value=True,
                    color='blue',
                    label='kbds'
                ),
                daq.Indicator( width = 30,
                    id='kfcs-status',
                    value=True,
                    color='blue',
                    label='kfcs'
                )
            ]),
            html.Div(className='indicator-box', id='mechanism-servers', children=[
                html.H4("Mechanisms"),
                daq.Indicator( width = 30,
                    id='kbes-status',
                    value=True,
                    color='blue',
                    label='kbes'
                ),
                daq.Indicator( width = 30,
                    id='kbms-status',
                    value=True,
                    color='blue',
                    label='kbms'
                ),
                daq.Indicator( width = 30,
                    id='kros-status',
                    value=True,
                    color='blue',
                    label='kros'
                ),
                daq.Indicator( width = 30,
                    id='kcas-status',
                    value=True,
                    color='blue',
                    label='kcas'
                )
            ]),
            html.Div(className='indicator-box', id='global-servers', children=[
                html.H4("Global"),
                daq.Indicator( width = 30,
                    id='kcwi-status',
                    value=True,
                    color='blue',
                    label='kcwi'
                )
            ])
        ])
])

rootLayout1 = html.Div([
    html.Br(),
    html.Div(className='indicator-box', id='settings-container1', children=[
        html.H4('Blue CCD Temperature Check'),
        daq.Indicator(
            id='tmp1-check',
            value=True,
            color='blue',
            label='Loading...',
            width = 50
        ),
    ]),
    html.Div(className='indicator-box', id='settings-container2', children=[
        html.H4('CCD Power Check'),
        daq.Indicator(
            id='ccdpower-check',
            value=True,
            color='blue',
            label='Loading...',
            width = 50
        )
    ]),
    html.Div(className='indicator-box', id='settings-container3', children=[
        html.H4('Ion Pump Check'),
        daq.Indicator(
            id='hvon-check',
            value=True,
            color='blue',
            label='Loading...',
            width = 50
        )
    ]),
    html.Br(),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box', children=[
            daq.StopButton(id='stop-button')
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
                color='yellow',
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
                id='legend-red',
                value=True,
                color='blue',
                label='Loading ='
            )
        ])
    ]),
    html.Br(),
    dcc.Link('Go to Welcome Page', href='/', className='indicator-box', id='welcome-link')
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
    paper_bgcolor="#303030"
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
    html.Div(className='indicator-box', id='graph-container1', children=[
        html.H4('Blue CCD Temperature'),
        dcc.Graph(
            id='temperature-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': temperature_layout
            }),
        )
    ]),
    html.Div(id='legend-container2', children=[
        html.Div(className='indicator-box', id='dropdown-container1', children=[
            html.H4('Temperature History'),
            html.Div(className='dropdown-theme', id='dropdown1', children=[
                dcc.Dropdown(
                    id='temperature-graph-dropdown',
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
    html.Div(className='indicator-box', id='tmp1-container', children=[
        html.H4("Blue CCD Temperature"),
        daq.Thermometer(id='tmp1-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp1-k-temperature',
            value='000000',
            color='blue',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp1-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box', id='tmp7-container', children=[
        html.H4("Cab Interior Temperature"),
        daq.Thermometer(id='tmp7-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp7-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp7-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box', id='tmp8-container', children=[
        html.H4("Blue Fill Temperature"),
        daq.Thermometer(id='tmp8-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp8-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay(
            id='tmp8-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ])
])

powerRoot2 = html.Div([
    html.Div(id='PWSTATA-container', children=[
            html.Div(className='indicator-box', id='pwstata-status', children=[
                html.H4("Power Bank A"),
                daq.Indicator( width = 30,
                    id='pwa1-status',
                    value=True,
                    color='blue',
                    label='Port 1'
                ),
                daq.Indicator( width = 30,
                    id='pwa2-status',
                    value=True,
                    color='blue',
                    label='Port 2'
                ),
                daq.Indicator( width = 30,
                    id='pwa3-status',
                    value=True,
                    color='blue',
                    label='Port 3'
                ),
                daq.Indicator( width = 30,
                    id='pwa4-status',
                    value=True,
                    color='blue',
                    label='Port 4'
                ),
                daq.Indicator( width = 30,
                    id='pwa5-status',
                    value=True,
                    color='blue',
                    label='Port 5'
                ),
                daq.Indicator( width = 30,
                    id='pwa6-status',
                    value=True,
                    color='blue',
                    label='Port 6'
                ),
                daq.Indicator( width = 30,
                    id='pwa7-status',
                    value=True,
                    color='blue',
                    label='Port 7'
                ),
                daq.Indicator( width = 30,
                    id='pwa8-status',
                    value=True,
                    color='blue',
                    label='Port 8'
                )
            ])
        ]),
    html.Div(id='PWSTATB-container', children=[
        html.Div(className='indicator-box', id='pwstatb-status', children=[
            html.H4("Power Bank B"),
            daq.Indicator( width = 30,
                id='pwb1-status',
                value=True,
                color='blue',
                label='Port 1'
            ),
            daq.Indicator( width = 30,
                id='pwb2-status',
                value=True,
                color='blue',
                label='Port 2'
            ),
            daq.Indicator( width = 30,
                id='pwb3-status',
                value=True,
                color='blue',
                label='Port 3'
            ),
            daq.Indicator( width = 30,
                id='pwb4-status',
                value=True,
                color='blue',
                label='Port 4'
            ),
            daq.Indicator( width = 30,
                id='pwb5-status',
                value=True,
                color='blue',
                label='Port 5'
            ),
            daq.Indicator( width = 30,
                id='pwb6-status',
                value=True,
                color='blue',
                label='Port 6'
            ),
            daq.Indicator( width = 30,
                id='pwb7-status',
                value=True,
                color='blue',
                label='Port 7'
            ),
            daq.Indicator( width = 30,
                id='pwb8-status',
                value=True,
                color='blue',
                label='Port 8'
            )
        ])
    ]),
    html.Div(id='PWSTATC-container', children=[
        html.Div(className='indicator-box', id='pwstatc-status', children=[
            html.H4("Power Bank C"),
            daq.Indicator( width = 30,
                id='pwc1-status',
                value=True,
                color='blue',
                label='Port 1'
            ),
            daq.Indicator( width = 30,
                id='pwc2-status',
                value=True,
                color='blue',
                label='Port 2'
            ),
            daq.Indicator( width = 30,
                id='pwc3-status',
                value=True,
                color='blue',
                label='Port 3'
            ),
            daq.Indicator( width = 30,
                id='pwc4-status',
                value=True,
                color='blue',
                label='Port 4'
            ),
            daq.Indicator( width = 30,
                id='pwc5-status',
                value=True,
                color='blue',
                label='Port 5'
            ),
            daq.Indicator( width = 30,
                id='pwc6-status',
                value=True,
                color='blue',
                label='Port 6'
            ),
            daq.Indicator( width = 30,
                id='pwc7-status',
                value=True,
                color='blue',
                label='Port 7'
            ),
            daq.Indicator( width = 30,
                id='pwc8-status',
                value=True,
                color='blue',
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
    paper_bgcolor="#303030"
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
    html.Div(className='indicator-box', id='graph-container', children=[
        html.H4(kcwiKeywords.get_keyword('kbvs', 'prname')),
        dcc.Graph(
            id='pressure-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': pressure_layout
            }),
        )
    ]),
    html.Div(id='legend-container1', children=[
        html.Div(className='indicator-box', id='dropdown-container', children=[
            html.H4('Pressure History'),
            html.Div(className='dropdown-theme', id='dropdown', children=[
                dcc.Dropdown(
                    id='pressure-graph-dropdown',
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
    html.Div(className='indicator-box', id='pgpress-container', children=[
        html.H4('Blue Pressure Gauge'),
        daq.Gauge(
            id='pgpress-status',
            logarithmic=True,
            min=-4, max=1,
            units="Torr",
            showCurrentValue=True,
        ),
        html.Div([
            daq.Gauge(
                id='pgpress-status1',
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
    html.Div(className='indicator-box', id='thePressure-container', children=[
        html.H4('Blue Vac Ion'),
        daq.Gauge(
            id='thePressure-status',
            logarithmic=True,
            min=-8, max=-5,
            units="Torr",
            showCurrentValue=True,
        ),
        html.Div([
            daq.Gauge(
                id='thePressure-status1',
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
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(id='tab1', label='KCWI Settings', value='tabs1', className='custom-tab',
                selected_className='custom-tab--selected', children=[
            html.Br(),
            daq.ToggleSwitch(
                id='daq-light-dark-theme',
                label=['Light', 'Dark'],
                style={'width': '250px', 'margin': 'auto'},
                value=theme['dark']
            ),
            html.Br(),
            html.Div(id='dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='polling-interval',
                n_intervals=0,
                interval=1*1000,
                disabled=False
            ),
            dcc.Store(id='annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='tab2', label='KCWI Servers', value='tab2', className='custom-tab',
                selected_className='custom-tab--selected', children=[
            html.Div(id='dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='subtabs', value='subtabs1', children=[
                        dcc.Tab(id='subtab4', label='All Servers', value='subtab4', className='custom-tab',
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=serverRoot2)),
                        dcc.Tab(id='subtab1', label='Temperature Servers', value='subtab1',className='custom-tab',
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='subtab2', label='Power Servers', value='subtab2', className='custom-tab',
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='subtab3', label='Pressure Servers', value='subtab3', className='custom-tab',
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='tabs-content')
]



@app.callback(
    [Output('polling-interval', 'disabled'),
     Output('stop-button', 'buttonText')],
    [Input('stop-button', 'n_clicks')],
    state=[State('polling-interval', 'disabled')]
)
def stop_production(_, current):
    return not current, "stop" if current else "start"

@app.callback(
    [Output('dark-theme-component-demo', 'children'),
     Output('subtab4', 'children'),
     Output('subtab1', 'children'),
     Output('subtab2', 'children'),
     Output('subtab3', 'children')],
    [Input('daq-light-dark-theme', 'value')],
    state=[State('full-page', 'children')]
)
def turn_dark(dark_theme, current_children):
    if(dark_theme):
        theme.update(
            dark=True
        )
    else:
        theme.update(
            dark=False
        )
    return [daq.DarkThemeProvider(theme=theme, children=rootLayout1),
        daq.DarkThemeProvider(theme=theme, children=serverRoot2),
        daq.DarkThemeProvider(theme=theme, children=temperatureRoot2),
        daq.DarkThemeProvider(theme=theme, children=powerRoot2),
        daq.DarkThemeProvider(theme=theme, children=pressureRoot2)]

@app.callback(
    [Output('tab1', 'className'),
     Output('tab1', 'selected_className'),
     Output('tab2', 'className'),
     Output('tab2', 'selected_className'),
     Output('subtab1', 'className'),
     Output('subtab1', 'selected_className'),
     Output('subtab2', 'className'),
     Output('subtab2', 'selected_className'),
     Output('subtab3', 'className'),
     Output('subtab3', 'selected_className'),
     Output('subtab4', 'className'),
     Output('subtab4', 'selected_className'),
     Output('subtab5', 'className'),
     Output('subtab5', 'selected_className')],
    [Input('daq-light-dark-theme', 'value')]
)
def change_class_name_tab(dark_theme):
    bVw = list()
    temp = ''
    if(dark_theme):
        temp = '-dark'
    for x in range(0,7):
        bVw.append('custom-tab'+temp)
        bVw.append('custom-tab--selected'+temp)

    return bVw

@app.callback(
    [Output('graph-container', 'className'),
    Output('graph-container1', 'className'),
    Output('pgpress-container', 'className'),
    Output('thePressure-container', 'className'),
    Output('time-container', 'className'),
    Output('substance-container', 'className'),
    Output('welcome-link', 'className'),
    Output('tmp1-container', 'className'),
    Output('tmp7-container', 'className'),
    Output('tmp8-container', 'className'),
    Output('legend-status', 'className'),
    Output('settings-container1', 'className'),
    Output('settings-container2', 'className'),
    Output('settings-container3', 'className'),
    Output('pwstata-status', 'className'),
    Output('pwstatb-status', 'className'),
    Output('pwstatc-status', 'className'),
    Output('temperature-servers', 'className'),
    Output('power-servers', 'className'),
    Output('pressure-servers', 'className'),
    Output('detector-servers', 'className'),
    Output('mechanism-servers', 'className'),
    Output('global-servers', 'className'),
    Output('dropdown-container', 'className'),
    Output('dropdown-container1', 'className'),
    Output('dropdown1', 'className'),
    Output('dropdown', 'className'),
    Output('temperature-graph', 'figure'),
    Output('pressure-graph', 'figure')],
    [Input('daq-light-dark-theme', 'value'),
    Input('pressure-graph-dropdown', 'value'),
    Input('temperature-graph-dropdown', 'value')],
    state=[State('pressure-graph', 'figure'),
    State('temperature-graph', 'figure')]
)
def change_class_name(dark_theme, valueP, valueT, current_figP, current_figT):
    bVw = list()
    temp = ''
    current_figT['layout'] = temperature_layout
    current_figP['layout'] = pressure_layout
    if(dark_theme):
        temp = '-dark'
        current_figT['layout'] = temperature_layout_dark
        current_figP['layout'] = pressure_layout_dark
    for x in range(0,25):
        bVw.append('indicator-box'+temp)
    bVw.append('dropdown-theme'+temp)
    bVw.append('dropdown-theme'+temp)

    current_data = current_figT['data'][0]
    new_data = [histKeys.get_keyword_history('kt1s', 'tmp1', valueT)]
    current_figT['data'] = new_data
    bVw.append(current_figT)

    current_data = current_figP['data'][0]
    new_data = [histKeys.get_keyword_history('kbvs', 'pressure', valueP)]
    current_figP['data'] = new_data
    bVw.append(current_figP)
    return bVw



@app.callback(
    [Output('page-content', 'style')],
    [Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return [{'backgroundColor': '#303030', 'color': 'white'}]
    else:
        return [{'background-color': 'white', 'color': 'black'}]

@app.callback(
    [Output('pgpress-status', 'value'),
     Output('pgpress-status1', 'value'),
     Output('thePressure-status', 'value'),
     Output('thePressure-status1', 'value'),
     Output('tmp1-temp', 'value'),
     Output('tmp1-k-temperature', 'value'),
     Output('tmp1-c-temperature', 'value'),
     Output('tmp7-temp', 'value'),
     Output('tmp7-k-temperature', 'value'),
     Output('tmp7-c-temperature', 'value'),
     Output('tmp8-temp', 'value'),
     Output('tmp8-k-temperature', 'value'),
     Output('tmp8-c-temperature', 'value')],
     [Input('polling-interval2', 'n_intervals')]
)
def update_stats2(n_intervals):
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
    return stats


@app.callback(
    [Output('tmp1-check', 'color'),
     Output('tmp1-check', 'label'),
     Output('tmp1-check', 'height'),
     Output('ccdpower-check', 'color'),
     Output('ccdpower-check', 'label'),
     Output('ccdpower-check', 'height'),
     Output('hvon-check', 'color'),
     Output('hvon-check', 'label'),
     Output('hvon-check', 'height')],
    [Input('polling-interval', 'n_intervals')]
)
def update_stats1(n_intervals):
    stats=[]
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
    return stats


@app.callback(
    [Output('kt1s-status', 'color'),
    Output('kt2s-status', 'color'),
    Output('kp1s-status', 'color'),
    Output('kp2s-status', 'color'),
    Output('kp3s-status', 'color'),
    Output('kbgs-status', 'color'),
    Output('kbvs-status', 'color'),
    Output('kbds-status', 'color'),
    Output('kfcs-status', 'color'),
    Output('kbes-status', 'color'),
    Output('kbms-status', 'color'),
    Output('kros-status', 'color'),
    Output('kcas-status', 'color'),
    Output('kcwi-status', 'color'),
    Output('pwa1-status', 'color'),
    Output('pwa2-status', 'color'),
    Output('pwa3-status', 'color'),
    Output('pwa4-status', 'color'),
    Output('pwa5-status', 'color'),
    Output('pwa6-status', 'color'),
    Output('pwa7-status', 'color'),
    Output('pwa8-status', 'color'),
    Output('pwa1-status', 'label'),
    Output('pwa2-status', 'label'),
    Output('pwa3-status', 'label'),
    Output('pwa4-status', 'label'),
    Output('pwa5-status', 'label'),
    Output('pwa6-status', 'label'),
    Output('pwa7-status', 'label'),
    Output('pwa8-status', 'label'),
    Output('pwb1-status', 'color'),
    Output('pwb2-status', 'color'),
    Output('pwb3-status', 'color'),
    Output('pwb4-status', 'color'),
    Output('pwb5-status', 'color'),
    Output('pwb6-status', 'color'),
    Output('pwb7-status', 'color'),
    Output('pwb8-status', 'color'),
    Output('pwb1-status', 'label'),
    Output('pwb2-status', 'label'),
    Output('pwb3-status', 'label'),
    Output('pwb4-status', 'label'),
    Output('pwb5-status', 'label'),
    Output('pwb6-status', 'label'),
    Output('pwb7-status', 'label'),
    Output('pwb8-status', 'label'),
    Output('pwc1-status', 'color'),
    Output('pwc2-status', 'color'),
    Output('pwc3-status', 'color'),
    Output('pwc4-status', 'color'),
    Output('pwc5-status', 'color'),
    Output('pwc6-status', 'color'),
    Output('pwc7-status', 'color'),
    Output('pwc8-status', 'color'),
    Output('pwc1-status', 'label'),
    Output('pwc2-status', 'label'),
    Output('pwc3-status', 'label'),
    Output('pwc4-status', 'label'),
    Output('pwc5-status', 'label'),
    Output('pwc6-status', 'label'),
    Output('pwc7-status', 'label'),
    Output('pwc8-status', 'label'),
    Output('kt1s-status', 'height'),
    Output('kt2s-status', 'height'),
    Output('kp1s-status', 'height'),
    Output('kp2s-status', 'height'),
    Output('kp3s-status', 'height'),
    Output('kbgs-status', 'height'),
    Output('kbvs-status', 'height'),
    Output('kbds-status', 'height'),
    Output('kfcs-status', 'height'),
    Output('kbes-status', 'height'),
    Output('kbms-status', 'height'),
    Output('kros-status', 'height'),
    Output('kcas-status', 'height'),
    Output('kcwi-status', 'height'),
    Output('pwa1-status', 'height'),
    Output('pwa2-status', 'height'),
    Output('pwa3-status', 'height'),
    Output('pwa4-status', 'height'),
    Output('pwa5-status', 'height'),
    Output('pwa6-status', 'height'),
    Output('pwa7-status', 'height'),
    Output('pwa8-status', 'height'),
    Output('pwb1-status', 'height'),
    Output('pwb2-status', 'height'),
    Output('pwb3-status', 'height'),
    Output('pwb4-status', 'height'),
    Output('pwb5-status', 'height'),
    Output('pwb6-status', 'height'),
    Output('pwb7-status', 'height'),
    Output('pwb8-status', 'height'),
    Output('pwc1-status', 'height'),
    Output('pwc2-status', 'height'),
    Output('pwc3-status', 'height'),
    Output('pwc4-status', 'height'),
    Output('pwc5-status', 'height'),
    Output('pwc6-status', 'height'),
    Output('pwc7-status', 'height'),
    Output('pwc8-status', 'height')],
    [Input('polling-interval2', 'n_intervals')],
    state=[State('tabs', 'children'),
    State('annotations-storage2', 'data')]
)
def update(n_intervals, tab, current_annotations):
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
        if color_list[x] =='green' or color_list[x] =='yellow':
            color_list.append(0)
        elif color_list[x] =='red':
            color_list.append(30)
    print('power and server update done')
    return color_list
