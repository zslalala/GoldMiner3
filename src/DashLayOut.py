import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from Server import app,server
import DashMainPagePlot                 #一定要导入，不要乱删
import MovingAverageStrategy            #一定要导入，不要乱删
import StopLossLayOut                   #一定要导入，不要乱删

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
        html.Div(id='my-div'),


        html.Br(),
        GetAverageStrategy(),

    ])

    return OverAllLayOut


#代码、日期布局
def GetStockIdLayOut():

    StockIdLayOut = html.Div([
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("股票代码",addon_type="prepend"),
                dcc.Input(id="StockIdInput", value='SHSE.600000', type='text',style = {'width':'10%'})
            ],
        ),
        dbc.Form(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("开始日期", addon_type="prepend"),
                        dcc.Input(id="StartTime", value='2010-01-01', type='text'),
                    ]
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("终止日期", addon_type="prepend"),
                        dcc.Input(id="EndTime", value='2021-08-31', type='text'),
                    ]
                ),
            ],
            inline=True
        ),
        html.Br(),
        dbc.Button('查询', id='StockIdButton',color="info", className="mr-1", n_clicks=0),
        html.P(id='StockP')
    ])

    return StockIdLayOut

#均线系统布局
def GetMALayOut():

    MALayOut = html.Div([
        html.P(id="MATypeP", children="均线类型"),
        dbc.Select(
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
        dbc.Button('Submit', id='MAButton',color="info", className="mr-1", n_clicks=0)
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

#均线策略界面
def GetAverageStrategy():

    AverageStrategyLayOut = html.Div([

        html.P(id = 'MAStrategyP',children = 'MovingAverageStrategy'),

        html.P(children="均线类型"),
        dcc.Dropdown(id='MAStrategyTypeDown',
            options=[
                {'label': 'SMA', 'value': 'SMA'},
                {'label': 'EMA', 'value': 'EMA'},
                {'label': 'WMA', 'value': 'WMA'},
                {'label': 'HMA', 'value': 'HMA'},
            ],
            value = 'SMA'
        ),

        html.P(children="仓位管理策略"),
        dcc.Dropdown(id='DBPositionControl',
                     options=[
                         {'label': 'None', 'value': 'None'},
                         {'label': 'PETTM', 'value': 'PETTM'},
                     ],
                     value='PETTM'),

        html.P(children="策略类型"),
        dcc.Dropdown(id='MAStrategyDown',
            options=[
                {'label': 'DoubleAverage', 'value': 'DoubleAverage'},
                {'label': 'ThripleAverage', 'value': 'ThripleAverage'},
            ],
            value='DoubleAverage'
        ),

        html.P(children="操作类型"),
        dcc.Dropdown(id='OperationType',
            options=[
                {'label': 'OnlyLong(仅做多)','value':'OnlyLong'},
                {'label': 'LongAndShort(做多和做空均可)', 'value': 'LongAndShort'}
            ],
            value='OnlyLong'
        ),

        html.P(children="止损策略"),
        dcc.Dropdown(id="LossControl",
                     options=[
                {'label': 'None(无止损)','value':'None'},
                {'label': 'ATR', 'value': 'ATR'}
            ],
            value='ATR'),
        html.Div(id = 'StopLossContainer'),

        html.Br(),
        html.Div(id = 'AverageContainer'),
        html.P(id = "TestMultiFileP"),
    ])

    return AverageStrategyLayOut


#布局信息
app.layout = GetOverAllLayOut()