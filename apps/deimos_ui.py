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
        'dark': False,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E'
    }

class_theme = {'dark' : ''}

#### Check Keywords Tab
check_keywords = Keywords()
serverUpQ = []
serverUpQ.append(['deimot','tvfilraw'])
serverUpQ.append(['deimot','g4tltraw'])
serverUpQ.append(['deimot','tmirrraw'])
serverUpQ.append(['deimot','hplogtim'])
serverUpQ.append(['deimot','slbarcfg'])
serverUpQ.append(['deimot','bargncfg'])
serverUpQ.append(['deiccd','tempdet,wcrate,observer'])
serverUpQ.append(['deifcs','wcrate,observer'])
serverUpQ.append(['deirot','rotatval'])
serverUpQ.append(['acs','mode'])
serverUpQ.append(['dcs','ra'])


##### Check Settings Tab
settings_keywords = Keywords()
tempset = float(settings_keywords.get_keyword('deiccd', 'tempset'))
rotccwlm = -330
rotcwlm = 402
settingsGoodQ = []
settingsGoodQ.append({ 'NAME' : 'CCD temp setpoint',
            'LIBRARY' : 'deiccd',
            'KEYWORD' : 'tempset',
            'MINVALUE' : -116,
            'MAXVALUE' : -114,
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'CCD temperature',
            'LIBRARY' : 'deiccd',
            'KEYWORD' : 'tempdet',
            'MINVALUE' : tempset-1,
            'MAXVALUE' : tempset+1,
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Coolant flow',
            'LIBRARY' : 'deirot',
            'KEYWORD' : 'coolflow',
            'GOODVALUE' : 'okay',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'TV coolant flow',
            'LIBRARY' : 'deimot',
            'KEYWORD' : 'tvcoflow',
            'GOODVALUE' : 'okay',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Air pressure (barrel)',
            'LIBRARY' : 'deimot',
            'KEYWORD' : 'airpress',
            'GOODVALUE' : 'okay',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Air pressure (cradle)',
            'LIBRARY' : 'deirot',
            'KEYWORD' : 'airpress',
            'GOODVALUE' : 'okay',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Dewar ion pump',
            'LIBRARY' : 'deimot',
            'KEYWORD' : 'ionpump1',
            'GOODVALUE' : 'on',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Vessel ion pump',
            'LIBRARY' : 'deimot',
            'KEYWORD' : 'ionpump2',
            'GOODVALUE' : 'on',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Science CCD 15V Power',
            'LIBRARY' : 'deiccd',
            'KEYWORD' : 'UTB15VEN',
            'GOODVALUE' : 'enabled',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'Science CCD 30V Power',
            'LIBRARY' : 'deiccd',
            'KEYWORD' : 'UTB30VEN',
            'GOODVALUE' : 'enabled',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'FCS CCD 15V Power',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'UTB15VEN',
            'GOODVALUE' : 'enabled',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'FCS CCD 30V Power',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'UTB30VEN',
            'GOODVALUE' : 'enabled',
            'BADSTATUS' : 'red'})
settingsGoodQ.append({ 'NAME' : 'FCS lamp',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'fcscusel',
            'GOODVALUE' : 'Cu1',
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'FCS focus tolerance 1',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'fcsfoto1',
            'MINVALUE' : 100,
            'MAXVALUE' : 1000,
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'FCS focus tolerance 2',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'fcsfoto2',
            'MINVALUE' : 100,
            'MAXVALUE' : 1000,
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Add frame (science)',
            'LIBRARY' : 'deiccd',
            'KEYWORD' : 'addframe',
            'GOODVALUE' : 'true',
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Add frame (FCS)',
            'LIBRARY' : 'deifcs',
            'KEYWORD' : 'addframe',
            'GOODVALUE' : 'true',
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Current instrument',
            'LIBRARY' : 'dcs',
            'KEYWORD' : 'currinst',
            'GOODVALUE' : 'DEIMOS',
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Rotator CCW limit',
            'LIBRARY' : 'dcs',
            'KEYWORD' : 'rotccwlm',
            'MINVALUE' : rotccwlm-1,
            'MAXVALUE' : rotccwlm+1,
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Rotator CW limit',
            'LIBRARY' : 'dcs',
            'KEYWORD' : 'rotcwlm',
            'MINVALUE' : rotcwlm-1,
            'MAXVALUE' : rotcwlm+1,
            'BADSTATUS' : 'yellow'})


