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
import dash_table_experiments as dt
import pandas as pd

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
    html.Div(id='esi-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='esi-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='esi-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='esi-summary-container2', children=[
            html.H4('Daemons Check'),
            daq.Indicator(
                id='esi-daemons-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='esi-summary-container3', children=[
            html.H4('Keyword Libraries Check'),
            daq.Indicator(
                id='esi-keyword-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='esi-summary-container4', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='esi-settings-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='esi-summary-container5', children=[
            html.H4('Temperature Check'),
            daq.Indicator(
                id='esi-temperature-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Br(),
        html.P('Daemon Check Not Ready Yet!!!!!!!')
    ]),
    html.Br(),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='esi-stop-button')
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
                height = 20,
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
                height = 30,
                id='legend-blue',
                value=True,
                color='blue',
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='esi-welcome-link')
    ])
])

###################### Second Tab Layout ######################
###############################################################

###################### Check Computers Tab ######################

check_computers = Keywords()
computersUpQ = []
computersUpQ.append({'SERVICE':'esiserver2', 'NAME':'supervisory computer - Sun'})
computersUpQ.append({'SERVICE':'deits1', 'NAME':'Lantronix'})
computersUpQ.append({'SERVICE':'esi5cb', 'NAME':'CCD crate'})
computersUpQ.append({'SERVICE':'waiaha', 'NAME':'Sybase server'})
computersUpQ.append({'SERVICE':'esi', 'NAME':'GAlil 0 motor control', 'KEYWORD':'dwfillck', 'VALUE':'UNLOCKED'})
computersUpQ.append({'SERVICE':'esi', 'NAME':'GAlil 1 motor control', 'KEYWORD':'prismlck', 'VALUE':'UNLOCKED'})

check_daemons =  Keywords()
daemonsUpQ = []

computer = []
for x in computersUpQ:
    if x['SERVICE'] == 'esi':
        computer.append(daq.Indicator(width = 30,
            id='%s-%s-check1' % (x['SERVICE'], x['KEYWORD']),
            value=True,
            color='blue',height=30,
            label=x['NAME']
        ))
    else:
        computer.append(daq.Indicator(width = 30,
            id='%s-check' % (x['SERVICE']),
            value=True,
            color='blue',height=30,
            label=x['NAME']
        ))

computersRoot2 = html.Div([
    html.Div(id='esi-computers-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Computers'),
        html.Div(id='esi-computers-1', className='indicator-box-no-border'+class_theme['dark'], children=computer[:3]),
        html.Div(id='esi-computers-1', className='indicator-box-no-border'+class_theme['dark'], children=computer[3:]),
        html.Br(),
        html.P('Lantronix and CCD crate Not Ready Yet!!!!!!')
    ]),
    html.Div(id='esi-daemons-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Daemons'),
        html.Br(),
        html.P('Daemons Not Ready Yet!!!!!!!')
    ])
])

###################### Check Keywords Tab ######################
check_keywords = Keywords()
keywordsUpQ = []
keywordsUpQ.append({'LIBRARY':'esi', 'KEYWORD':'dwfillck', 'NAME':'dispatcher 0'})
keywordsUpQ.append({'LIBRARY':'esi', 'KEYWORD':'prismlck', 'NAME':'dispatcher 1'})
keywordsUpQ.append({'LIBRARY':'esi', 'KEYWORD':'observer', 'NAME':'infoman'})
keywordsUpQ.append({'LIBRARY':'esi', 'KEYWORD':'tempdet,wcrate', 'NAME':'CCD'})
keywordsUpQ.append({'LIBRARY':'dcs', 'KEYWORD':'ra', 'NAME':'DCS'})

keys = [html.H4('Keyword Libraries')]
counter = 0
for x in keywordsUpQ:
    counter += 1
    keys.append(html.Div(id='esi-keyword-%s' % (str(counter)), className='indicator-box-no-border'+class_theme['dark'], children=[
        daq.Indicator(width = 30,
            id='%s-%s-check' % (x['LIBRARY'], x['KEYWORD']),
            value=True,
            color='blue',height=30,
            label=x['NAME']
        )
    ]))

