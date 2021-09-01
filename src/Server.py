from flask import Flask
from dash import Dash

#服务器设置
server = Flask('myproject')
app = Dash(server=server)