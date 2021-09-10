from __future__ import print_function, absolute_import
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from MultiMovingAverageLineDash import DealMovingAverage
from DataProcess import StaffAnalysis,PEAnalysis
import plotly

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from Server import app

#设置个人用户的tokenID
set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')

# global data
# global date_list

#主数据获取函数
@app.callback(
    Output("StockP","children"),
    Input("StockIdButton","n_clicks"),
    [State("StockIdInput","value"),
     State("StartTime","value"),
     State("EndTime","value")]
)
def DataAcquire(n_clicks,StockId,StartTime,EndTime):

    if len(StockId) < 11:
        return "WrongID"

    price_Data = history(symbol=StockId, frequency='1d', start_time=StartTime, end_time=EndTime,
                         fields='open,high,low,close,eob', df=True, adjust=ADJUST_PREV)

    fundamental_Data = get_fundamentals(table='trading_derivative_indicator', symbols=StockId, start_date=StartTime,
                                        end_date=EndTime, fields='PETTM', limit=10000, df=True)

    price_Data, fundamental_Data = DataPreprocess(price_Data, Stock=True, fundamental_Data=fundamental_Data)

    #定义全局变量data
    global data
    data = pd.merge(price_Data,fundamental_Data,left_index=True,right_index=True)

    #定义全局变量date_list
    global date_list
    date_list= data.index.values.tolist()

    return "StockId is {},StartDate is {},End Date is {}".format(StockId, StartTime, EndTime)


#主图绘制函数
@app.callback(
    Output("graph", "figure"),
    [Input("StockP", "children"),
     Input('ValueEvaluation','value'),
     Input('MAButton','n_clicks')],
    [State("MATypeDrop","value"),
     State("Timing01","value"),
     State("Timing02","value"),
     State("Timing03","value"),
     State("Timing04","value"),]
)
def MainGraphPlot(text,valueText,n_clicks,MAType,Timing01,Timing02,Timing03,Timing04):

    windowList = [Timing01,Timing02,Timing03,Timing04]

    CData,CData_list = GetData()

    if CData is None:
        return 0

    Average,MAtitleName = DealMovingAverage(data=CData,MAtype=MAType,windowList=windowList)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        subplot_titles=('StockPrice', valueText), row_width=[0.2, 0.7])

    fig.add_trace(go.Candlestick(x=CData.itx,
                                 open=CData.open, high=CData.high,
                                 low=CData.low, close=CData.close, increasing_line_color='#f6416c',
                                 decreasing_line_color='#7bc0a3', name="Price",
                                 hovertext=CData_list,
                                 ), row=1, col=1)

    for i in MAtitleName:
        fig.add_trace(
            go.Scatter(
                x=Average.itx,
                y=Average[i],
                name=i,
            ), row=1, col=1)

    fig.add_trace(go.Scatter(x=data.itx, y=data.PETTM, name=valueText, showlegend=True), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig

#主数据传输函数
def GetData():

    try:
        print(data)
    except:
        return None,None
    else:
        return data,date_list