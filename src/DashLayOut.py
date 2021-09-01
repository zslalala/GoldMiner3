import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#总布局
def GetOverAllLayOut():

    OverAllLayOut = html.Div([

        # 代码、日期页面布局
        GetStockIdLayOut(),

        # 均线系统页面布局
        GetMALayOut(),

        # 获取估值数据
        GetValuationLayOut(),

        dcc.Graph(id="graph"),
        dcc.Input(id='my-id', value='initial value', type='text'),
        html.Div(id='my-div')
    ])

    return OverAllLayOut


#代码、日期布局
def GetStockIdLayOut():

    StockIdLayOut = html.Div([
        dcc.Input(id="StockIdInput", value='SHSE.600000', type='text'),
        dcc.Input(id="StartTime", value='2014-01-01', type='text'),
        dcc.Input(id="EndTime", value='2021-08-31', type='text'),
        html.Br(),
        html.Button('查询', id='StockIdButton', n_clicks=0),
        html.P(id='StockP')
    ])

    return StockIdLayOut

#均线系统布局
def GetMALayOut():

    MALayOut = html.Div([
        html.P(id="MATypeP", children="均线类型"),
        dcc.Dropdown(
            id='MATypeDrop',
            options=[
                {'label': 'SMA', 'value': 'SMA'},
                {'label': 'EMA', 'value': 'EMA'},
                {'label': 'WMA', 'value': 'WMA'},
                {'label': 'HMA', 'value': 'HMA'},
            ],
            value='SMA',
        ),
        dcc.Input(id='Timing01', value=5, type='number'),
        dcc.Input(id='Timing02', value=20, type='number'),
        dcc.Input(id='Timing03', value=60, type='number'),
        dcc.Input(id='Timing04', value=120, type='number'),
        html.Br(),
        html.Button('Submit', id='MAButton', n_clicks=0)
    ])

    return MALayOut

#获取估值信息
def GetValuationLayOut():

    ValuationLayOut = html.Div([
        html.P(id="ValueP", children='Method Of Valuation'),
        dcc.Dropdown(
            id='ValueEvaluation',
            options=[
                {'label': 'PETTM', 'value': 'PETTM'},
                {'label': 'PBTTM', 'value': 'PBTTM'},
            ],
            value='PETTM'
        )
    ])

    return ValuationLayOut