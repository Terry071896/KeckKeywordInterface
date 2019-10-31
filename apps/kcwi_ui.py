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

theme = {
        'dark': False,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : ''}

rootLayout1 = html.Div([
    html.Div(id='kcwi-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container1', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='kcwi-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container2', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='kcwi-settings-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='settings-container3', children=[
            html.H4('Power Check'),
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
            daq.StopButton(id='stop-button')
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
                id='legend-red',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='welcome-link')
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
    html.Div(className='indicator-box'+class_theme['dark'], id='graph-container1', children=[
        html.H4('Blue CCD Temperature'),
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
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp1-container', children=[
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
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp7-container', children=[
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
    html.Div(className='indicator-box'+class_theme['dark'], id='tmp8-container', children=[
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

powerOutlets = []
powerChildren = []
check_power = Keywords()
counter = 0
for i in ['A','B','C']:
    counter += 1
    powerChildren.append(html.H4('Power Bank %s' %(i)))
    for j in range(1,9):
        powerOutlets.append({'KEYWORD':'PWSTAT'+str(j)+i, 'LIBRARY':'kp%ss'%(counter), 'NAME':'PWNAME'+str(j)+i})
        powerChildren.append(daq.Indicator( width = 30,
            id='PWSTAT'+str(j)+i+'-status',
            value=True,
            color='blue',height=30,
            label='Port %s'%(str(j))
        ))


powerRoot2 = html.Div([
    html.Div(id='PWSTATA-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstata-status', children=powerChildren[:9]),
    ]),
    html.Div(id='PWSTATB-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstatb-status', children=powerChildren[9:18]),
    ]),
    html.Div(id='PWSTATC-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='pwstatc-status', children=powerChildren[18:])
    ]),
    dcc.ConfirmDialogProvider(
        children=html.Button(
            'Help',
            id='help-power-button'
        ),
        id='help-power-provider',
        message='FPCam: Okay if it is off to operate \n Magiq: Okay if it is off to operate'
    ),
    html.Div(id='output-provider')
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
    html.Div(className='indicator-box'+class_theme['dark'], id='graph-container', children=[
        html.H4(check_power.get_keyword('kbvs', 'prname')),
        dcc.Graph(
            id='pressure-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': pressure_layout if class_theme['dark'] == '' else pressure_layout_dark
            }),
        )
    ]),
    html.Div(id='legend-container1', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dropdown-container', children=[
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
    html.Div(className='indicator-box'+class_theme['dark'], id='pgpress-container', children=[
        html.H4('Blue Pressure Gauge'),
        # daq.Gauge(
        #     id='pgpress-status',
        #     logarithmic=True,
        #     min=-4, max=1,
        #     units="Torr",
        #     showCurrentValue=True,
        # ),
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
    html.Div(className='indicator-box'+class_theme['dark'], id='thePressure-container', children=[
        html.H4('Blue Vac Ion'),
        # daq.Gauge(
        #     id='thePressure-status',
        #     logarithmic=True,
        #     min=-8, max=-5,
        #     units="Torr",
        #     showCurrentValue=True,
        # ),
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

serverUpQ = []
check_servers = Keywords()

for library in allServers[:-1]:
    serverUpQ.append({'KEYWORD':'uptime', 'LIBRARY':library})
serverUpQ.append({'KEYWORD':'TESTINT', 'LIBRARY':'kcwi'})

settingsCheckQ = []
check_settings = Keywords()
settingsCheckQ.append({'NAME':'Blue CCD Temperature Check', 'KEYWORD':'tmp1', 'LIBRARY':'kt1s', 'MINVALUE':161, 'MAXVALUE':165, 'BADSTATUS':'red', 'NORMAL':163})
settingsCheckQ.append({'NAME':'CCD Power Check', 'KEYWORD':'ccdpower', 'LIBRARY':'kbds', 'GOODVALUE':1, 'BADSTATUS':'red'})
settingsCheckQ.append({'NAME':'Ion Pump Check', 'KEYWORD':'hvon', 'LIBRARY':'kbvs', 'GOODVALUE':1, 'BADSTATUS':'red'})

serverRoot2 = html.Div([
    html.Div(id='SERVER-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('All Servers'),
        html.Div(className='indicator-box'+class_theme['dark'], id='temperature-servers', children=[
            html.H4('Temperature'),
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
            html.H4("Power"),
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
            html.H4("Pressure"),
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
            html.H4("Detector"),
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
            html.H4("Mechanisms"),
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
            html.H4("Global"),
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
        html.H4('Settings Checks'),
        html.Div(id='settings-container1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='tmp1-check',
                value=True,
                color='blue',height=30,
                label='Blue CCD Temperature Check',
                width = 30
            )
        ]),
        html.Div(id='settings-container2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='ccdpower-check',
                value=True,
                color='blue',height=30,
                label='CCD Power Check',
                width = 30
            )
        ]),
        html.Div(id='settings-container3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='hvon-check',
                value=True,
                color='blue',height=30,
                label='Ion Pump Check',
                width = 30
            )
        ])
    ])
])



layout = [
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(id='tab1', label='KCWI Summary', value='tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Br(),
            html.Div(id='dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='polling-interval',
                n_intervals=0,
                interval=2*1000,
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

check_temperature_pressure = Keywords()

@app.callback(
    [Output('polling-interval', 'disabled'),
     Output('stop-button', 'buttonText')],
    [Input('stop-button', 'n_clicks')],
    state=[State('polling-interval', 'disabled')]
)
def stop_production(_, current):
    return not current, "stop" if current else "start"

# @app.callback(Output('output-provider', 'children'),
#               [Input('help-power-provider', 'submit_n_clicks')])
# def help_power_button(submit_n_clicks):
#     if not submit_n_clicks:
#         return ''
#     return """
#         It was dangerous but we did it!
#         Submitted {} times
#     """.format(submit_n_clicks)

kcwi_semaphore = threading.Semaphore()
@app.callback(
    [Output('temperature-graph', 'figure'),
    Output('pressure-graph', 'figure')],
    [Input('pressure-graph-dropdown', 'value'),
    Input('temperature-graph-dropdown', 'value')],
    state=[State('pressure-graph', 'figure'),
    State('temperature-graph', 'figure')]
)
def populate_temp_pressure_figs(valueP, valueT, current_figP, current_figT):
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


kcwi_semaphore1 = threading.Semaphore()
@app.callback(
    [#Output('pgpress-status', 'value'),
     Output('pgpress-status1', 'value'),
     #Output('thePressure-status', 'value'),
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
    with kcwi_semaphore1:
        stats=[]
        pgpress = float(check_temperature_pressure.get_keyword('kbgs', 'pgpress'))
        # stats.append(pgpress)
        stats.append(pgpress*10**4)
        pressure = float(check_temperature_pressure.get_keyword('kbvs', 'pressure'))
        # stats.append(pressure)
        stats.append(pressure*10**7)
        tmp1 = round(float(check_temperature_pressure.get_keyword('kt1s', 'tmp1')),3)
        tmp7 = round(float(check_temperature_pressure.get_keyword('kt2s', 'tmp7')),3)
        tmp8 = round(float(check_temperature_pressure.get_keyword('kt2s', 'tmp8')),3)

        for tmp in [tmp1, tmp7, tmp8]:
            stats.append(tmp)
            stats.append(str(tmp))
            stats.append(str(round(tmp-273,3)))
        return stats

outputs = [Output('tmp1-check', 'color'),
 Output('tmp1-check', 'height'),
 Output('ccdpower-check', 'color'),
 Output('ccdpower-check', 'height'),
 Output('hvon-check', 'color'),
 Output('hvon-check', 'height'),
 Output('kcwi-settings-check', 'color'),
 Output('kcwi-settings-check', 'label'),
 Output('kcwi-settings-check', 'height')]



for x in serverUpQ:
    outputs.append(Output('%s-status'%(x['LIBRARY']), 'color'))
    outputs.append(Output('%s-status'%(x['LIBRARY']), 'height'))

outputs.append(Output('kcwi-server-check', 'color'))
outputs.append(Output('kcwi-server-check', 'label'))
outputs.append(Output('kcwi-server-check', 'height'))

outputs.append(Output('tab1', 'disabled'))

kcwi_semaphore2 = threading.Semaphore()
@app.callback(
    outputs,
    [Input('polling-interval', 'n_intervals'),
    Input('polling-interval2', 'n_intervals')]
)
def populate_settings_servers(n_intervals1, n_intervals2):
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

        stats.append(False)
        print('ended kcwi settings and servers')
        return stats

outputs = []
for x in powerOutlets:
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'color'))
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'label'))
    outputs.append(Output('%s-status'%(x['KEYWORD']), 'height'))

outputs.append(Output('kcwi-power-check', 'color'))
outputs.append(Output('kcwi-power-check', 'label'))
outputs.append(Output('kcwi-power-check', 'height'))
outputs.append(Output('tab2', 'disabled'))
kcwi_semaphore3 = threading.Semaphore()
@app.callback(
    outputs,
    [Input('polling-interval', 'n_intervals'),
    Input('polling-interval2', 'n_intervals')]
)
def update(n_intervals1, n_intervals2):
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
            stats.append('Good (%s off)'%(okayOff))
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        stats.append(False)
        print('power and server update done')
        return stats
