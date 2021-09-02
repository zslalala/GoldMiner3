from __future__ import print_function, absolute_import
from dash.dependencies import Input, Output, State
from MultiMovingAverageLine import DealMovingAverage
import dash_html_components as html
import dash_core_components as dcc
from Server import app
from DashMainPagePlot import GetData


#均线策略下滑框选择
@app.callback(
    Output("AverageContainer","children"),
    Input("MAStrategyDown","value"),
)
def MASDynamicChoice(text):

    #双均线策略
    if text == 'DoubleAverage':
        return html.Div(
            [
                dcc.Input(id = "DShortMA",value=20,type='number'),
                dcc.Input(id = 'DLongMA',value=60,type='number'),
                html.Br(),
                html.Button('查询', id='DAverageButton', n_clicks=0),
                dcc.Graph(id="MAStrategyGraph"),
            ]
        )

    #三均线策略
    if text == 'ThripleAverage':
        return html.Div(
            [
                dcc.Input(id="TShortMA", value=5, type='number'),
                dcc.Input(id="TMiddleMA", value=20, type='number'),
                dcc.Input(id='TLongMA', value=60, type='number'),
            ]
        )


@app.callback(
    Output("TestMultiFileP","children"),
    Input("TShortMA","value")
)
def GetTshortMa(value):
    return "TshortMa is {}".format(value)



@app.callback(
    Output("my-div","children"),
    Input("ValueEvaluation", "value")
)
def TestMultiFile(text):

    data = GetData()

    if data is None:
        return "No Data"
    else:
        print(data)
        return text + "300"