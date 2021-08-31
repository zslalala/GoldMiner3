from __future__ import print_function, absolute_import
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from DataProcess import StaffAnalysis,PEAnalysis
import plotly

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from HigherDraw import HigherDrawing
from PlotlyDraw import ETFPlotDrawing

#设置个人用户的tokenID
set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')

app = dash.Dash(__name__)

#布局信息
app.layout = html.Div([
    dcc.Input(id = "StockIdInput", value = 'SHSE.600000',type='text'),
    dcc.Input(id = "StartTime",value = '2014-01-01',type = 'text'),
    dcc.Input(id = "EndTime",value = '2021-08-31',type = 'text'),

    html.P(id = 'StockIdP'),

    html.Div([
        html.P(id = "ValueP",children='Method Of Valuation'),
        dcc.Dropdown(
            id = 'ValueEvaluation',
            options=[
                {'label':'PE','value':'PEvalue'},
                {'label':'PB','value':'PBvalue'}
            ],
            value='PEvalue'
        )
    ]),

    dcc.Graph(id="graph"),
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])


@app.callback(
    Output("StockIdP","children"),
    [Input("StockIdInput","value"),
     Input("StartTime","value"),
     Input("EndTime","value")]
)
def MainDataAcquire(StockId,StartTime,EndTime):

    if len(StockId) < 11:
        return "WrongID"

    price_Data = history(symbol=StockId, frequency='1d', start_time=StartTime, end_time=EndTime,
                         fields='open,high,low,close,eob', df=True)

    fundamental_Data = get_fundamentals(table='trading_derivative_indicator', symbols=StockId, start_date=StartTime,
                                        end_date=EndTime, fields='PETTM', limit=10000, df=True)

    price_Data, fundamental_Data = DataPreprocess(price_Data, Stock=True, fundamental_Data=fundamental_Data)

    #定义全局变量data
    global data
    data = pd.merge(price_Data,fundamental_Data,left_index=True,right_index=True)

    #定义全局变量date_list
    global date_list
    date_list= data.index.values.tolist()

    return "StockId is {},StartDate is {},End Date is {}".format(StockId,StartTime,EndTime)

@app.callback(
    Output("graph", "figure"),
    [Input("StockIdP", "children"),
     Input('ValueEvaluation','value')])
def MainGraphPlot(text,valueText):

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        subplot_titles=('StockPrice', 'PETTM'), row_width=[0.2, 0.7])

    fig.add_trace(go.Candlestick(x=data.itx,
                                 open=data.open, high=data.high,
                                 low=data.low, close=data.close, increasing_line_color='#f6416c',
                                 decreasing_line_color='#7bc0a3', name="Price",
                                 hovertext=date_list,
                                 ), row=1, col=1)

    fig.add_trace(go.Scatter(x=data.itx, y=data.PETTM, name='PETTM', showlegend=True), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig

if __name__ == '__main__':
    app.run_server()