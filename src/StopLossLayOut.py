from __future__ import print_function, absolute_import

import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table
from MultiMovingAverageLineDash import DealMovingAverage
import dash_html_components as html
import dash_core_components as dcc
from Server import app
from DashMainPagePlot import GetData
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import FundManagement as FM
import LayOutTemplate
from PositionControl import GetPercentage,GetPositionByPETTM
from Start import r
from VolatilityIndex import GetATR


#止损下滑框触发
@app.callback(
    Output("StopLossContainer","children"),
    Input("LossControl","value"),
)
def MASDynamicChoice(text):

    #ATR止损策略
    if text == 'ATR':
        r.set("LossControl","ATR")
        return html.Div(
            [
                html.P(children="中心环绕均线类型"),
                dcc.Dropdown(id='ATRAverageType',
                             options=[
                                 {'label': 'SMA', 'value': 'SMA'},
                                 {'label': 'EMA', 'value': 'EMA'},
                                 {'label': 'WMA', 'value': 'WMA'},
                                 {'label': 'HMA', 'value': 'HMA'},
                             ],
                             value='EMA'
                             ),
                dcc.Input(id = "ATRAverageLineWS",value=20,type='number'),
                dcc.Input(id = 'ATRWS',value=14,type='number'),
                dcc.Input(id = 'ATRMultiple',value=2,type='number'),
                html.Button('设置ATR参数', id='ATRConfirmButton', n_clicks=0),
                html.P(id="ATRP"),
                html.Br(),
            ]
        )
    else:
        r.set("LossControl","None")

#ATR参数入缓存
@app.callback(
    Output("ATRP", "children"),
    [Input('ATRConfirmButton','n_clicks')],
    [State("ATRAverageType","value"),
     State("ATRAverageLineWS","value"),
     State("ATRMultiple","value"),
     State("ATRWS","value")]
)
def SetATR(n_clicks,ATRAverageType,ATRAverageLineWS,ATRMultiple,ATRWS):
    r.set("ATRAverageType",ATRAverageType)
    r.set("ATRAverageLineWS",ATRAverageLineWS)
    r.set("ATRMultiple",ATRMultiple)
    r.set("ATRWS",ATRWS)
    OutStr = "中心线类型为:"+ATRAverageType+"  中心均线时间周期为:"+str(ATRAverageLineWS) + "  ATR波动统计时间窗口为:"+str(ATRWS) + "  ATR倍数为:"+str(ATRMultiple)
    return OutStr