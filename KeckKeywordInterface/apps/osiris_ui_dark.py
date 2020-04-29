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
    html.Div(id='osiris-summary-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], id='osiris-summary-container1', children=[
            html.H4('Computer Check'),
            daq.Indicator(
                id='osiris-computer-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            ),
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='osiris-summary-container2', children=[
            html.H4('Server Check'),
            daq.Indicator(
                id='osiris-server-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='osiris-summary-container3', children=[
            html.H4('Power Check'),
            daq.Indicator(
                id='osiris-power-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ]),
        html.Div(className='indicator-box'+class_theme['dark'], id='osiris-summary-container6', children=[
            html.H4('Settings Check'),
            daq.Indicator(
                id='osiris-settings-check',
                value=True,
                color='blue',height=50,
                label='Loading...',
                width = 50
            )
        ])
    ]),
    html.Br(),
    html.Div(id='legend-container', children=[
        html.Div(className='indicator-box'+class_theme['dark'], children=[
            daq.StopButton(id='osiris-stop-button')
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
                id='legend-blue',
                value=True,
                color='blue',height=30,
                label='Loading ='
            )
        ]),
        html.Br(),
        dcc.Link('Go to Welcome Page', href='/', className='indicator-box'+class_theme['dark'], id='osiris-welcome-link')
    ])
])
###################### Second Tab Layout ######################
###############################################################

###################### Check Servers/Computers Tab ######################
check_servers = Keywords()
serverUpQ = []
serverKeyword = 'lastalive'
serverUpQ.append({'LIBRARY':'osiris', 'NAME':'global server', 'KEYWORD':'telescop'})
serverUpQ.append({'LIBRARY':'osds', 'NAME' : 'SPEC detector', 'KEYWORD':'ready'})
serverUpQ.append({'LIBRARY':'oids', 'NAME': 'IMAG detector', 'KEYWORD':'numreads'})
serverUpQ.append({'LIBRARY':'om1s', 'NAME': 'SPEC collimator wheel', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'om2s', 'NAME': 'SPEC filter wheel', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'om3s', 'NAME': 'SPEC camera wheel', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'om4s', 'NAME': 'SPEC lenslet mask', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'om5s', 'NAME': 'IMAG filter wheel 1', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'om6s', 'NAME': 'IMAG filter wheel 2', 'KEYWORD':'range'})
serverUpQ.append({'LIBRARY':'op1s', 'NAME': 'power 1', 'KEYWORD':'comment'})
serverUpQ.append({'LIBRARY':'op2s', 'NAME': 'power 2', 'KEYWORD':'comment'})
serverUpQ.append({'LIBRARY':'oprs', 'NAME': 'dewar vacuum pressure monitor', 'KEYWORD':'comment'})
serverUpQ.append({'LIBRARY':'ot1s', 'NAME': 'dewar temperature monitor', 'KEYWORD':'port'})
serverUpQ.append({'LIBRARY':'ot2s', 'NAME': 'electronics temperature monitor', 'KEYWORD':'port'})
serverUpQ.append({'LIBRARY':'otcs', 'NAME': 'temperature control', 'KEYWORD':'port'})

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
    html.Div(id='osiris-servers-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Servers'),
        html.Div(id='osiris-server-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (serverUpQ[0]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[0]['NAME'], serverUpQ[0]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[1]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[1]['NAME'], serverUpQ[1]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[2]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[2]['NAME'], serverUpQ[2]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[3]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[3]['NAME'], serverUpQ[3]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[4]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[4]['NAME'], serverUpQ[4]['LIBRARY']),
                width = 30
            )
        ]),
        html.Div(id='osiris-server-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (serverUpQ[5]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[5]['NAME'], serverUpQ[5]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[6]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[6]['NAME'], serverUpQ[6]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[7]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[7]['NAME'], serverUpQ[7]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[8]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[8]['NAME'], serverUpQ[8]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[9]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[9]['NAME'], serverUpQ[9]['LIBRARY']),
                width = 30
            )
        ]),
        html.Div(id='osiris-server-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (serverUpQ[10]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[10]['NAME'], serverUpQ[10]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[11]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[11]['NAME'], serverUpQ[11]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[12]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[12]['NAME'], serverUpQ[12]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[13]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[13]['NAME'], serverUpQ[13]['LIBRARY']),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (serverUpQ[14]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (serverUpQ[14]['NAME'], serverUpQ[14]['LIBRARY']),
                width = 30
            )
        ])

    ]),
    html.Div(id='osiris-computer-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Computers'),
        html.Div(id='osiris-computer-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[0].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[0].values())[0], list(computerUpQ[0].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[1].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[1].values())[0], list(computerUpQ[1].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[2].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[2].values())[0], list(computerUpQ[2].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-computer-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[3].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[3].values())[0], list(computerUpQ[3].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[4].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[4].values())[0], list(computerUpQ[4].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[5].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[5].values())[0], list(computerUpQ[5].keys())[0]),
                width = 30
            )
        ]),
        html.Div(id='osiris-computer-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[6].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[6].values())[0], list(computerUpQ[6].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[7].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[7].values())[0], list(computerUpQ[7].keys())[0]),
                width = 30
            ),
            daq.Indicator(
                id='%s-check' % (list(computerUpQ[8].keys())[0]),
                value=True,
                color='blue',height=30,
                label='%s (%s)' % (list(computerUpQ[8].values())[0], list(computerUpQ[8].keys())[0]),
                width = 30
            )
        ]),
    ])
])

