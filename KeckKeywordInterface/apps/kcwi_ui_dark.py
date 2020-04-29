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
'kcwi'] # list of servers

theme = {
        'dark': True,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    } # overall theme of page, either 'dark' = False or 'dark' = True

class_theme = {'dark' : '-dark'} # the class theme, either '' or '-dark'


###################### First Tab Layout ######################
rootLayout1 = html.Div([
    html.Div(id='kcwi-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container1', children=[
            html.H4('Server Check'), # Indicator for all servers, green circle if all up, red box if one or more are down
            daq.Indicator(
                id='kcwi-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container2', children=[
            html.H4('Settings Check'), # Indicator for all settings, green circle if all up, red box if one or more are down
            daq.Indicator(
                id='kcwi-settings-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container3', children=[
            html.H4('Power Check'), # Indicator for all power, green circle if all up, red box if one or more are down
            daq.Indicator(
                id='kcwi-power-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
    ]),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='stop-button') # stop button to stop updating
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='legend-status', children=[
            html.H4("Legend"), # Legend indicators, so nothing changes
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
                id='legend-red',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='welcome-link') # link back to the welcome page
    ])
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
) # temperature graph layout for dark theme
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
) # temperature graph layout for light theme

####################### Second Tab Layouts #######################
##################################################################

####################### Temperature Tab #######################
temperatureRoot2 = html.Div(style={'overflow':'scroll'}, children=[
    html.Div(className='indicator-box'+class_theme['dark'], id='graph-container1', children=[
        html.H4('Blue CCD Temperature'), # temperature graph
        dcc.Graph(
            id='temperature-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': temperature_layout if class_theme['dark'] == '' else temperature_layout_dark
            }),
        )
    ]),
    html.Div(id='legend-container2', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dropdown-container1', children=[
            html.H4('Temperature History'), # drop down option for temperature history
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
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp1-container', children=[
        html.H4("Blue CCD Temperature"), # Temperautre Thermometer for Blue CCD
        daq.Thermometer(id='tmp1-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature as LED box in K for Blue CCD
            id='tmp1-k-temperature',
            value='000000',
            color='blue',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature in LED box in C for Blue CCD
            id='tmp1-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp7-container', children=[
        html.H4("Cab Interior Temperature"), # Temperature Thermometer for Cab Interior Temperature
        daq.Thermometer(id='tmp7-temp',
            min=270, max=320,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature as LED box in K for Cab Interior Temperature
            id='tmp7-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature as LED box in C for Cab Interior Temperature
            id='tmp7-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp8-container', children=[
        html.H4("Blue Fill Temperature"), # Temperature Thermometer for Blue Fill
        daq.Thermometer(id='tmp8-temp',
            min=0, max=273,
            value=100,
            color='blue'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature as LED box in K for Blue Fill
            id='tmp8-k-temperature',
            value='000000',
            label={'label': 'K', 'style': {'font-size': '24pt'}},
            color='blue',
            labelPosition='right'
        ),
        html.Br(),
        daq.LEDDisplay( # display temperature as LED box in C for Blue Fill
            id='tmp8-c-temperature',
            value='000000',
            label={'label': 'C', 'style': {'font-size': '24pt'}},
            color='red',
            labelPosition='right'
        )
    ])
])


########################### Power Tab ###########################
# Init keywords for all 3 power banks A, B, C
powerOutlets = [] # list of dictionaries holding keyword, library/server, and name/label
powerChildren = []  # the indicator list indexing with powerOutlets dictionaries
check_power = Keywords()
counter = 0
for i in ['A','B','C']: # loop over the 3 different power banks
    counter += 1
    powerChildren.append(html.H4('Power Bank %s' %(i)))
    for j in range(1,9): # loop over each power in bank
        powerOutlets.append({'KEYWORD':'PWSTAT'+str(j)+i, 'LIBRARY':'kp%ss'%(counter), 'NAME':'PWNAME'+str(j)+i})
        powerChildren.append(daq.Indicator( width = 30,
            id='PWSTAT'+str(j)+i+'-status',
            value=True,
            color='blue',height=30,
            label='Port %s'%(str(j))
        ))


powerRoot2 = html.Div([
    html.Div(id='PWSTATA-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstata-status', children=powerChildren[:9]), # Power Bank A, total of 9 keywords
    ]),
    html.Div(id='PWSTATB-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstatb-status', children=powerChildren[9:18]), # Power Bank B, total of 9 keywords
    ]),
    html.Div(id='PWSTATC-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstatc-status', children=powerChildren[18:]) # Power Bank C, total of 9 keywords
    ]),
    dcc.ConfirmDialogProvider( # help button and message
        children=html.Button(
            'Help',
            id='help-power-button'
        ),
        id='help-power-provider',
        message='FPCam: Okay to operate if off during day \n Magiq: Okay to operate if off during day'
    ),
    html.Div(id='output-provider')
])


