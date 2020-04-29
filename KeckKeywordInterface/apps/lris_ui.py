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


layout = html.Div([
    html.H1('THIS PAGE IS NOT READY!'),
    dcc.Link('Go to Welcome Page', href='/')
])