###################### Power Tab ######################
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
    html.Div(id='osiris-power-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Power Outlets'),
        html.Div(id='osiris-power-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[0]['KEYWORD'], powerOutlets[0]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[1]['KEYWORD'], powerOutlets[1]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[2]['KEYWORD'], powerOutlets[2]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[2]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[3]['KEYWORD'], powerOutlets[3]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[3]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-power-2', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[4]['KEYWORD'], powerOutlets[4]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[5]['KEYWORD'], powerOutlets[5]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[5]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[6]['KEYWORD'], powerOutlets[6]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[7]['KEYWORD'], powerOutlets[7]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[7]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-power-3', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[8]['KEYWORD'], powerOutlets[8]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[8]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[9]['KEYWORD'], powerOutlets[9]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[10]['KEYWORD'], powerOutlets[10]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (powerOutlets[11]['KEYWORD'], powerOutlets[11]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (powerOutlets[11]['NAME']),
                width = 30
            )
        ])
    ])
])

###################### Settings Tab ######################

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
    html.Div(id='osiris-stages-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Stages'),
        html.Div(id='osiris-stages-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[0]['KEYWORD'], settingsCheckQ[0]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[0]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[1]['KEYWORD'], settingsCheckQ[1]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[1]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[2]['KEYWORD'], settingsCheckQ[2]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[2]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-stages-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[3]['KEYWORD'], settingsCheckQ[3]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[3]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[4]['KEYWORD'], settingsCheckQ[4]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[4]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[5]['KEYWORD'], settingsCheckQ[5]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[5]['NAME']),
                width = 30
            )
        ])
    ]),
    html.Div(id='osiris-settings-container', className='indicator-box'+class_theme['dark'], children=[
        html.H4('Settings'),
        html.Div(id='osiris-settings-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[6]['KEYWORD'], settingsCheckQ[6]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[6]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[7]['KEYWORD'], settingsCheckQ[7]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[7]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[8]['KEYWORD'], settingsCheckQ[8]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[8]['NAME']),
                width = 30
            )
        ]),
        html.Div(id='osiris-settings-1', className='indicator-box-no-border'+class_theme['dark'], children=[
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[9]['KEYWORD'], settingsCheckQ[9]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[9]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[10]['KEYWORD'], settingsCheckQ[10]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[10]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[11]['KEYWORD'], settingsCheckQ[11]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[11]['NAME']),
                width = 30
            ),
            daq.Indicator(
                id='%s-%s-check' % (settingsCheckQ[12]['KEYWORD'], settingsCheckQ[12]['LIBRARY']),
                value=True,
                color='blue',height=30,
                label='%s' % (settingsCheckQ[12]['NAME']),
                width = 30
            )
        ])
    ]),
])