###################### Pressure Tab #############################
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
) # pressure graph layout under a dark theme
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
) # pressure graph layout under a light theme

pressureRoot2 = html.Div([
    html.Div(className='indicator-box'+class_theme['dark'], id='graph-container', children=[
        html.H4(check_power.get_keyword('kbvs', 'prname')),
        dcc.Graph( # pressure graph
            id='pressure-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': pressure_layout if class_theme['dark'] == '' else pressure_layout_dark
            }),
        )
    ]),
    html.Div(id='legend-container1', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dropdown-container', children=[
            html.H4('Pressure History'), # drop down menu for history options
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
    html.Div(className='indicator-box'+class_theme['dark'], id='pgpress-container', children=[
        html.H4('Blue Pressure Gauge'), # pressure gauge for blue pressure
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
            dash_katex.DashKatex(expression='\\textrm{x } 10^{-4}') # scale
        ])
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='thePressure-container', children=[
        html.H4('Blue Vac Ion'), # pressure gauge for blue vac ion
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
            dash_katex.DashKatex(expression='\\textrm{x } 10^{-7}') # scale
        ])
    ])
])


####################### Servers and Settings Tab #####################
serverUpQ = [] # list of dictionaries containing the server keyword and library/servers
check_servers = Keywords()

for library in allServers[:-1]: # loop through all the servers (not including 'kcwi') to make sure keyword 'uptime' has a value and therefore is up.
    serverUpQ.append({'KEYWORD':'uptime', 'LIBRARY':library})
serverUpQ.append({'KEYWORD':'TESTINT', 'LIBRARY':'kcwi'}) # append 'kcwi' keyword to check to make sure server is up

settingsCheckQ = [] # list of dictionaries containing the settings name, keyword, library/server, and other checks for indicator
check_settings = Keywords()
settingsCheckQ.append({'NAME':'Blue CCD Temperature Check', 'KEYWORD':'tmp1', 'LIBRARY':'kt1s', 'MINVALUE':161, 'MAXVALUE':165, 'BADSTATUS':'red', 'NORMAL':163})
settingsCheckQ.append({'NAME':'CCD Power Check', 'KEYWORD':'ccdpower', 'LIBRARY':'kbds', 'GOODVALUE':1, 'BADSTATUS':'red'})
settingsCheckQ.append({'NAME':'Ion Pump Check', 'KEYWORD':'hvon', 'LIBRARY':'kbvs', 'GOODVALUE':1, 'BADSTATUS':'red'})