keywordRoot2 = html.Div([
    html.Div(id='esi-keyword-container', className='indicator-box'+class_theme['dark'], children=keys),
    html.Br(),
    html.P('DCS Not Ready Yet!!!!!!!')
])

###################### Check Settings Tab ######################
check_settings = Keywords()
settingsCheckQ = []
settingsCheckQ.append({ 'NAME':'Controller 0 5V Power',
                'LIBRARY':'esi',
                'KEYWORD':'POW05S0V',
                'MINVALUE':4.9,
                'MAXVALUE':5.1,
                'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Controller 1 5V Power',
            'LIBRARY':'esi',
            'KEYWORD':'POW05S1V',
            'MINVALUE':4.9,
            'MAXVALUE':5.1,
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Controller 0 28V Power',
            'LIBRARY':'esi',
            'KEYWORD':'POW28S0V',
            'MINVALUE':27,
            'MAXVALUE':29,
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Controller 1 28V Power',
            'LIBRARY':'esi',
            'KEYWORD':'POW28S1V',
            'MINVALUE':27,
            'MAXVALUE':29,
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'CCD 15V Power',
            'LIBRARY':'esi',
            'KEYWORD':'UTB15VEN',
            'GOODVALUE':'enabled',
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'CCD 30V Power',
            'LIBRARY':'esi',
            'KEYWORD':'UTB30VEN',
            'GOODVALUE':'enabled',
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'CCD temp setpoint',
            'LIBRARY':'esi',
            'KEYWORD':'tempset',
            'MINVALUE':-121,
            'MAXVALUE':-119,
            'BADSTATUS':'red'})
tempset = float(check_settings.get_keyword('esi','tempset'))
settingsCheckQ.append({ 'NAME':'CCD temperature',
            'LIBRARY':'esi',
            'KEYWORD':'tempdet',
            'MINVALUE':tempset-1,
            'MAXVALUE':tempset+1,
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Coolant flow',
            'LIBRARY':'esi',
            'KEYWORD':'coolflow',
            'GOODVALUE':'okay',
            'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Air pressure',
            'LIBRARY':'esi',
            'KEYWORD':'airpress',
            'GOODVALUE':'okay',
            'BADSTATUS':'red'})

# settingsCheckQ.append({ 'NAME':'Ion pump',
# 		    COMMAND:'ionpump -n',
# 		    'GOODVALUE':'3',
# 		    'BADSTATUS':'red'})
#
# settingsCheckQ.append({ 'NAME':'Black Box power',
# 		    COMMAND:'rsh k2server -l k2ruts show -s k2bb -terse ESI_STATUS',
# 		    'GOODVALUE':'ON',
# 		    'BADSTATUS':'red'})

settingsCheckQ.append({ 'NAME':'Current instrument',
            'LIBRARY':'dcs',
            'KEYWORD':'currinst',
            'GOODVALUE':'ESI',
            'BADSTATUS':'yellow'})

set = []
for x in settingsCheckQ:
    set.append(daq.Indicator(width = 30,
        id='%s-%s-checkS' % (x['LIBRARY'], x['KEYWORD']),
        value=True,
        color='blue',height=30,
        label=x['NAME']
    ))

settingsRoot2 = html.Div([
    html.Div(id='esi-settings-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Settings'),
        html.Div(id='esi-settings-1', className='indicator-box-no-border'+class_theme['dark'], children=set[:4]),
        html.Div(id='esi-settings-2', className='indicator-box-no-border'+class_theme['dark'], children=set[4:8]),
        html.Div(id='esi-settings-3', className='indicator-box-no-border'+class_theme['dark'], children=set[8:])
    ])
])