###################### Temperature/Pressure Tab ######################
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
    html.Div(className='indicator-box'+class_theme['dark'], id='osiris-temperatures-container', children=[
        html.H4('OSIRIS Dewar Temperatures (K)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-names', children=names),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-current', children=current),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-normal', children=normal)
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='osiris-temperatures-container1', children=[
        html.H4('OSIRIS Cabinet Temperatures (K)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-names1', children=names1),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-current1', children=current1),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-temperatures-normal1', children=normal1)
    ]),
    html.Div(className='indicator-box'+class_theme['dark'], id='osiris-pressure-container', children=[
        html.H4('OSIRIS Dewar Pressure (mTorr)'),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-pressure-keyword', children=[
            html.H4('Keyword'),
            html.P(pressureCheckQ['KEYWORD'])
        ]),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-pressure-current', children=[
            html.H4('Pressure'),
            html.P(pressureCheckQ['CURRENT'])
        ]),
        html.Div(className='indicator-box-no-border'+class_theme['dark'], id='osiris-pressure-normal', children=[
            html.H4('Normal'),
            html.P(pressureCheckQ['NORMAL'])
        ])
    ])
])



###################### OVERALL LAYOUT ######################
layout = [
    dcc.Tabs(id="osiris-tabs", value='osiris-tabs', children=[
        dcc.Tab(id='osiris-tab1', label='OSIRIS Summary', value='osiris-tabs1', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
            html.Br(),
            html.Div(id='osiris-dark-theme-component-demo',
                children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
            dcc.Interval(id='osiris-polling-interval',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='osiris-annotations-storage',
                data=[]
            )
        ]),
        dcc.Tab(id='osiris-tab2', label='OSIRIS Servers', value='tab2', className='custom-tab'+class_theme['dark'],
                selected_className='custom-tab--selected', disabled=True, children=[
            html.Div(id='osiris-dark-theme-component-demo2',
                children=[
                    dcc.Tabs(id='osiris-subtabs', value='subtabs1', children=[
                        dcc.Tab(id='osiris-subtab4', label='All Servers/Computers', value='subtab4', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=serversRoot2)),
                        dcc.Tab(id='osiris-subtab1', label='Power Servers', value='subtab1',className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=powerRoot2)),
                        dcc.Tab(id='osiris-subtab2', label='Settings', value='subtab2', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=settingsRoot2)),
                        dcc.Tab(id='osiris-subtab3', label='Temperatures', value='subtab3', className='custom-tab'+class_theme['dark'],
                            selected_className='custom-tab--selected', children=daq.DarkThemeProvider(theme=theme, children=temperatureRoot2))
                    ])
                ]),
            dcc.Interval(id='osiris-polling-interval2',
                n_intervals=0,
                interval=30*1000,
                disabled=False
            ),
            dcc.Store(id='osiris-annotations-storage2',
                data=[]
            )
        ]),
    ]),
    html.Div(id='osiris-tabs-content')
]

inputs_intervals = [Input('osiris-polling-interval', 'n_intervals'), Input('osiris-polling-interval2', 'n_intervals')] # interval input list for all callbacks for updating both pages
outputs = []
for x in serverUpQ:
    outputs.append(Output('%s-check' % (x['LIBRARY']), 'color'))
    outputs.append(Output('%s-check' % (x['LIBRARY']), 'height'))
for x in computerUpQ:
    outputs.append(Output('%s-check' % (list(x.keys())[0]), 'color'))
    outputs.append(Output('%s-check' % (list(x.keys())[0]), 'height'))

outputs.append(Output('osiris-server-check', 'color'))
outputs.append(Output('osiris-server-check', 'label'))
outputs.append(Output('osiris-server-check', 'height'))

outputs.append(Output('osiris-computer-check', 'color'))
outputs.append(Output('osiris-computer-check', 'label'))
outputs.append(Output('osiris-computer-check', 'height'))