serverRoot2 = html.Div([
    html.Div(id='SERVER-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('All Servers'), # box of all the servers
        html.Div(className='indicator-box'+class_theme['dark'], id='temperature-servers', children=[
            html.H4('Temperature'), # indicators of temperature servers
            daq.Indicator( width = 30,
                id='kt1s-status',
                value=True,
                color='blue',height=30,
                label='kt1s'
            ),
            daq.Indicator( width = 30,
                id='kt2s-status',
                value=True,
                color='blue',height=30,
                label='kt2s'
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='power-servers', children=[
            html.H4("Power"), # indicators of the power servers
            daq.Indicator( width = 30,
                id='kp1s-status',
                value=True,
                color='blue',height=30,
                label='kp1s'
            ),
            daq.Indicator( width = 30,
                id='kp2s-status',
                value=True,
                color='blue',height=30,
                label='kp2s'
            ),
            daq.Indicator( width = 30,
                id='kp3s-status',
                value=True,
                color='blue',height=30,
                label='kp3s'
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='pressure-servers', children=[
            html.H4("Pressure"), # indicators of the pressure servers
            daq.Indicator( width = 30,
                id='kbgs-status',
                value=True,
                color='blue',height=30,
                label='kbgs'
            ),
            daq.Indicator( width = 30,
                id='kbvs-status',
                value=True,
                color='blue',height=30,
                label='kbvs'
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='detector-servers', children=[
            html.H4("Detector"), # indicators of the detector servers
            daq.Indicator( width = 30,
                id='kbds-status',
                value=True,
                color='blue',height=30,
                label='kbds'
            ),
            daq.Indicator( width = 30,
                id='kfcs-status',
                value=True,
                color='blue',height=30,
                label='kfcs'
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='mechanism-servers', children=[
            html.H4("Mechanisms"), # indicators of the machanism servers
            daq.Indicator( width = 30,
                id='kbes-status',
                value=True,
                color='blue',height=30,
                label='kbes'
            ),
            daq.Indicator( width = 30,
                id='kbms-status',
                value=True,
                color='blue',height=30,
                label='kbms'
            ),
            daq.Indicator( width = 30,
                id='kros-status',
                value=True,
                color='blue',height=30,
                label='kros'
            ),
            daq.Indicator( width = 30,
                id='kcas-status',
                value=True,
                color='blue',height=30,
                label='kcas'
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='global-servers', children=[
            html.H4("Global"), # indicator for global servers
            daq.Indicator( width = 30,
                id='kcwi-status',
                value=True,
                color='blue',height=30,
                label='kcwi'
            )
        ])
    ]),
    html.Br(),
    html.Div(className='indicator-box'+class_theme['dark'], id='settings-container', children=[
        html.H4('Settings Checks'), # settings box
        html.Div(id='settings-container1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator( # temperature settings indicator check for blue CCD
                id='tmp1-check',
                value=True,
                color='blue',height=30,
                label='Blue CCD Temperature Check',
                width = 30
            )
        ]),
        html.Div(id='settings-container2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator( # power settings indicator check for ccd power
                id='ccdpower-check',
                value=True,
                color='blue',height=30,
                label='CCD Power Check',
                width = 30
            )
        ]),
        html.Div(id='settings-container3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator( # machanism settings indicator check for ion pump
                id='hvon-check',
                value=True,
                color='blue',height=30,
                label='Ion Pump Check',
                width = 30
            )
        ])
    ])
])


################################### OVERALL LAYOUT #######################################
layout = [
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(id='tab1', label='KCWI Summary', value='tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Br(),
            html.Div(id='dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='polling-interval',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='tab2', label='KCWI Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Div(id='dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='subtabs', value='subtabs1', children=[
                        dcc.Tab(id='subtab4', label='Servers/Settings', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=serverRoot2)),
                        dcc.Tab(id='subtab1', label='Temperature Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='subtab2', label='Power Servers', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='subtab3', label='Pressure Servers', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='polling-interval2',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='tabs-content')
]

check_temperature_pressure = Keywords()

@app.callback(
    [Output('polling-interval', 'disabled'),
     Output('stop-button', 'buttonText')],
    [Input('stop-button', 'n_clicks')],
    state=[State('polling-interval', 'disabled')]
)
def stop_production(_, current):
    '''
    Stop button activation, once pressed the current state is swiched and label switches to 'stop' or 'start'

    Parameters
    ----------
    current : boolean
        the state of which the page is updating or not.

    Returns
    -------
    boolean
        the opposite state of the parameter state with the purpose to switch states
    str
        the label of the button, either 'stop' or 'start'
    '''
    return not current, "stop" if current else "start"


kcwi_semaphore = threading.Semaphore() # init semaphore for temperature and pressure graphs page
@app.callback(
    [Output('temperature-graph', 'figure'),
    Output('pressure-graph', 'figure')],
    [Input('pressure-graph-dropdown', 'value'),
    Input('temperature-graph-dropdown', 'value')],
    state=[State('pressure-graph', 'figure'),
    State('temperature-graph', 'figure')]
)
def populate_temp_pressure_figs(valueP, valueT, current_figP, current_figT):
    '''
    Temperature and Pressure figures activation, display history as graph by dropdown request

    Parameters
    ----------
    valueP : str
        the history requested of the pressure keyword 'pressure' from server 'kbvs'.  Ex. 'second', 'day', 'month', etc.
    valueT : str
        the history requested of the temperature keyword 'tmp1' from server 'kt1s'.  Ex. 'second', 'day', 'month', etc.
    current_figP : dcc.Graph
        the current graph display for the pressure history figure
    current_figT : dcc.Graph
        the current graph display for the temperature history figure

    Returns
    -------
    list
        list of the temperature and pressure figures.
    '''
    with kcwi_semaphore:
        bVw = list()
        current_data = current_figT['data'][0]
        new_data = [check_temperature_pressure.get_keyword_history('kt1s', 'tmp1', valueT)]
        current_figT['data'] = new_data
        bVw.append(current_figT)

        current_data = current_figP['data'][0]
        new_data = [check_temperature_pressure.get_keyword_history('kbvs', 'pressure', valueP)]
        current_figP['data'] = new_data
        bVw.append(current_figP)
        return bVw


kcwi_semaphore1 = threading.Semaphore() # init Semaphore for temperature thermometers and pressure gauges
@app.callback(
    [Output('pgpress-status1', 'value'),
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
def populate_temp_pressure(n_intervals2):
    '''
    Temperature and Pressure thermometers and gauges activation, update values.

    Parameters
    ----------
    n_intervals2 : int
        number of milliseconds passed since start updates for page 2.

    Returns
    -------
    list
        list of values in order expressed in Output callback list.
    '''
    with kcwi_semaphore1:
        stats=[]
        pgpress = float(check_temperature_pressure.get_keyword('kbgs', 'pgpress'))
        stats.append(pgpress*10**4)
        pressure = float(check_temperature_pressure.get_keyword('kbvs', 'pressure'))
        stats.append(pressure*10**7)
        tmp1 = round(float(check_temperature_pressure.get_keyword('kt1s', 'tmp1')),3)
        tmp7 = round(float(check_temperature_pressure.get_keyword('kt2s', 'tmp7')),3)
        tmp8 = round(float(check_temperature_pressure.get_keyword('kt2s', 'tmp8')),3)

        for tmp in [tmp1, tmp7, tmp8]:
            stats.append(tmp)
            stats.append(str(tmp))
            stats.append(str(round(tmp-273,3)))
        return stats



outputs = [Output('tmp1-check', 'color'), # settings indicator checks on page 2
 Output('tmp1-check', 'height'),
 Output('ccdpower-check', 'color'),
 Output('ccdpower-check', 'height'),
 Output('hvon-check', 'color'),
 Output('hvon-check', 'height'),
 Output('kcwi-settings-check', 'color'), # settings global check on page 1
 Output('kcwi-settings-check', 'label'),
 Output('kcwi-settings-check', 'height')] # init/create outputs list to populate the settings indicators

for x in serverUpQ: # loop through all servers dictionaries
    outputs.append(Output('%s-status'%(x['LIBRARY']), 'color'))
    outputs.append(Output('%s-status'%(x['LIBRARY']), 'height'))

outputs.append(Output('kcwi-server-check', 'color')) # add server global indicator check on page 1
outputs.append(Output('kcwi-server-check', 'label'))
outputs.append(Output('kcwi-server-check', 'height'))

kcwi_semaphore2 = threading.Semaphore() # init semaphore for settings and server indicator values
@app.callback(
    outputs,
    [Input('polling-interval', 'n_intervals'),
    Input('polling-interval2', 'n_intervals')]
)
def populate_settings_servers(n_intervals1, n_intervals2):
    '''
    Settings and Server indicator value checks, update values

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
    with kcwi_semaphore2:
        stats=[]
        counterGreen = 0
        counterYellow = 0
        print('started kcwi settings and servers')
        for keyword in settingsCheckQ:
            if sorted(keyword.keys())[1] == 'GOODVALUE':
                if check_settings.get_keyword(keyword['LIBRARY'], keyword['KEYWORD']) == keyword['GOODVALUE']:
                    stats.append('green')
                    stats.append(0)
                    counterGreen += 1
                else:
                    stats.append(keyword['BADSTATUS'])
                    if keyword['BADSTATUS'] == 'yellow':
                        counterYellow += 1
                        stats.append(20)
                    else:
                        stats.append(30)
            else:
                if keyword['MINVALUE'] <= float(check_settings.get_keyword(keyword['LIBRARY'], keyword['KEYWORD'])) <= keyword['MAXVALUE']:
                    stats.append('green')
                    stats.append(0)
                    counterGreen += 1
                else:
                    stats.append(keyword['BADSTATUS'])
                    if keyword['BADSTATUS'] == 'yellow':
                        counterYellow += 1
                        stats.append(20)
                    else:
                        stats.append(30)

        if counterGreen == len(settingsCheckQ):
            stats.append('green')
            stats.append('Good')
            stats.append(0)
        elif counterGreen + counterYellow == len(settingsCheckQ):
            stats.append('yellow')
            stats.append('WARNING')
            stats.append(40)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        counter = 0
        for x in serverUpQ:
            if check_servers.server_up(x['LIBRARY'], x['KEYWORD']):
                stats.append('green')
                stats.append(0)
                counter += 1
            else:
                stats.append('red')
                stats.append(30)

        if counter == len(serverUpQ):
            stats.append('green')
            stats.append('Good')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        print('ended kcwi settings and servers')
        return stats

outputs = [] # init outputs for power indicator checks
for x in powerOutlets: # loop through power keyword dictionaries
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'color'))
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'label'))
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'height'))

outputs.append(Output('kcwi-power-check', 'color')) # power global indicator check on page 1
outputs.append(Output('kcwi-power-check', 'label'))
outputs.append(Output('kcwi-power-check', 'height'))
outputs.append(Output('tab1', 'disabled')) # tab1 disabled state
outputs.append(Output('tab2', 'disabled')) # tab2 disabled state
kcwi_semaphore3 = threading.Semaphore() # init semaphore for power indicator updates
@app.callback(
    outputs,
    [Input('polling-interval', 'n_intervals'),
    Input('polling-interval2', 'n_intervals')]
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
    with kcwi_semaphore3:
        print('power update started')
        stats = []
        okayOff = ''
        counter = 0
        for x in powerOutlets:
            if check_power.get_keyword(x['LIBRARY'], x['KEYWORD'][:-1]) == '1':
                stats.append('green')
                stats.append(check_power.get_keyword(x['LIBRARY'],x['NAME'][:-1]))
                stats.append(0)
            else:
                name = check_power.get_keyword(x['LIBRARY'],x['NAME'][:-1])
                stats.append('red')
                stats.append(name)
                stats.append(30)
                if name == 'FPCam' or name == 'Magiq':
                    okayOff = okayOff + ' ' + name
                elif name != 'Unused':
                    counter += 1


        if counter == 0 and okayOff == '':
            stats.append('green')
            stats.append('Good')
            stats.append(0)
        elif counter == 0 and okayOff != '':
            stats.append('green')
            stats.append('Good (%s off)'%(okayOff[1:]))
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        stats.append(False)
        stats.append(False)
        print('power and server update done')
        return stats
