from __future__ import print_function, absolute_import
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from MultiMovingAverageLine import DealMovingAverage
from Server import app


@app.callback(
    Output("my-div","children"),
    Input("ValueEvaluation", "value")
)
def TestMultiFile(text):

    print(text)

    # data = GetData()

    # print(data)

    return text + "300"