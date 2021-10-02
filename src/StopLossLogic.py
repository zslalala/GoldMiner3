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
from VolatilityIndex import CalVolatility

#处理止损,返回两个值，第一个值0代表无需止损，返回1代表需要止损，第二个值代表止损价格
def DynamicStopLoss(index,PositionType,Average,VolatilityData):

    #空仓返回0
    if PositionType == 0:
        return 0,0

    StopLossType = r.get("LossControl")

    if StopLossType == "ATR":
        return ATRStopLoss(index,PositionType,Average,VolatilityData)

#ATR移动止损
def ATRStopLoss(index,PositionType,Average,VolatilityData):

    ClosePrice = Average.iloc[index].close
    LowPrice = Average.iloc[index].low
    HighPrice = Average.iloc[index].low

    #中心线
    CenterLine = VolatilityData.iloc[index].CenterLine

    ATRValue = VolatilityData.iloc[index].ATR                     #ATR值
    ATRMultiple = int(r.get("ATRMultiple"))                       #ATR倍数
    ATRUpperChannel = CenterLine + ATRMultiple * ATRValue         #ATR通道上通道
    ATRLowerChannel = CenterLine - ATRMultiple * ATRValue         #ATR通道下通道

    if PositionType == 1 and ClosePrice < ATRLowerChannel:        #多头仓位，破下轨止损
        return 1,ClosePrice
    if PositionType == -1 and ClosePrice > ATRUpperChannel:       #空头仓位，破上轨止损
        return 1,ClosePrice

    #正常情况，返回0,0
    return 0,0
