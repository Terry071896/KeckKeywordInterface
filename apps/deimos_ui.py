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
globalValueT = ''
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
#serverUpQ.append(['dcs2','ra'])
serverUpQ.append(['dcs2','ra'])

histKeys = Keywords()
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
            'LIBRARY' : 'dcs2',
            'KEYWORD' : 'currinst',
            'GOODVALUE' : 'DEIMOS',
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Rotator CCW limit',
            'LIBRARY' : 'dcs2',
            'KEYWORD' : 'rotccwlm',
            'MINVALUE' : rotccwlm-1,
            'MAXVALUE' : rotccwlm+1,
            'BADSTATUS' : 'yellow'})
settingsGoodQ.append({ 'NAME' : 'Rotator CW limit',
            'LIBRARY' : 'dcs2',
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
            daq.StopButton(id='deimos-stop-button')
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
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box', id='deimos-welcome-link')
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
                id='tvcoflow-check',
                value=True,
                color='blue',
                label=settingsGoodQ[3]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='airpressBarrel-check',
                value=True,
                color='blue',
                label=settingsGoodQ[4]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='airpressCradle-check',
                value=True,
                color='blue',
                label=settingsGoodQ[5]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='ionpump1-check',
                value=True,
                color='blue',
                label=settingsGoodQ[6]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='deimos-settings-2', children=[
            daq.Indicator(
                id='ionpump2-check',
                value=True,
                color='blue',
                label=settingsGoodQ[7]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB15VEN-check',
                value=True,
                color='blue',
                label=settingsGoodQ[8]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB30VEN-check',
                value=True,
                color='blue',
                label=settingsGoodQ[9]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB15VEN-fcs-check',
                value=True,
                color='blue',
                label=settingsGoodQ[10]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='UTB30VEN-fcs-check',
                value=True,
                color='blue',
                label=settingsGoodQ[11]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='fcscusel-check',
                value=True,
                color='blue',
                label=settingsGoodQ[12]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='fcsfoto1-check',
                value=True,
                color='blue',
                label=settingsGoodQ[13]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='deimos-settings-3', children=[
            daq.Indicator(
                id='fcsfoto2-check',
                value=True,
                color='blue',
                label=settingsGoodQ[14]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='addframeScience-check',
                value=True,
                color='blue',
                label=settingsGoodQ[15]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='addframeFCS-check',
                value=True,
                color='blue',
                label=settingsGoodQ[16]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='currinst-check',
                value=True,
                color='blue',
                label=settingsGoodQ[17]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='rotccwlm-check',
                value=True,
                color='blue',
                label=settingsGoodQ[18]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='rotcwlm-check',
                value=True,
                color='blue',
                label=settingsGoodQ[19]['NAME'],
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

temperature_layout_dark = go.Layout(
    yaxis=dict(
        title='Temperature (C)',
        range=[-130, -90],
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    xaxis=dict(
        title='Date (UTC)',
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    height=505,
    plot_bgcolor="#313336",
    paper_bgcolor="#303030"
)
temperature_layout = go.Layout(
    yaxis=dict(
        title='Temperature (C)',
        range=[-130, -90]
    ),
    xaxis=dict(
        title='Date (UTC)'
    ),
    height=505,
    plot_bgcolor="#f3f3f3"
)

dataT = {'day' : '', 'week' : '', 'month' : ''}

temperatureRoot2 = html.Div([
    html.Div(className='indicator-box', id='deimos-graph-container1', children=[
        html.H4('Science Detector Temperature'),
        dcc.Graph(
            id='deimos-temperature-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': temperature_layout
            }),
        )
    ]),
    html.Div(id='legend-container2', children=[
        html.Div(className='indicator-box', id='deimos-dropdown-container1', children=[
            html.H4('Temperature History'),
            html.Div(className='dropdown-theme', id='deimos-dropdown1', children=[
                dcc.Dropdown(
                    id='deimos-temperature-graph-dropdown',
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
])
pressureRoot2 = html.Div([])

layout = [
    dcc.Tabs(id="deimos-tabs", value='deimos-tabs', children=[
        dcc.Tab(id='deimos-tab1', label='DEIMOS Summary', value='deimos-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
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
                interval=10*1000,
                disabled=False
            ),
            dcc.Store(id='deimos-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='deimos-tab2', label='DEIMOS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
            html.Div(id='deimos-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='deimos-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='deimos-subtab4', label='Settings Checks', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='deimos-subtab1', label='Keyword Library Checks', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=keywordsRoot2)),
                        dcc.Tab(id='deimos-subtab2', label='Temperatures', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='deimos-subtab3', label='[Maybe More...]', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='deimos-polling-interval2',
                n_intervals=0,
                interval=10*1000,
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
    [Output('deimos-polling-interval', 'disabled'),
    Output('deimos-polling-interval2', 'disabled'),
     Output('deimos-stop-button', 'buttonText')],
    [Input('deimos-stop-button', 'n_clicks')],
    state=[State('deimos-polling-interval', 'disabled'),
    State('deimos-polling-interval2', 'disabled')]
)
def stop_production(_, current, current2):
    return not current, not current2, "stop" if current else "start"




@app.callback(
    [Output('tvfilraw-check', 'color'),
    Output('tvfilraw-check', 'height'),
    Output('g4tltraw-check', 'color'),
    Output('g4tltraw-check', 'height'),
    Output('tmirrraw-check', 'color'),
    Output('tmirrraw-check', 'height'),
    Output('hplogtim-check', 'color'),
    Output('hplogtim-check', 'height'),
    Output('slbarcfg-check', 'color'),
    Output('slbarcfg-check', 'height'),
    Output('bargncfg-check', 'color'),
    Output('bargncfg-check', 'height'),
    Output('two-check', 'color'),
    Output('two-check', 'height'),
    Output('wo-check', 'color'),
    Output('wo-check', 'height'),
    Output('rotatval-check', 'color'),
    Output('rotatval-check', 'height'),
    Output('mode-check', 'color'),
    Output('mode-check', 'height'),
    Output('ra-check', 'color'),
    Output('ra-check', 'height'),
    Output('deimos-keyword-check', 'color'),
    Output('deimos-keyword-check', 'label'),
    Output('deimos-keyword-check', 'height')
    ],
    [Input('deimos-polling-interval2', 'n_intervals'),
    Input('deimos-polling-interval', 'n_intervals')]
)
def keyword_library_check(n_intervals2, n_intervals1):
    stats = []
    counter = 0
    for key in serverUpQ:
        if check_keywords.server_up(key[0],key[1]):
            counter += 1
            stats.append('green')
            stats.append(0)
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
    return stats

@app.callback(
    [Output('tempset-check', 'color'),
    Output('tempdet-check', 'color'),
    Output('coolflow-check', 'color'),
    Output('tvcoflow-check', 'color'),
    Output('airpressBarrel-check', 'color'),
    Output('airpressCradle-check', 'color'),
    Output('ionpump1-check', 'color'),
    Output('ionpump2-check', 'color'),
    Output('UTB15VEN-check', 'color'),
    Output('UTB30VEN-check', 'color'),
    Output('UTB15VEN-fcs-check', 'color'),
    Output('UTB30VEN-fcs-check', 'color'),
    Output('fcscusel-check', 'color'),
    Output('fcsfoto1-check', 'color'),
    Output('fcsfoto2-check', 'color'),
    Output('addframeScience-check', 'color'),
    Output('addframeFCS-check', 'color'),
    Output('currinst-check', 'color'),
    Output('rotccwlm-check', 'color'),
    Output('rotcwlm-check', 'color'),
    Output('tempset-check', 'height'),
    Output('tempdet-check', 'height'),
    Output('coolflow-check', 'height'),
    Output('tvcoflow-check', 'height'),
    Output('airpressBarrel-check', 'height'),
    Output('airpressCradle-check', 'height'),
    Output('ionpump1-check', 'height'),
    Output('ionpump2-check', 'height'),
    Output('UTB15VEN-check', 'height'),
    Output('UTB30VEN-check', 'height'),
    Output('UTB15VEN-fcs-check', 'height'),
    Output('UTB30VEN-fcs-check', 'height'),
    Output('fcscusel-check', 'height'),
    Output('fcsfoto1-check', 'height'),
    Output('fcsfoto2-check', 'height'),
    Output('addframeScience-check', 'height'),
    Output('addframeFCS-check', 'height'),
    Output('currinst-check', 'height'),
    Output('rotccwlm-check', 'height'),
    Output('rotcwlm-check', 'height'),
    Output('deimos-settings-check', 'color'),
    Output('deimos-settings-check', 'label'),
    Output('deimos-settings-check', 'height'),
    Output('deimos-tab1', 'disabled'),
    Output('deimos-tab2', 'disabled')],
    [Input('deimos-polling-interval2', 'n_intervals'),
    Input('deimos-polling-interval', 'n_intervals')]
)
def settings_check(n_intervals2, n_intervals1):
    stats = []
    counterGreen = 0
    counterYellow = 0
    print('settings_check started')
    for keyword in settingsGoodQ:
        if sorted(keyword.keys())[1] == 'GOODVALUE':
            if settings_keywords.get_keyword(keyword['LIBRARY'], keyword['KEYWORD']) == keyword['GOODVALUE']:
                stats.append('green')
                counterGreen += 1
            else:
                stats.append(keyword['BADSTATUS'])
                if keyword['BADSTATUS'] == 'yellow':
                    counterYellow += 1
        else:
            if keyword['MINVALUE'] <= float(settings_keywords.get_keyword(keyword['LIBRARY'], keyword['KEYWORD'])) <= keyword['MAXVALUE']:
                stats.append('green')
                counterGreen += 1
            else:
                stats.append(keyword['BADSTATUS'])
                if keyword['BADSTATUS'] == 'yellow':
                    counterYellow += 1
    len_stats = len(stats)
    for x in range(len_stats):
        if stats[x] == 'green' or stats[x] == 'yellow':
            stats.append(0)
        else:
            stats.append(30)
            #print(30)

    if counterGreen == len(settingsGoodQ):
        stats.append('green')
        stats.append('Good')
        stats.append(0)
    elif counterGreen + counterYellow == len(settingsGoodQ):
        stats.append('yellow')
        stats.append('WARNING')
        stats.append(0)
    else:
        stats.append('red')
        stats.append('ERROR')
        stats.append(50)

    stats.append(False)
    stats.append(False)
    print('settings_check done')
    return stats


@app.callback(
    [Output('deimos-temperature-graph', 'figure')],
    [Input('deimos-temperature-graph-dropdown', 'value'),
    Input('deimos-polling-interval2', 'n_intervals'),
    Input('deimos-polling-interval2', 'interval')],
    state=[State('deimos-temperature-graph', 'figure')]
)
def populate_temp_graph(valueT, n_intervals, interval, current_figT):
    stats = []
    current_data = current_figT['data']
    global dataT
    if valueT == 'fake':
        current_figT['data'] = [{'x' : [], 'y' : []}]
        stats.append(current_figT)
        return stats
    elif dataT[valueT] == '':
        new_data = [histKeys.get_keyword_history('deiccd', 'tempdet1', valueT, 'CCD1 temp (C)')]
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet2', valueT, 'CCD2 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet3', valueT, 'CCD3 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet4', valueT, 'CCD4 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet5', valueT, 'CCD5 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet6', valueT, 'CCD6 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet7', valueT, 'CCD7 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet8', valueT, 'CCD8 temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet', valueT, 'Detector average temp (C)'))
        new_data.append(histKeys.get_keyword_history('deiccd', 'tempset', valueT, 'Detector set temp (-114.958 C)'))
        dataT[valueT] = new_data
    else:
        n =60/(interval/1000)
        if n_intervals % n == 0:
            new_data = [histKeys.get_keyword_history('deiccd', 'tempdet1', 'second', 'CCD1 temp (C)')]
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet2', 'second', 'CCD2 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet3', 'second', 'CCD3 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet4', 'second', 'CCD4 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet5', 'second', 'CCD5 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet6', 'second', 'CCD6 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet7', 'second', 'CCD7 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet8', 'second', 'CCD8 temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet', 'second', 'Detector average temp (C)'))
            new_data.append(histKeys.get_keyword_history('deiccd', 'tempset', 'second', 'Detector set temp (-114.958 C)'))
            for key in dataT.keys():
                if dataT[key] != '':
                    for i in range(len(new_data)):
                        dataT[key][i]['x'].append(new_data[i]['x'][0])
                        dataT[key][i]['y'].append(new_data[i]['y'][0])
                        dataT[key][i] = {'x' : dataT[key][i]['x'],
                        'y' : dataT[key][i]['y'],
                        'name' : dataT[key][i]['name']}
                else:
                    new_data = [histKeys.get_keyword_history('deiccd', 'tempdet1', key, 'CCD1 temp (C)')]
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet2', key, 'CCD2 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet3', key, 'CCD3 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet4', key, 'CCD4 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet5', key, 'CCD5 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet6', key, 'CCD6 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet7', key, 'CCD7 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet8', key, 'CCD8 temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempdet', key, 'Detector average temp (C)'))
                    new_data.append(histKeys.get_keyword_history('deiccd', 'tempset', key, 'Detector set temp (-114.958 C)'))
                    dataT[key] = new_data


    current_figT['data'] = dataT[valueT]
    stats.append(current_figT)
    return stats


# @app.callback(
#     [Output('deimos-keyword-check', 'color'),
#     Output('deimos-keyword-check', 'label'),
#     Output('deimos-settings-check', 'color'),
#     Output('deimos-settings-check', 'label')],
#     [Input('deimos-polling-interval', 'n_intervals')]
# )
# def global_checks(n_intervals):
#     stats = []
#     counter = 0
#     for key in serverUpQ:
#         if check_keywords.server_up(key[0],key[1]):
#             counter += 1
#     if counter == len(serverUpQ):
#         stats.append('green')
#         stats.append('Good')
#     else:
#         stats.append('red')
#         stats.append('ERROR')
#
#     counterGreen = 0
#     counterYellow = 0
#     for keyword in settingsGoodQ:
#         if sorted(keyword.keys())[1] == 'GOODVALUE':
#             if settings_keywords.get_keyword(keyword['LIBRARY'], keyword['KEYWORD']) == keyword['GOODVALUE']:
#                 counterGreen += 1
#             else:
#                 if keyword['BADSTATUS'] == 'yellow':
#                     counterYellow += 1
#         else:
#             if keyword['MINVALUE'] <= float(settings_keywords.get_keyword(keyword['LIBRARY'], keyword['KEYWORD'])) <= keyword['MAXVALUE']:
#                 counterGreen += 1
#             else:
#                 if keyword['BADSTATUS'] == 'yellow':
#                     counterYellow += 1
#     if counterGreen == len(settingsGoodQ):
#         stats.append('green')
#         stats.append('Good')
#     elif counterGreen + counterYellow == len(settingsGoodQ):
#         stats.append('yellow')
#         stats.append('WARNING')
#     else:
#         stats.append('red')
#         stats.append('ERROR')
#     return stats

# @app.callback(
#     [Output('deimos-dark-theme-component-demo', 'children'),
#      Output('deimos-subtab4', 'children'),
#      Output('deimos-subtab1', 'children'),
#      Output('deimos-subtab2', 'children'),
#      Output('deimos-subtab3', 'children')],
#     [Input('deimos-daq-light-dark-theme', 'value')],
#     state=[State('full-page', 'children')]
# )
# def turn_dark(dark_theme, current_children):
#     if(dark_theme):
#         theme.update(
#             dark=True
#         )
#     else:
#         theme.update(
#             dark=False
#         )
#     return [daq.DarkThemeProvider(theme=theme, children=rootLayout1),
#         daq.DarkThemeProvider(theme=theme, children=settingsRoot2),
#         daq.DarkThemeProvider(theme=theme, children=keywordsRoot2),
#         daq.DarkThemeProvider(theme=theme, children=temperatureRoot2),
#         daq.DarkThemeProvider(theme=theme, children=pressureRoot2)]
#
# @app.callback(
#     [Output('deimos-tab1', 'className'),
#      Output('deimos-tab1', 'selected_className'),
#      Output('deimos-tab2', 'className'),
#      Output('deimos-tab2', 'selected_className'),
#      Output('deimos-subtab1', 'className'),
#      Output('deimos-subtab1', 'selected_className'),
#      Output('deimos-subtab2', 'className'),
#      Output('deimos-subtab2', 'selected_className'),
#      Output('deimos-subtab3', 'className'),
#      Output('deimos-subtab3', 'selected_className'),
#      Output('deimos-subtab4', 'className'),
#      Output('deimos-subtab4', 'selected_className'),
#      Output('deimos-subtab5', 'className'),
#      Output('deimos-subtab5', 'selected_className')],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_class_name_tab(dark_theme):
#     bVw = list()
#     temp = ''
#     if(dark_theme):
#         temp = '-dark'
#     for x in range(0,7):
#         bVw.append('custom-tab'+temp)
#         bVw.append('custom-tab--selected'+temp)
#
#     return bVw
#
# @app.callback(
#     [Output('deimos-summary-container1', 'className'),
#     Output('deimos-summary-container2', 'className'),
#     Output('deimos-summary-container3', 'className'),
#     Output('deimos-summary-container4', 'className'),
#     Output('deimos-legend-status', 'className'),
#     Output('deimos-welcome-link', 'className'),
#     Output('deimos-settings-container', 'className'),
#     Output('deimos-keyword-container', 'className'),
#     Output('deimos-graph-container1', 'className'),
#     Output('deimos-dropdown-container1', 'className'),
#     Output('deimos-dropdown1', 'className')
#     ],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_class_name(dark_theme):
#     bVw = list()
#     temp = ''
#     if(dark_theme):
#         temp = '-dark'
#     for x in range(0,9):
#         bVw.append('indicator-box'+temp)
#     bVw.append('dropdown-theme'+temp)
#     bVw.append('dropdown-theme'+temp)
#
#     return bVw



# @app.callback(
#     [Output('page-content', 'style')],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_bg(dark_theme):
#     if(dark_theme):
#         return [{'backgroundColor': '#303030', 'color': 'white'}]
#     else:
#         return [{'background-color': 'white', 'color': 'black'}]
