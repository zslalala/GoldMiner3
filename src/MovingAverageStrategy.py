from __future__ import print_function, absolute_import
from dash.dependencies import Input, Output, State
from MultiMovingAverageLineDash import DealMovingAverage
import dash_html_components as html
import dash_core_components as dcc
from Server import app
from DashMainPagePlot import GetData
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


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
                html.Button('查询', id='MAStrategyButton', n_clicks=0),
                html.Br(),
                dcc.Graph(id="MADShownStrategyGraph"),
                dcc.Graph(id="MADProfitStrateGraph"),
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



#双均线策略绘制函数
@app.callback(
    Output("MADShownStrategyGraph", "figure"),
    [Input('MAStrategyButton','n_clicks')],
    [State("MAStrategyTypeDown","value"),
     State("DShortMA","value"),
     State("DLongMA","value"),]
)
def MainGraphPlot(n_clicks,MAType,DShortMA,DLongMA):

    windowList = [DShortMA,DLongMA]

    data,date_list = GetData()

    if data is None:
        return 0

    Average,MAtitleName = DealMovingAverage(data=data,MAtype=MAType,windowList=windowList)

    # result = BuyAndSellPoint(Average)

    fig = make_subplots(rows=1, cols=1,
                        subplot_titles=('MADoubletrategy'))

    for i in MAtitleName:
        fig.add_trace(
            go.Scatter(
                x=Average.itx,
                y=Average[i],
                name=i,
                hovertext=date_list,
            ), row=1, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig



@app.callback(
    Output("my-div","children"),
    Input("ValueEvaluation", "value")
)
def TestMultiFile(text):

    data,date_list = GetData()

    #判断Data是否已经定义，若未定义则返回No Data，若已定义则返回所需
    if data is None:
        return "No Data"
    else:
        return text + "300"



#策略执行函数
def BuyAndSellPoint(Average):

    data_length = len(Average)

    print(data_length,"data_length")

    empty_list = []

    i = 0
    j = 1
    while j < data_length:

        print(Average.iloc[j][3])
        j = j + 1
        i = i + 1



    return Average