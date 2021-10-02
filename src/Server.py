from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

#服务器设置
server = Flask('myproject')
app = Dash(server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])