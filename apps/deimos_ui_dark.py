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
    html.Div(id='dark-deimos-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='dark-deimos-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-summary-container2', children=[
            html.H4('Daemons Check'),
            daq.Indicator(
                id='dark-deimos-daemons-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-summary-container3', children=[
            html.H4('Keyword Librarys Check'),
            daq.Indicator(
                id='dark-deimos-keyword-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-summary-container4', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='dark-deimos-settings-check',
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
            daq.StopButton(id='dark-deimos-stop-button')
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
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='dark-deimos-welcome-link')
    ])
])

settingsRoot2 = html.Div([
    html.Div(id='dark-deimos-settings-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Settings Check'),
        html.Div(id='dark-deimos-settings-1', children=[
            daq.Indicator(
                id='dark-tempset-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[0]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-tempdet-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[1]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-coolflow-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[2]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-tvcoflow-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[3]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-airpressBarrel-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[4]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-airpressCradle-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[5]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-ionpump1-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[6]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='dark-deimos-settings-2', children=[
            daq.Indicator(
                id='dark-ionpump2-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[7]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-UTB15VEN-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[8]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-UTB30VEN-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[9]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-UTB15VEN-fcs-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[10]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-UTB30VEN-fcs-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[11]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-fcscusel-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[12]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-fcsfoto1-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[13]['NAME'],
                width = 30
            )
        ]),
        html.Div(id='dark-deimos-settings-3', children=[
            daq.Indicator(
                id='dark-fcsfoto2-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[14]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-addframeScience-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[15]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-addframeFCS-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[16]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-currinst-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[17]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-rotccwlm-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[18]['NAME'],
                width = 30
            ),
            daq.Indicator(
                id='dark-rotcwlm-check',
                value=True,
                color='blue',height=30,
                label=settingsGoodQ[19]['NAME'],
                width = 30
            ),
        ])
    ])
])