osiris_semaphore = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
)
def populate_servers_computers(n_intervals1, n_intervals2):
    '''
    Server and Computer indicator value checks, update values

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
    with osiris_semaphore:
        stats = []
        counterS = 0
        counterC = 0
        for x in serverUpQ:
            if check_servers.server_up(x['LIBRARY'], x['KEYWORD']):
                stats.append('green')
                stats.append(0)
                counterS += 1
            else:
                stats.append('red')
                stats.append(30)
        for x in computerUpQ:
            if check_computers.ping_computer('osiris', list(x.keys())[0]):
                stats.append('green')
                stats.append(0)
                counterC += 1
            else:
                stats.append('red')
                stats.append(30)

        if counterS == len(serverUpQ):
            stats.append('green')
            stats.append('OK')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        if counterC == len(computerUpQ):
            stats.append('green')
            stats.append('OK')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)

        return stats


outputs = []
for x in powerOutlets:
    outputs.append(Output('%s-%s-check' % (x['KEYWORD'], x['LIBRARY']), 'color'))
    outputs.append(Output('%s-%s-check' % (x['KEYWORD'], x['LIBRARY']), 'height'))

outputs.append(Output('osiris-power-check', 'color'))
outputs.append(Output('osiris-power-check', 'label'))
outputs.append(Output('osiris-power-check', 'height'))

osiris_semaphore1 = threading.Semaphore()
@app.callback(
    outputs,
    inputs_intervals
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
    with osiris_semaphore1:
        stats = []
        counter = 0
        for x in powerOutlets:
            if check_power.get_keyword(x['LIBRARY'], x['KEYWORD']) == x['GOODVALUE']:
                stats.append('green')
                stats.append(0)
                counter += 1
            else:
                stats.append('red')
                stats.append(30)

        if counter == len(powerOutlets):
            stats.append('green')
            stats.append('OK')
            stats.append(0)
        else:
            stats.append('red')
            stats.append('ERROR')
            stats.append(50)
        return stats


outputs = []
for x in settingsCheckQ:
    outputs.append(Output('%s-%s-check' % (x['KEYWORD'], x['LIBRARY']), 'color'))
    outputs.append(Output('%s-%s-check' % (x['KEYWORD'], x['LIBRARY']), 'height'))

outputs.append(Output('osiris-settings-check', 'color'))
outputs.append(Output('osiris-settings-check', 'label'))
outputs.append(Output('osiris-settings-check', 'height'))

osiris_semaphore2 = threading.Semaphore()
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
    with osiris_semaphore2:
        stats = []
        counterGreen = 0
        counterYellow = 0
        print('started osiris settings')
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
                if not isinstance(keyword['MINVALUE'], int):
                    stats.append('red')
                    stats.append(30)
                elif keyword['MINVALUE'] <= float(check_settings.get_keyword(keyword['LIBRARY'], keyword['KEYWORD'])) <= keyword['MAXVALUE']:
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
        print('ended osiris settings')
        return stats

outputs = [
Output('osiris-temperatures-current', 'children'),
Output('osiris-temperatures-normal', 'children'),
Output('osiris-temperatures-current1', 'children'),
Output('osiris-temperatures-normal1', 'children'),
Output('osiris-pressure-current', 'children'),
Output('osiris-pressure-normal', 'children'),
Output('osiris-tab1', 'disabled'),
Output('osiris-tab2', 'disabled')
]
osiris_semaphore3 = threading.Semaphore()
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
    with osiris_semaphore3:
        stats = []
        current = [html.H4('Current')]
        normal = [html.H4('Normal')]
        current1 = [html.H4('Current')]
        normal1 = [html.H4('Normal')]
        counter = 0
        for x in tempCheckQ:
            x['CURRENT'] = str(check_temperature.get_keyword(x['LIBRARY'], x['KEYWORD']))
            newKey = x['KEYWORD'][:-1] + 'rng' + x['KEYWORD'][-1]
            x['NORMAL'] = str(check_temperature.get_keyword(x['LIBRARY'], newKey))
            if counter < 8:
                current.append(html.P(x['CURRENT']))
                normal.append(html.P(x['NORMAL']))
            else:
                current1.append(html.P(x['CURRENT']))
                normal1.append(html.P(x['NORMAL']))
            counter += 1
        stats.append(current)
        stats.append(normal)
        stats.append(current1)
        stats.append(normal1)
        current = [html.H4('Current'),html.Br()]
        normal = [html.H4('Normal'),html.Br()]
        current.append(str(check_pressure.get_keyword(pressureCheckQ['LIBRARY'], pressureCheckQ['KEYWORD'])))
        normal.append(str(check_pressure.get_keyword(pressureCheckQ['LIBRARY'], 'pressrng')))
        stats.append(current)
        stats.append(normal)
        stats.append(False)
        stats.append(False)
        return stats