rootLayout1 = html.Div([
    html.Div(id='deimos-summary-container', children=[
        html.Div(className='indicator-box', id='deimos-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='deimos-computer-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box', id='deimos-summary-container2', children=[
            html.H4('Daemons Check'),
            daq.Indicator(
                id='deimos-daemons-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='deimos-summary-container3', children=[
            html.H4('Keyword Librarys Check'),
            daq.Indicator(
                id='deimos-keyword-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='deimos-summary-container4', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='deimos-settings-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ])
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
                height = 0,
                id='legend-red',
                value=True,
                color='red',
                label='Off/Error ='
            ),
            daq.Indicator( width = 30,
                id='legend-blue',
                value=True,
                color='blue',
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box', id='welcome-link')
    ])
])

settingsRoot2 = html.Div([
    html.Div(id='deimos-settings-container', className='indicator-box', children=[
        html.H4('Settings Check'),
        html.Div(id='deimos-settings-1', children=[
            daq.Indicator(
                id='tempset-check',
                value=True,
                color='blue',
                label=settingsGoodQ[0]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='tempdet-check',
                value=True,
                color='blue',
                label=settingsGoodQ[1]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='coolflow-check',
                value=True,
                color='blue',
                label=settingsGoodQ[2]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='airpressBarrel-check',
                value=True,
                color='blue',
                label=settingsGoodQ[3]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='airpressCradle-check',
                value=True,
                color='blue',
                label=settingsGoodQ[4]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='ionpump1-check',
                value=True,
                color='blue',
                label=settingsGoodQ[5]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='deimos-settings-2', children=[
            daq.Indicator(
                id='UTB15VEN-check',
                value=True,
                color='blue',
                label=settingsGoodQ[6]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB30VEN-check',
                value=True,
                color='blue',
                label=settingsGoodQ[7]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB15VEN-fcs-check',
                value=True,
                color='blue',
                label=settingsGoodQ[8]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB30VEN-fcs-check',
                value=True,
                color='blue',
                label=settingsGoodQ[9]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='fcscusel-check',
                value=True,
                color='blue',
                label=settingsGoodQ[10]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='fcsfoto1-check',
                value=True,
                color='blue',
                label=settingsGoodQ[11]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='deimos-settings-3', children=[
            daq.Indicator(
                id='fcsfoto2-check',
                value=True,
                color='blue',
                label=settingsGoodQ[12]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='addframe-check',
                value=True,
                color='blue',
                label=settingsGoodQ[13]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='currinst-check',
                value=True,
                color='blue',
                label=settingsGoodQ[14]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='rotccwlm-check',
                value=True,
                color='blue',
                label=settingsGoodQ[15]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='rotcwlm-check',
                value=True,
                color='blue',
                label=settingsGoodQ[16]['NAME'],
                width = 30
            ),
        ])
    ])
])

keywordsRoot2 = html.Div([
    html.Div(id='deimos-keyword-container', className='indicator-box', children=[
        html.H4('Keyword Library Checks'),
        html.Div(id='deimos-keyword-container1', children=[
            daq.Indicator(
                id='tvfilraw-check',
                value=True,
                color='blue',
                label='Dispatcher 1',
                width = 30
            ),
            daq.Indicator(
                id='g4tltraw-check',
                value=True,
                color='blue',
                label='Dispatcher 2',
                width = 30
            ),
            daq.Indicator(
                id='tmirrraw-check',
                value=True,
                color='blue',
                label='Piezo',
                width = 30
            )
        ]),
        html.Div(id='deimos-keyword-container2', children=[
            daq.Indicator(
                id='hplogtim-check',
                value=True,
                color='blue',
                label='Hplogger',
                width = 30
            ),
            daq.Indicator(
                id='slbarcfg-check',
                value=True,
                color='blue',
                label='Barco',
                width = 30
            ),
            daq.Indicator(
                id='bargncfg-check',
                value=True,
                color='blue',
                label='Bargun',
                width = 30
            )
        ]),
        html.Div(id='deimos-keyword-container3', children=[
            daq.Indicator(
                id='two-check',
                value=True,
                color='blue',
                label='CCD+infopatcher',
                width = 30
            ),
            daq.Indicator(
                id='wo-check',
                value=True,
                color='blue',
                label='FCS+infopatcher',
                width = 30
            ),
            daq.Indicator(
                id='rotatval-check',
                value=True,
                color='blue',
                label='Rotator',
                width = 30
            )
        ]),
        html.Div(id='deimos-keyword-container4', children=[
            daq.Indicator(
                id='mode-check',
                value=True,
                color='blue',
                label='ACS',
                width = 30
            ),
            daq.Indicator(
                id='ra-check',
                value=True,
                color='blue',
                label='DCS',
                width = 30
            ),
        ])
    ])
])

powerRoot2 = html.Div([])
pressureRoot2 = html.Div([])

layout = [
    dcc.Tabs(id="deimos-tabs", value='deimos-tabs', children=[
        dcc.Tab(id='deimos-tab1', label='DEIMOS Summary', value='deimos-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', children=[
            html.Br(),
            daq.ToggleSwitch(
                id='deimos-daq-light-dark-theme',
                label=['Light', 'Dark'],
                style={'width': '250px', 'margin': 'auto'},
                value=False
            ),
            html.Br(),
            html.Div(id='deimos-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='deimos-polling-interval',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='deimos-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='deimos-tab2', label='DEIMOS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', children=[
            html.Div(id='deimos-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='deimos-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='deimos-subtab4', label='Settings Checks', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='deimos-subtab1', label='Keyword Library Checks', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=keywordsRoot2)),
                        dcc.Tab(id='deimos-subtab2', label='Power Servers', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='deimos-subtab3', label='Pressure Servers', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='deimos-polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='deimos-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='deimos-tabs-content')
]

@app.callback(
    [Output('deimos-keyword-check', 'color'),
    Output('deimos-keyword-check', 'label')],
    [Input('deimos-polling-interval', 'n_intervals')]
)
def global_checks(n_intervals):
    stats = []
    counter = 0
    for key in serverUpQ:
        if check_keywords.server_up(key[0],key[1]):
            counter += 1
    if counter == len(serverUpQ):
        stats.append('green')
        stats.append('Good')
    else:
        stats.append('red')
        stats.append('ERROR')
    return stats

@app.callback(
    [Output('tvfilraw-check', 'color'),
    Output('g4tltraw-check', 'color'),
    Output('tmirrraw-check', 'color'),
    Output('hplogtim-check', 'color'),
    Output('slbarcfg-check', 'color'),
    Output('bargncfg-check', 'color'),
    Output('two-check', 'color'),
    Output('wo-check', 'color'),
    Output('rotatval-check', 'color'),
    Output('mode-check', 'color'),
    Output('ra-check', 'color')
    ],
    [Input('deimos-polling-interval2', 'n_intervals')]
)
def keyword_library_check(n_intervals):
    stats = []
    for key in serverUpQ:
        if check_keywords.server_up(key[0],key[1]):
            stats.append('green')
        else:
            stats.append('red')
    return stats
