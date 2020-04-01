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

from KeckKeywordInterface.keywords import Keywords
from KeckKeywordInterface.app import app
from KeckKeywordInterface.apps import main_page

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
    html.Div(id='dark-osiris-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='dark-osiris-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-summary-container2', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='dark-osiris-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-summary-container3', children=[
            html.H4('Power Check'),
            daq.Indicator(
                id='dark-osiris-power-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-summary-container4', children=[
            html.H4('Daemons Check'),
            daq.Indicator(
                id='dark-osiris-daemons-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-summary-container6', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='dark-osiris-settings-check',
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
            daq.StopButton(id='dark-osiris-stop-button')
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
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='dark-osiris-welcome-link')
    ])
])

#### Check Servers/Computers Tab
check_servers = Keywords()
serverUpQ = []
serverKeyword = 'lastalive'
serverUpQ.append({'osiris' : 'global server'})
serverUpQ.append({'osds' : 'SPEC detector'})
serverUpQ.append({'oids' : 'IMAG detector'})
serverUpQ.append({'om1s' : 'SPEC collimator wheel'})
serverUpQ.append({'om2s' : 'SPEC filter wheel'})
serverUpQ.append({'om3s' : 'SPEC camera wheel'})
serverUpQ.append({'om4s' : 'SPEC lenslet mask'})
serverUpQ.append({'om5s' : 'IMAG filter wheel 1'})
serverUpQ.append({'om6s' : 'IMAG filter wheel 2'})
serverUpQ.append({'op1s' : 'power 1'})
serverUpQ.append({'op2s' : 'power 2'})
serverUpQ.append({'oprs' : 'dewar vacuum pressure monitor'})
serverUpQ.append({'ot1s' : 'dewar temperature monitor'})
serverUpQ.append({'ot2s' : 'electronics temperature monitor'})
serverUpQ.append({'otcs' : 'temperature control'})

check_computers = Keywords()
computerUpQ = []
computerUpQ.append({'napili' : 'OSIRIS host'})
computerUpQ.append({'osirisbuild' : 'Global Server Host'})
computerUpQ.append({'puunoa' : 'SPEC detector target'})
computerUpQ.append({'kuiaha' : 'IMAG detector target'})
computerUpQ.append({'osiris-control1' : 'SPEC sidecar server'})
computerUpQ.append({'osiris-control2' : 'IMAG sidecar server'})
computerUpQ.append({'osiris-drp' : 'DRP machine'})
computerUpQ.append({'osiris-odrp' : 'spare DRP machine'})
computerUpQ.append({'osrsterm' : 'terminal server'})


serversRoot2 = html.Div([
    html.Div(id='dark-osiris-servers-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Servers'),
        html.Div(id='dark-osiris-server-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[0].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[0].values())[0], list(serverUpQ[0].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[1].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[1].values())[0], list(serverUpQ[1].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[2].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[2].values())[0], list(serverUpQ[2].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[3].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[3].values())[0], list(serverUpQ[3].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[4].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[4].values())[0], list(serverUpQ[4].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-server-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[5].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[5].values())[0], list(serverUpQ[5].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[6].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[6].values())[0], list(serverUpQ[6].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[7].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[7].values())[0], list(serverUpQ[7].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[8].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[8].values())[0], list(serverUpQ[8].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[9].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[9].values())[0], list(serverUpQ[9].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-server-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[10].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[10].values())[0], list(serverUpQ[10].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[11].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[11].values())[0], list(serverUpQ[11].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[12].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[12].values())[0], list(serverUpQ[12].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[13].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[13].values())[0], list(serverUpQ[13].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(serverUpQ[14].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(serverUpQ[14].values())[0], list(serverUpQ[14].keys())[0]),
                width = 30
            )
        ])

    ]),
    html.Div(id='dark-osiris-computer-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Computers'),
        html.Div(id='dark-osiris-computer-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[0].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[0].values())[0], list(computerUpQ[0].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[1].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[1].values())[0], list(computerUpQ[1].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[2].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[2].values())[0], list(computerUpQ[2].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-computer-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[3].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[3].values())[0], list(computerUpQ[3].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[4].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[4].values())[0], list(computerUpQ[4].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[5].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[5].values())[0], list(computerUpQ[5].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-computer-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[6].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[6].values())[0], list(computerUpQ[6].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[7].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[7].values())[0], list(computerUpQ[7].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-check' % (list(computerUpQ[8].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[8].values())[0], list(computerUpQ[8].keys())[0]),
                width = 30
            )
        ]),
    ])
])

