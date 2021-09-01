from __future__ import print_function, absolute_import
from dash.dependencies import Input, Output, State
from MultiMovingAverageLine import DealMovingAverage
from Server import app
from DashMainPagePlot import GetData


@app.callback(
    Output("my-div","children"),
    Input("ValueEvaluation", "value")
)
def TestMultiFile(text):

    print(text)

    data = GetData()

    print(data)

    return text + "300"