###################### Check Temperature Tab ######################
check_temperature = Keywords()
tempCheckQ = []
tempCheckQ.append({'NAME':'CCD utility board temp', 'LIBRARY':'esi', 'KEYWORD':'utbtemp', 'NORMAL':6.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'CCD desired dewar temp', 'LIBRARY':'esi', 'KEYWORD':'tempset', 'NORMAL':-120.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'CCD temperature', 'LIBRARY':'esi', 'KEYWORD':'tempdet', 'NORMAL':-120.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Spectrograph exterior temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpextc', 'NORMAL':-2.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Camera exterior temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcamc', 'NORMAL':-3.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Oss temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpossc', 'NORMAL':-100.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Frame 1 temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpfrm1c', 'NORMAL':-3.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Frame 2 temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpfrm2c', 'NORMAL':-2.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 0 coolant out temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcou0c', 'NORMAL':-3.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 1 coolant out temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcou1c', 'NORMAL':-4.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 0 electronics box temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpbox0c', 'NORMAL':1.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 1 electronics box temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpbox1c', 'NORMAL':5.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Prism temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpprsmc', 'NORMAL':-2.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 0 electronics temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpele0c', 'NORMAL':7.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 1 electronics temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpele1c', 'NORMAL':5.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Collimator temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcollc', 'NORMAL':-2.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 0 coolant in temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcin0c', 'NORMAL':-5.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Calibration lamp temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmplampc', 'NORMAL':-1.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Motor controller 1 coolant in temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpcin1c', 'NORMAL':-5.0, 'TOLERANCE':5})
tempCheckQ.append({'NAME':'Spectrograph interior temp [C]', 'LIBRARY':'esi', 'KEYWORD':'tmpintc', 'NORMAL':-2.0, 'TOLERANCE':5})

names=[html.H4('Description')]
keyword=[html.H4('Keyword')]
current=[html.H4('Current')]
normal=[html.H4('Normal')]
status=[html.H4('Status')]
for x in tempCheckQ:
    names.append(html.P(x['NAME']))
    keyword.append(html.P(x['KEYWORD']))
    current.append(html.P(-0))
    normal.append(html.P(x['NORMAL']))
    status.append(daq.Indicator(
        id='esi-%s-check' % (x['KEYWORD']),
        value=True,
        color='blue',height=20,
        label='loading...',
        width = 20,
        labelPosition='right'
    ))

temperatureRoot2 = html.Div([
    html.Div(className='indicator-box'+class_theme['dark'], id='esi-temperatures-container', children=[
        html.H4('Temperatures'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='esi-temperatures-names', children=names),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='esi-temperatures-keyword', children=keyword),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='esi-temperatures-current', children=current),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='esi-temperatures-normal', children=normal),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='esi-temperatures-status', children=status)
    ])
])

###################### OVERALL LAYOUT ######################
layout = [
    dcc.Tabs(id="esi-tabs", value='esi-tabs', children=[
        dcc.Tab(id='esi-tab1', label='ESI Summary', value='esi-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
            html.Br(),
            html.Div(id='esi-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='esi-polling-interval',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='esi-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='esi-tab2', label='ESI Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
            html.Div(id='esi-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='esi-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='esi-subtab4', label='Computers/Daemons', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=computersRoot2)),
                        dcc.Tab(id='esi-subtab1', label='Keyword Librarys', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=keywordRoot2)),
                        dcc.Tab(id='esi-subtab2', label='Settings', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='esi-subtab3', label='Temperatures', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2))
                    ])
                ]),
            dcc.Interval(id='esi-polling-interval2',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='esi-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='esi-tabs-content')
]

inputs_intervals = [Input('esi-polling-interval', 'n_intervals'), Input('esi-polling-interval2', 'n_intervals')]

outputs = []
for x in computersUpQ:
    if x['SERVICE'] == 'esi':
        outputs.append(Output('%s-%s-check1' % (x['SERVICE'], x['KEYWORD']), 'color'))
        outputs.append(Output('%s-%s-check1' % (x['SERVICE'], x['KEYWORD']), 'height'))
    else:
        outputs.append(Output('%s-check' % (x['SERVICE']), 'color'))
        outputs.append(Output('%s-check' % (x['SERVICE']), 'height'))
outputs.append(Output('esi-computer-check', 'color'))
outputs.append(Output('esi-computer-check', 'height'))
outputs.append(Output('esi-computer-check', 'label'))