check_daemons = Keywords()
daemonsUpQ = []
for x in ['watchrot', 'watchslew', 'watchfcs', 'autodisplay']:
    daemonsUpQ.append({'LIBRARY' : 'osiris','KEYWORD' : '%sok' % (x), 'NAME' : x})
daemonsUpQ.append({'LIBRARY':'osiris','KEYWORD' : 'darenabl', 'NAME' : 'DAR correction'})


daemonRoot2 = html.Div([
    html.Div(id='dark-osiris-daemons-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Daemons'),
        html.Div(id='dark-osiris-daemons-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (daemonsUpQ[0]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label='%s' % (daemonsUpQ[0]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-daemons-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (daemonsUpQ[1]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label='%s' % (daemonsUpQ[1]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-daemons-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (daemonsUpQ[2]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label='%s' % (daemonsUpQ[2]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-daemons-4', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (daemonsUpQ[3]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label='%s' % (daemonsUpQ[3]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-daemons-5', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-check' % (daemonsUpQ[4]['KEYWORD']),
                value=True,
                color='blue',height=30,
                label='%s' % (daemonsUpQ[4]['NAME']),
                width = 30
            )
        ])
    ])
])

check_power = Keywords()
powerOutlets = []
powerOutlets.append({'NAME':'IMAG SAM',
  'LIBRARY':'op1s',
  'KEYWORD':'pwstat4',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 1 pos 5
powerOutlets.append({'NAME':'SPEC SAM',
  'LIBRARY':'op1s',
  'KEYWORD':'pwstat5',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 1 pos 6
powerOutlets.append({'NAME':'IMAG PC',
  'LIBRARY':'op1s',
  'KEYWORD':'pwstat6',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 1 pos 7
powerOutlets.append({'NAME':'SPEC PC',
  'LIBRARY':'op1s',
  'KEYWORD':'pwstat7',
  'GOODVALUE':'1',
  'BADSTATUS':'yellow'})

# power strip 1 pos 8
powerOutlets.append({'NAME':'EC Cooling System',
  'LIBRARY':'op1s',
  'KEYWORD':'pwstat8',
  'GOODVALUE':'1',
  'BADSTATUS':'yellow'})

# power strip 2 pos 1
powerOutlets.append({'NAME':'Pressure Gauge',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat1',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 2
powerOutlets.append({'NAME':'Lakeshore 340',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat2',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 3
powerOutlets.append({'NAME':'Dewar Lakeshore 218',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat3',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 4
powerOutlets.append({'NAME':'Cabinet Lakeshore 218',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat4',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 5
powerOutlets.append({'NAME':'Motor Controllers',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat5',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 6
powerOutlets.append({'NAME':'Terminal Server',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat6',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

# power strip 2 pos 7 UNUSED

# power strip 2 pos 8
powerOutlets.append({'NAME':'EC Cooling System',
  'LIBRARY':'op2s',
  'KEYWORD':'pwstat8',
  'GOODVALUE':'1',
  'BADSTATUS':'red'})

powerRoot2 = html.Div([
    html.Div(id='dark-osiris-power-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Power Outlets'),
        html.Div(id='dark-osiris-power-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[0]['KEYWORD'], powerOutlets[0]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[1]['KEYWORD'], powerOutlets[1]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[2]['KEYWORD'], powerOutlets[2]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[2]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[3]['KEYWORD'], powerOutlets[3]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[3]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-power-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[4]['KEYWORD'], powerOutlets[4]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[5]['KEYWORD'], powerOutlets[5]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[5]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[6]['KEYWORD'], powerOutlets[6]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[7]['KEYWORD'], powerOutlets[7]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[7]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-power-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[8]['KEYWORD'], powerOutlets[8]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[8]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[9]['KEYWORD'], powerOutlets[9]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[10]['KEYWORD'], powerOutlets[10]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (powerOutlets[11]['KEYWORD'], powerOutlets[11]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[11]['NAME']),
                width = 30
            )
        ])
    ])
])

check_settings = Keywords()
settingsCheckQ = []
thresh = 0.1
settingsCheckQ.append({'NAME':'SPEC Collimator',
  'LIBRARY':'om1s',
  'KEYWORD':'status',
  'GOODVALUE':'OK',
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

# SPEC Filter
settingsCheckQ.append({'NAME':'SPEC Filter Wheel',
  'LIBRARY':'om2s',
  'KEYWORD':'status',
  'GOODVALUE':'OK',
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

# SPEC Camera Wheel
settingsCheckQ.append({'NAME':'SPEC Camera',
  'LIBRARY':'om3s',
  'KEYWORD':'status',
  'GOODVALUE':'OK',
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

# SPEC Lenslet Mask
settingsCheckQ.append({'NAME':'SPEC Lenslet Mask',
  'LIBRARY':'om4s',
  'KEYWORD':'status',
  'GOODVALUE':'OK',
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

# IMAG Filter Wheel #1
settingsCheckQ.append({'NAME':'IMAG Filter #1',
  'LIBRARY':'om5s',
  'KEYWORD':'status',
  'GOODVALUE':'OK',
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

# IMAG Filter Wheel #2
settingsCheckQ.append({'NAME':'IMAG Filter #2',
  'LIBRARY':'om6s',
  'KEYWORD':'status',
  'GOODVALUE':'OK', # two possible values are OK here
  'LOCKED':'lockall',
  'BADSTATUS':'yellow'})

trgtmp1 = float(check_settings.get_keyword('otcs','trgtmp1'))
settingsCheckQ.append({'NAME':"SPEC detector temp",
  'LIBRARY':'otcs',
  'KEYWORD':'tmp1',
  'MINVALUE': trgtmp1 - thresh,
  'MAXVALUE': trgtmp1 + thresh,
  'BADSTATUS':'yellow'})

# detector temp...
trgtmp2 = float(check_settings.get_keyword('otcs','trgtmp2'))
settingsCheckQ.append({'NAME':"IMAG detector temp",
  'LIBRARY':'otcs',
  'KEYWORD':'tmp2',
  'MINVALUE': trgtmp2 - thresh,
  'MAXVALUE': trgtmp2 + thresh,
  'BADSTATUS':'yellow'})

# CCR state...
settingsCheckQ.append({'NAME':"CCR Head",
  'LIBRARY':'ot1s',
  'KEYWORD':'tmp1',
  'MINVALUE':38.0,
  'MAXVALUE':45.0,
  'BADSTATUS':'red'})

# Dewar pressure
settingsCheckQ.append({'NAME':'dewar pressure',
  'LIBRARY':'oprs',
  'KEYWORD':'pressure',
  'MINVALUE': 10**(-8),
  'MAXVALUE': 50**(-3),
  'BADSTATUS':'red'})

# datataking system status...
settingsCheckQ.append({'NAME':'SPEC ready to expose',
  'LIBRARY':'osds',
  'KEYWORD':'ready',
  'GOODVALUE':'1',
  'BADSTATUS':'yellow'})

# datataking system status...
settingsCheckQ.append({'NAME':'IMAG ready to expose',
  'LIBRARY':'oids',
  'KEYWORD':'ready',
  'GOODVALUE':'1',
  'BADSTATUS':'yellow'})

# current instrument check...
settingsCheckQ.append({'NAME':'current instrument',
  'LIBRARY':'dcs',
  'KEYWORD':'currinst',
  'GOODVALUE':'OSIRIS',
  'BADSTATUS':'yellow'})

settingsRoot2 = html.Div([
    html.Div(id='dark-osiris-stages-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Stages'),
        html.Div(id='dark-osiris-stages-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[0]['KEYWORD'], settingsCheckQ[0]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[1]['KEYWORD'], settingsCheckQ[1]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[2]['KEYWORD'], settingsCheckQ[2]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[2]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-stages-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[3]['KEYWORD'], settingsCheckQ[3]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[3]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[4]['KEYWORD'], settingsCheckQ[4]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[5]['KEYWORD'], settingsCheckQ[5]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[5]['NAME']),
                width = 30
            )
        ])
    ]),
    html.Div(id='dark-osiris-settings-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Settings'),
        html.Div(id='dark-osiris-settings-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[6]['KEYWORD'], settingsCheckQ[6]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[7]['KEYWORD'], settingsCheckQ[7]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[7]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[8]['KEYWORD'], settingsCheckQ[8]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[8]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='dark-osiris-settings-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[9]['KEYWORD'], settingsCheckQ[9]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[10]['KEYWORD'], settingsCheckQ[10]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[11]['KEYWORD'], settingsCheckQ[11]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[11]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='dark-%s-%s-check' % (settingsCheckQ[12]['KEYWORD'], settingsCheckQ[12]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[12]['NAME']),
                width = 30
            )
        ])
    ]),
])

check_temperature = Keywords()
tempCheckQ = []
tempCheckQ.append({'NAME':'ECCS1 Intake', 'KEYWORD':'tmp1', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'ECCS1 Exhaust', 'KEYWORD':'tmp2', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'EC1 Top of Cabinet', 'KEYWORD':'tmp3', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Ambient Air', 'KEYWORD':'tmp4', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'ECCS2 Intake', 'KEYWORD':'tmp5', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'ECCS2 Exhaust', 'KEYWORD':'tmp6', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'EC2 Mid of Cabinet', 'KEYWORD':'tmp7', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'EC2 Top of Cabinet', 'KEYWORD':'tmp8', 'LIBRARY':'ot1s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'CCR Head', 'KEYWORD':'tmp1', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Primary Plate', 'KEYWORD':'tmp2', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Secondary Plate', 'KEYWORD':'tmp3', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Front Splitter Mirror', 'KEYWORD':'tmp4', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Scale Turret 2', 'KEYWORD':'tmp5', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Lenslet Mask Stage', 'KEYWORD':'tmp6', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'TMA Housing', 'KEYWORD':'tmp7', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})
tempCheckQ.append({'NAME':'Cold Shield', 'KEYWORD':'tmp8', 'LIBRARY':'ot2s', 'CURRENT':0, 'NORMAL':'Loading...'})

names=[html.H4('Description')]
keyword=[html.H4('Keyword')]
current=[html.H4('Current')]
normal=[html.H4('Normal')]

names1=[html.H4('Description')]
keyword1=[html.H4('Keyword')]
current1=[html.H4('Current')]
normal1=[html.H4('Normal')]

counter = 0
for x in tempCheckQ:
    if counter < 8:
        names.append(html.P(x['NAME']))
        keyword.append(html.P(x['KEYWORD']))
        current.append(html.P(x['CURRENT']))
        normal.append(html.P(x['NORMAL']))
    else:
        names1.append(html.P(x['NAME']))
        keyword1.append(html.P(x['KEYWORD']))
        current1.append(html.P(x['CURRENT']))
        normal1.append(html.P(x['NORMAL']))
    counter += 1

check_pressure = Keywords()
pressureCheckQ = {'KEYWORD':'pressure', 'LIBRARY':'oprs', 'NORMAL':'Loading...', 'CURRENT':0}

temperatureRoot2 = html.Div([
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-temperatures-container', children=[
        html.H4('OSIRIS Dewar Temperatures (K)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-names', children=names),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-keyword', children=keyword),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-current', children=current),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-normal', children=normal)
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-temperatures-container1', children=[
        html.H4('OSIRIS Cabinet Temperatures (K)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-names1', children=names1),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-keyword1', children=keyword1),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-current1', children=current1),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-temperatures-normal1', children=normal1)
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='dark-osiris-pressure-container', children=[
        html.H4('OSIRIS Dewar Pressure (mTorr)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-pressure-keyword', children=[
            html.H4('Keyword'),
            html.P(pressureCheckQ['KEYWORD'])
        ]),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-pressure-normal', children=[
            html.H4('Normal'),
            html.P(pressureCheckQ['NORMAL'])
        ]),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='dark-osiris-pressure-current', children=[
            html.H4('Pressure'),
            html.P(pressureCheckQ['CURRENT'])
        ])
    ])
])




layout = [
    dcc.Tabs(id="osiris-tabs", value='osiris-tabs', children=[
        dcc.Tab(id='dark-osiris-tab1', label='OSIRIS Summary', value='osiris-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Br(),
            daq.ToggleSwitch(
                id='dark-osiris-daq-light-dark-theme',
                label=['Light', 'Dark'],
                style={'width': '250px', 'margin': 'auto'},
                value=False
            ),
            html.Br(),
            html.Div(id='dark-osiris-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='dark-osiris-polling-interval',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-osiris-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='dark-osiris-tab2', label='OSIRIS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Div(id='dark-osiris-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='dark-osiris-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='dark-osiris-subtab4', label='All Servers/Computers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=serversRoot2)),
                        dcc.Tab(id='dark-osiris-subtab1', label='Daemons', value='subtab0',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=daemonRoot2)),
                        dcc.Tab(id='dark-osiris-subtab1', label='Power Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='dark-osiris-subtab2', label='Settings', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='dark-osiris-subtab3', label='Temperatures', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2))
                    ])
                ]),
            dcc.Interval(id='dark-osiris-polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='dark-osiris-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='dark-osiris-tabs-content')
]

inputs_intervals = [Input('osiris-polling-interval', 'n_intervals'), Input('osiris-polling-interval2', 'n_intervals')]