keywordsRoot2 = html.Div([
    html.Div(id='dark-deimos-keyword-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Keyword Library Checks'),
        html.Div(id='dark-deimos-keyword-container1', children=[
            daq.Indicator(
                id='dark-tvfilraw-check',
                value=True,
                color='blue',height=30,
                label='Dispatcher 1',
                width = 30
            ),
            daq.Indicator(
                id='dark-g4tltraw-check',
                value=True,
                color='blue',height=30,
                label='Dispatcher 2',
                width = 30
            ),
            daq.Indicator(
                id='dark-tmirrraw-check',
                value=True,
                color='blue',height=30,
                label='Piezo',
                width = 30
            )
        ]),
        html.Div(id='dark-deimos-keyword-container2', children=[
            daq.Indicator(
                id='dark-hplogtim-check',
                value=True,
                color='blue',height=30,
                label='Hplogger',
                width = 30
            ),
            daq.Indicator(
                id='dark-slbarcfg-check',
                value=True,
                color='blue',height=30,
                label='Barco',
                width = 30
            ),
            daq.Indicator(
                id='dark-bargncfg-check',
                value=True,
                color='blue',height=30,
                label='Bargun',
                width = 30
            )
        ]),
        html.Div(id='dark-deimos-keyword-container3', children=[
            daq.Indicator(
                id='dark-two-check',
                value=True,
                color='blue',height=30,
                label='CCD+infopatcher',
                width = 30
            ),
            daq.Indicator(
                id='dark-wo-check',
                value=True,
                color='blue',height=30,
                label='FCS+infopatcher',
                width = 30
            ),
            daq.Indicator(
                id='dark-rotatval-check',
                value=True,
                color='blue',height=30,
                label='Rotator',
                width = 30
            )
        ]),
        html.Div(id='dark-deimos-keyword-container4', children=[
            daq.Indicator(
                id='dark-mode-check',
                value=True,
                color='blue',height=30,
                label='ACS',
                width = 30
            ),
            daq.Indicator(
                id='dark-ra-check',
                value=True,
                color='blue',height=30,
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
    paper_bgcolor="#303030",
    legend=go.layout.Legend(font=dict(color='white'))
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
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-graph-container1', children=[
        html.H4('Science Detector Temperature'),
        dcc.Graph(
            id='dark-deimos-temperature-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': temperature_layout if class_theme['dark'] == '' else temperature_layout_dark
            }),
        )
    ]),
    html.Div(id='dark-legend-container2', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-deimos-dropdown-container1', children=[
            html.H4('Temperature History'),
            html.Div(className='dropdown-theme'+class_theme['dark'], id='dark-deimos-dropdown1', children=[
                dcc.Dropdown(
                    id='dark-deimos-temperature-graph-dropdown',
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
        dcc.Tab(id='dark-deimos-tab1', label='DEIMOS Summary', value='deimos-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Br(),
            daq.ToggleSwitch(
                id='dark-deimos-daq-light-dark-theme',
                label=['Light', 'Dark'],
                style={'width': '250px', 'margin': 'auto'},
                value=False
            ),
            html.Br(),
            html.Div(id='dark-deimos-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='dark-deimos-polling-interval',
                n_intervals=0,
                interval=10*1000,
                disabled=False
            ),
            dcc.Store(id='dark-deimos-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='dark-deimos-tab2', label='DEIMOS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected'+class_theme['dark'], disabled=True, children=[
            html.Div(id='dark-deimos-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='dark-deimos-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='dark-deimos-subtab4', label='Settings Checks', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='dark-deimos-subtab1', label='Keyword Library Checks', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=keywordsRoot2)),
                        dcc.Tab(id='dark-deimos-subtab2', label='Temperatures', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='dark-deimos-subtab3', label='[Maybe More...]', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected'+class_theme['dark'], children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='dark-deimos-polling-interval2',
                n_intervals=0,
                interval=10*1000,
                disabled=False
            ),
            dcc.Store(id='dark-deimos-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='dark-deimos-tabs-content')
]

@app.callback(
    [Output('dark-deimos-polling-interval', 'disabled'),
    Output('dark-deimos-polling-interval2', 'disabled'),
     Output('dark-deimos-stop-button', 'buttonText')],
    [Input('deimos-stop-button', 'n_clicks')],
    state=[State('deimos-polling-interval', 'disabled'),
    State('deimos-polling-interval2', 'disabled')]
)
def stop_production(_, current, current2):
    return not current, not current2, "stop" if current else "start"




@app.callback(
    [Output('dark-tvfilraw-check', 'color'),
    Output('dark-tvfilraw-check', 'height'),
    Output('dark-g4tltraw-check', 'color'),
    Output('dark-g4tltraw-check', 'height'),
    Output('dark-tmirrraw-check', 'color'),
    Output('dark-tmirrraw-check', 'height'),
    Output('dark-hplogtim-check', 'color'),
    Output('dark-hplogtim-check', 'height'),
    Output('dark-slbarcfg-check', 'color'),
    Output('dark-slbarcfg-check', 'height'),
    Output('dark-bargncfg-check', 'color'),
    Output('dark-bargncfg-check', 'height'),
    Output('dark-two-check', 'color'),
    Output('dark-two-check', 'height'),
    Output('dark-wo-check', 'color'),
    Output('dark-wo-check', 'height'),
    Output('dark-rotatval-check', 'color'),
    Output('dark-rotatval-check', 'height'),
    Output('dark-mode-check', 'color'),
    Output('dark-mode-check', 'height'),
    Output('dark-ra-check', 'color'),
    Output('dark-ra-check', 'height'),
    Output('dark-deimos-keyword-check', 'color'),
    Output('dark-deimos-keyword-check', 'label'),
    Output('dark-deimos-keyword-check', 'height')
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
    [Output('dark-tempset-check', 'color'),
    Output('dark-tempdet-check', 'color'),
    Output('dark-coolflow-check', 'color'),
    Output('dark-tvcoflow-check', 'color'),
    Output('dark-airpressBarrel-check', 'color'),
    Output('dark-airpressCradle-check', 'color'),
    Output('dark-ionpump1-check', 'color'),
    Output('dark-ionpump2-check', 'color'),
    Output('dark-UTB15VEN-check', 'color'),
    Output('dark-UTB30VEN-check', 'color'),
    Output('dark-UTB15VEN-fcs-check', 'color'),
    Output('dark-UTB30VEN-fcs-check', 'color'),
    Output('dark-fcscusel-check', 'color'),
    Output('dark-fcsfoto1-check', 'color'),
    Output('dark-fcsfoto2-check', 'color'),
    Output('dark-addframeScience-check', 'color'),
    Output('dark-addframeFCS-check', 'color'),
    Output('dark-currinst-check', 'color'),
    Output('dark-rotccwlm-check', 'color'),
    Output('dark-rotcwlm-check', 'color'),
    Output('dark-tempset-check', 'height'),
    Output('dark-tempdet-check', 'height'),
    Output('dark-coolflow-check', 'height'),
    Output('dark-tvcoflow-check', 'height'),
    Output('dark-airpressBarrel-check', 'height'),
    Output('dark-airpressCradle-check', 'height'),
    Output('dark-ionpump1-check', 'height'),
    Output('dark-ionpump2-check', 'height'),
    Output('dark-UTB15VEN-check', 'height'),
    Output('dark-UTB30VEN-check', 'height'),
    Output('dark-UTB15VEN-fcs-check', 'height'),
    Output('dark-UTB30VEN-fcs-check', 'height'),
    Output('dark-fcscusel-check', 'height'),
    Output('dark-fcsfoto1-check', 'height'),
    Output('dark-fcsfoto2-check', 'height'),
    Output('dark-addframeScience-check', 'height'),
    Output('dark-addframeFCS-check', 'height'),
    Output('dark-currinst-check', 'height'),
    Output('dark-rotccwlm-check', 'height'),
    Output('dark-rotcwlm-check', 'height'),
    Output('dark-deimos-settings-check', 'color'),
    Output('dark-deimos-settings-check', 'label'),
    Output('dark-deimos-settings-check', 'height'),
    Output('dark-deimos-tab1', 'disabled'),
    Output('dark-deimos-tab2', 'disabled')],
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
        stats.append(20)
    else:
        stats.append('red')
        stats.append('ERROR')
        stats.append(50)

    stats.append(False)
    stats.append(False)
    print('settings_check done')
    return stats


@app.callback(
    [Output('dark-deimos-temperature-graph', 'figure')],
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
#     [Output('dark-deimos-keyword-check', 'color'),
#     Output('dark-deimos-keyword-check', 'label'),
#     Output('dark-deimos-settings-check', 'color'),
#     Output('dark-deimos-settings-check', 'label')],
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
#     [Output('dark-deimos-dark-theme-component-demo', 'children'),
#      Output('dark-deimos-subtab4', 'children'),
#      Output('dark-deimos-subtab1', 'children'),
#      Output('dark-deimos-subtab2', 'children'),
#      Output('dark-deimos-subtab3', 'children')],
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
#     [Output('dark-deimos-tab1', 'className'),
#      Output('dark-deimos-tab1', 'selected_className'),
#      Output('dark-deimos-tab2', 'className'),
#      Output('dark-deimos-tab2', 'selected_className'),
#      Output('dark-deimos-subtab1', 'className'),
#      Output('dark-deimos-subtab1', 'selected_className'),
#      Output('dark-deimos-subtab2', 'className'),
#      Output('dark-deimos-subtab2', 'selected_className'),
#      Output('dark-deimos-subtab3', 'className'),
#      Output('dark-deimos-subtab3', 'selected_className'),
#      Output('dark-deimos-subtab4', 'className'),
#      Output('dark-deimos-subtab4', 'selected_className'),
#      Output('dark-deimos-subtab5', 'className'),
#      Output('dark-deimos-subtab5', 'selected_className')],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_class_name_tab(dark_theme):
#     bVw = list()
#     temp = ''
#     if(dark_theme):
#         temp = '-dark'
#     for x in range(0,7):
#         bVw.append('custom-tab'+temp)
#         bVw.append('custom-tab--selected'+class_theme['dark']+temp)
#
#     return bVw
#
# @app.callback(
#     [Output('dark-deimos-summary-container1', 'className'),
#     Output('dark-deimos-summary-container2', 'className'),
#     Output('dark-deimos-summary-container3', 'className'),
#     Output('dark-deimos-summary-container4', 'className'),
#     Output('dark-deimos-legend-status', 'className'),
#     Output('dark-deimos-welcome-link', 'className'),
#     Output('dark-deimos-settings-container', 'className'),
#     Output('dark-deimos-keyword-container', 'className'),
#     Output('dark-deimos-graph-container1', 'className'),
#     Output('dark-deimos-dropdown-container1', 'className'),
#     Output('dark-deimos-dropdown1', 'className')
#     ],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_class_name(dark_theme):
#     bVw = list()
#     temp = ''
#     if(dark_theme):
#         temp = '-dark'
#     for x in range(0,9):
#         bVw.append('indicator-box'+class_theme['dark']+temp)
#     bVw.append('dropdown-theme'+temp)
#     bVw.append('dropdown-theme'+temp)
#
#     return bVw



# @app.callback(
#     [Output('dark-page-content', 'style')],
#     [Input('deimos-daq-light-dark-theme', 'value')]
# )
# def change_bg(dark_theme):
#     if(dark_theme):
#         return [{'backgroundColor': '#303030', 'color': 'white'}]
#     else:
#         return [{'background-color': 'white', 'color': 'black'}]
