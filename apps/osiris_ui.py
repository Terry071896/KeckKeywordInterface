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

histKeys = Keywords()
##### Check Settings Tab
settings_keywords = Keywords()

rootLayout1 = html.Div([
    html.Div(id='osiris-summary-container', children=[
        html.Div(className='indicator-box', id='osiris-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='osiris-computer-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box', id='osiris-summary-container2', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='osiris-server-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='osiris-summary-container3', children=[
            html.H4('Power Check'),
            daq.Indicator(
                id='osiris-power-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='osiris-summary-container4', children=[
            html.H4('Daimons Check'),
            daq.Indicator(
                id='osiris-daimons-check',
                value=True,
                color='blue',
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box', id='osiris-summary-container6', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='osiris-settings-check',
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
            daq.StopButton(id='osiris-stop-button')
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
                id='legend-blue',
                value=True,
                color='blue',
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box', id='osiris-welcome-link')
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
    html.Div(id='osiris-servers-container', className='indicator-box', children=[
        html.H4('Servers'),
        html.Div(id='osiris-server-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[0].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[0].values())[0], list(serverUpQ[0].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[1].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[1].values())[0], list(serverUpQ[1].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[2].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[2].values())[0], list(serverUpQ[2].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[3].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[3].values())[0], list(serverUpQ[3].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[4].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[4].values())[0], list(serverUpQ[4].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-server-2', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[5].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[5].values())[0], list(serverUpQ[5].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[6].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[6].values())[0], list(serverUpQ[6].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[7].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[7].values())[0], list(serverUpQ[7].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[8].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[8].values())[0], list(serverUpQ[8].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[9].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[9].values())[0], list(serverUpQ[9].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-server-3', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[10].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[10].values())[0], list(serverUpQ[10].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[11].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[11].values())[0], list(serverUpQ[11].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[12].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[12].values())[0], list(serverUpQ[12].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[13].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[13].values())[0], list(serverUpQ[13].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(serverUpQ[14].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(serverUpQ[14].values())[0], list(serverUpQ[14].keys())[0]),
                width = 30
            )
        ])

    ]),
    html.Div(id='osiris-computer-container', className='indicator-box', children=[
        html.H4('Computers'),
        html.Div(id='osiris-computer-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[0].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[0].values())[0], list(computerUpQ[0].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[1].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[1].values())[0], list(computerUpQ[1].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[2].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[2].values())[0], list(computerUpQ[2].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-computer-2', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[3].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[3].values())[0], list(computerUpQ[3].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[4].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[4].values())[0], list(computerUpQ[4].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[5].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[5].values())[0], list(computerUpQ[5].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-computer-3', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[6].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[6].values())[0], list(computerUpQ[6].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[7].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[7].values())[0], list(computerUpQ[7].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[8].keys())[0]),
                value=True,
                color='blue',
                label='%s (%s)' % (list(computerUpQ[8].values())[0], list(computerUpQ[8].keys())[0]),
                width = 30
            )
        ]),
    ])
])

check_daimons = Keywords()
daimonsUpQ = []
for x in ['watchrot', 'watchslew', 'watchfcs', 'autodisplay']:
    daimonsUpQ.append({'LIBRARY' : 'osiris','KEYWORD' : '%sok' % (x), 'NAME' : x})
daimonsUpQ.append({'LIBRARY':'osiris','KEYWORD' : 'darenabl', 'NAME' : 'DAR correction'})


daimonRoot2 = html.Div([
    html.Div(id='osiris-daimons-container', className='indicator-box', children=[
        html.H4('Daimons'),
        html.Div(id='osiris-daimons-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (daimonsUpQ[0]['KEYWORD']),
                value=True,
                color='blue',
                label='%s' % (daimonsUpQ[0]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-daimons-2', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (daimonsUpQ[1]['KEYWORD']),
                value=True,
                color='blue',
                label='%s' % (daimonsUpQ[1]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-daimons-3', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (daimonsUpQ[2]['KEYWORD']),
                value=True,
                color='blue',
                label='%s' % (daimonsUpQ[2]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-daimons-4', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (daimonsUpQ[3]['KEYWORD']),
                value=True,
                color='blue',
                label='%s' % (daimonsUpQ[3]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-daimons-5', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-check' % (daimonsUpQ[4]['KEYWORD']),
                value=True,
                color='blue',
                label='%s' % (daimonsUpQ[4]['NAME']),
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
    html.Div(id='osiris-power-container', className='indicator-box', children=[
        html.H4('Power Outlets'),
        html.Div(id='osiris-power-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[0]['KEYWORD'], powerOutlets[0]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[1]['KEYWORD'], powerOutlets[1]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[2]['KEYWORD'], powerOutlets[2]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[2]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[3]['KEYWORD'], powerOutlets[3]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[3]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-power-2', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[4]['KEYWORD'], powerOutlets[4]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[5]['KEYWORD'], powerOutlets[5]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[5]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[6]['KEYWORD'], powerOutlets[6]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[7]['KEYWORD'], powerOutlets[7]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[7]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-power-3', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[8]['KEYWORD'], powerOutlets[8]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[8]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[9]['KEYWORD'], powerOutlets[9]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[10]['KEYWORD'], powerOutlets[10]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (powerOutlets[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[11]['KEYWORD'], powerOutlets[11]['LIBRARY']),
                value=True,
                color='blue',
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
    html.Div(id='osiris-stages-container', className='indicator-box', children=[
        html.H4('Stages'),
        html.Div(id='osiris-stages-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[0]['KEYWORD'], settingsCheckQ[0]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[1]['KEYWORD'], settingsCheckQ[1]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[2]['KEYWORD'], settingsCheckQ[2]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[2]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-stages-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[3]['KEYWORD'], settingsCheckQ[3]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[3]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[4]['KEYWORD'], settingsCheckQ[4]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[5]['KEYWORD'], settingsCheckQ[5]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[5]['NAME']),
                width = 30
            )
        ])
    ]),
    html.Div(id='osiris-settings-container', className='indicator-box', children=[
        html.H4('Settings'),
        html.Div(id='osiris-settings-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[6]['KEYWORD'], settingsCheckQ[6]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[7]['KEYWORD'], settingsCheckQ[7]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[7]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[8]['KEYWORD'], settingsCheckQ[8]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[8]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-settings-1', className='indicator-box-no-border', children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[9]['KEYWORD'], settingsCheckQ[9]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[10]['KEYWORD'], settingsCheckQ[10]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[11]['KEYWORD'], settingsCheckQ[11]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[11]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[12]['KEYWORD'], settingsCheckQ[12]['LIBRARY']),
                value=True,
                color='blue',
                label='%s' % (settingsCheckQ[12]['NAME']),
                width = 30
            )
        ])
    ]),
])

check_temperature = Keywords()
tempCheckQ = []


temperatureRoot2 = html.Div([
    html.Div(className='indicator-box', id='osiris-temperatures-container', children=[
        html.H4('Temperatures'),
    ])
])

check_pressure = Keywords()
pressureCheckQ = []

pressureRoot2 = html.Div([
    html.Div(className='indicator-box', id='osiris-pressure-container', children=[
        html.H4('Pressures'),
    ])
])

layout = [
    dcc.Tabs(id="osiris-tabs", value='osiris-tabs', children=[
        dcc.Tab(id='osiris-tab1', label='OSIRIS Summary', value='osiris-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Br(),
            daq.ToggleSwitch(
                id='osiris-daq-light-dark-theme',
                label=['Light', 'Dark'],
                style={'width': '250px', 'margin': 'auto'},
                value=False
            ),
            html.Br(),
            html.Div(id='osiris-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='osiris-polling-interval',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='osiris-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='osiris-tab2', label='OSIRIS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=False, children=[
            html.Div(id='osiris-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='osiris-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='osiris-subtab4', label='All Servers/Computers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=serversRoot2)),
                        dcc.Tab(id='osiris-subtab1', label='Daimons', value='subtab0',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=daimonRoot2)),
                        dcc.Tab(id='osiris-subtab1', label='Power Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='osiris-subtab2', label='Settings', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='osiris-subtab3', label='Temperatures', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2)),
                        dcc.Tab(id='osiris-subtab3', label='Pressures', value='subtab5', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=pressureRoot2))
                    ])
                ]),
            dcc.Interval(id='osiris-polling-interval2',
                n_intervals=0,
                interval=2*1000,
                disabled=False
            ),
            dcc.Store(id='osiris-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='osiris-tabs-content')
]

inputs_intervals = [Input('osiris-polling-interval', 'n_intervals'), Input('osiris-polling-interval2', 'n_intervals')]