esi_semaphore = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_computers(n_intervals1, n_intervals2):
    '''
    Computers indicator value checks, update values

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
    with esi_semaphore:
        stats = []
        counter = 0
        print('started esi computers')
        for x in computersUpQ:
            if x['SERVICE'] == 'esi':
                if check_computers.get_keyword(x['SERVICE'], x['KEYWORD']) == x['VALUE']:
                    stats.append('green')
                    stats.append(0)
                    counter += 1
                else:
                    stats.append('red')
                    stats.append(30)
            else:
                if check_computers.ping_computer('esi', x['SERVICE']):
                    stats.append('green')
                    stats.append(0)
                    counter += 1
                else:
                    stats.append('red')
                    stats.append(30)
        if counter == len(computersUpQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('ERROR')
        print('ended esi computers')
        return stats


outputs = []
for x in keywordsUpQ:
    outputs.append(Output('%s-%s-check' % (x['LIBRARY'], x['KEYWORD']), 'color'))
    outputs.append(Output('%s-%s-check' % (x['LIBRARY'], x['KEYWORD']), 'height'))

outputs.append(Output('esi-keyword-check', 'color'))
outputs.append(Output('esi-keyword-check', 'height'))
outputs.append(Output('esi-keyword-check', 'label'))

esi_semaphore1 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_keywords(n_intervals1, n_intervals2):
    '''
    Keywords indicator value checks, update values

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
    with esi_semaphore1:
        stats = []
        counter = 0
        print('started esi keywords')
        for x in keywordsUpQ:
            if check_keywords.server_up(x['LIBRARY'], x['KEYWORD']):
                stats.append('green')
                stats.append(0)
                counter += 1
            else:
                stats.append('red')
                stats.append(30)

        if counter == len(keywordsUpQ):
            stats.append('green')
            stats.append(0)
            stats.append('OK')
        else:
            stats.append('red')
            stats.append(50)
            stats.append('ERROR')
        print('ended esi keywords')
        return stats

outputs = []
for x in settingsCheckQ:
    outputs.append(Output('%s-%s-checkS' % (x['LIBRARY'], x['KEYWORD']), 'color'))
    outputs.append(Output('%s-%s-checkS' % (x['LIBRARY'], x['KEYWORD']), 'height'))

outputs.append(Output('esi-settings-check', 'color'))
outputs.append(Output('esi-settings-check', 'label'))
outputs.append(Output('esi-settings-check', 'height'))

esi_semaphore2 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_settings(n_intervals1, n_intervals2):
    '''
    Settings indicator value checks, update values

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
    with esi_semaphore2:
        stats = []
        counterGreen = 0
        counterYellow = 0
        print('started esi settings')
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
        print('ended esi settings')
        return stats

outputs = []
for x in tempCheckQ:
    outputs.append(Output('esi-%s-check' % (x['KEYWORD']), 'color'))
    outputs.append(Output('esi-%s-check' % (x['KEYWORD']), 'label'))
    outputs.append(Output('esi-%s-check' % (x['KEYWORD']), 'height'))

outputs.append(Output('esi-temperatures-current', 'children'))

outputs.append(Output('esi-temperature-check', 'color'))
outputs.append(Output('esi-temperature-check', 'label'))
outputs.append(Output('esi-temperature-check', 'height'))
outputs.append(Output('esi-tab1', 'disabled'))
outputs.append(Output('esi-tab2', 'disabled'))

esi_semaphore3 = threading.Semaphore()
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
    with esi_semaphore3:
        stats = []
        counter = 0
        current=[html.H4('Current')]
        for x in tempCheckQ:
            valueTemp = float(check_temperature.get_keyword(x['LIBRARY'], x['KEYWORD']))
            current.append(html.P(valueTemp))
            if abs(valueTemp - x['NORMAL']) <= x['TOLERANCE']:
                stats.append('green')
                stats.append('Good')
                stats.append(0)
                counter += 1
            else:
                stats.append('red')
                stats.append('ERROR')
                stats.append(20)
        stats.append(current)
        if counter == len(tempCheckQ):
            stats.append('green')
            stats.append('Good')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)
        stats.append(False)
        stats.append(False)
        return stats
