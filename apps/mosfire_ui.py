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

mosfireKeywords = Keywords()

layout = html.Div([
    html.H1('THIS PAGE IS NOT READY!'),
    dcc.Link('Go to Welcome Page', href='/')
])
