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
from PositionControl import GetPercentage,GetPositionByPETTM
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
                html.Div(id='DoubleAverageContainer1'),
                html.Div(id='DoubleAverageContainer2'),
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
    [Output("MADShownStrategyGraph", "figure"),
     Output("MADProfitStrateGraph","figure"),
     Output("DoubleAverageContainer1","children"),
     Output("DoubleAverageContainer2","children")],
    [Input('MAStrategyButton','n_clicks')],
    [State("MAStrategyTypeDown","value"),
     State("DBPositionControl","value"),
     State("DShortMA","value"),
     State("DLongMA","value"),
     State("OperationType","value")]
)
def MainGraphPlot(n_clicks,MAType,PositionControlName,DShortMA,DLongMA,OperationType):

    windowList = [DShortMA,DLongMA]

    data,date_list = GetData()

    if data is None:
        return 0

    #获取估值要素的动态比例
    data,PercentageName = GetPercentage(PositionControlName,data)

    print(data)

    Average,MAtitleName = DealMovingAverage(data=data,MAtype=MAType,windowList=windowList)

    if PercentageName is not None:
        Average[PositionControlName] = data[PositionControlName]
        Average[PercentageName] = data[PercentageName]

    print(Average)

    BuyAndSellResult = BuyAndSellPoint(Average,date_list,MAtitleName)

    ResultDataFrame,OperationDataFrame = FundCurveCal(Average,date_list,BuyAndSellResult,PositionControlName,PercentageName,OperationType)

    Ana = FM.ResultAnalysisClass(OperationDataFrame)

    SignalAnalysisDict,OpeningAnalysisDict = Ana.SignalAndOpeningAnalysis()

    SADataFrame = pd.DataFrame.from_dict(SignalAnalysisDict,orient='index').T
    OADataFrame = pd.DataFrame.from_dict(OpeningAnalysisDict,orient='index').T

    rowNumber = GetRows(PositionControlName)

    #均线图绘制函数
    fig = make_subplots(rows=rowNumber, cols=1,subplot_titles=('StockPrice', PercentageName),shared_xaxes=True)
    #均线绘制
    for i in MAtitleName:
        fig.add_trace(
            go.Scatter(
                x=Average.itx,
                y=Average[i],
                name=i,
                hovertext=date_list,
            ), row=1, col=1)

    #图上标注买卖点
    fig.add_trace(go.Scatter(x = BuyAndSellResult.itx,y = BuyAndSellResult.close,
                             marker=dict(
                                 color = BuyAndSellResult.BuySellLabel - 1,
                                 colorscale=[[0, 'green'], [1, 'red']]
                             ),
                             name = 'Signal',mode = 'markers'),row = 1,col = 1)

    #如果有估值要素，应给出估值要素的曲线变化
    if PercentageName is not None:
        fig.add_trace(go.Scatter(x = Average.itx,y = Average[PercentageName],hovertext=Average[PositionControlName],name=PercentageName),row=2,col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(title = "双均线策略买卖点")

    #资金图绘制函数
    fig2 = make_subplots(rows=1, cols=1,
                        subplot_titles=('FundChange'))

    fig2.add_trace(go.Scatter(x=ResultDataFrame.itx, y=ResultDataFrame.TotalFund, name='Fund'), row=1,
                  col=1)

    fig2.add_trace(go.Scatter(x=ResultDataFrame.itx, y=ResultDataFrame.AssetsFund,name='AssetPosition'),row=1,col=1)

    # fig2.add_trace(go.Scatter(x=ResultDataFrame.itx, y=ResultDataFrame.AssetsFund / ResultDataFrame.TotalFund,name='Percent'),
    #                row=1,col=1)

    fig2.update(layout_xaxis_rangeslider_visible=False)
    fig2.update_layout(title="资金变化曲线")

    tableDiv1 = html.Div(
        [html.P(id="tableDiv1PSignal", children="策略信号运行结果"),
         dash_table.DataTable(
             id='DBTable1',
             columns=[{"name": i, "id": i} for i in SADataFrame.columns],
             data=SADataFrame.to_dict('records'),
         ),
         html.P(id="tableDiv1POpening", children="策略开仓运行结果"),
         dash_table.DataTable(
             id='DBTable1',
             columns=[{"name": i, "id": i} for i in OADataFrame.columns],
             data=OADataFrame.to_dict('records'),
         )
         ]
    )

    tableDiv2 = html.Div(
        [html.P(id = "tableDiv2P",children="详细操作列表"),
        dash_table.DataTable(
            id='DBTable2',
            columns=[{"name": i, "id": i} for i in OperationDataFrame.columns],
            data=OperationDataFrame.to_dict('records'),
        )]
    )

    return fig,fig2,tableDiv1,tableDiv2


# 资金曲线计算函数
def FundCurveCal(Average,date_list,BuyAndSellResult,PositionControlName,PercentageName,OperationType):

    # 开仓情况，0代表未持有任何仓位，1代表持有多头仓位，-1代表持有空头仓位
    PositionType = 0

    #获取主数据长度
    Average_length = len(Average)

    #获取结果数据长度
    BuyAndSellResultLength = len(BuyAndSellResult)

    #持有仓位的成本价
    PositionHoldingCostPrice = -1

    #Average数据遍历器
    i = 0
    #BuyAndSellResult数据遍历器
    k = 0

    #总资产
    TotalFund = 1

    #本次操作投入资产
    AssetsInvestedFund = 0

    #持仓资产
    AssetsPositionFund = 0

    #今日估值要素
    TodayElementValuation = -1

    #闲置资金
    IdleFund = 1

    #资金曲线逻辑
    FundManageMent = FM.FundCurveClass()
    OperationLogic = FM.OperationLogicClass()

    #双重遍历
    while i < Average_length and k < BuyAndSellResultLength:

        TodayPrice = Average.iloc[i]['close']                            #今日股价

        if PositionControlName != 'None':                               #若使用了仓位管理
            TodayElementValuation = Average.iloc[i][PercentageName]     #则今日估值要素的值

        # 计算持仓股票的涨跌幅
        if PositionType == 0:
            IncreaseRate = 0
        else:
            IncreaseRate = (TodayPrice - PositionHoldingCostPrice) / PositionHoldingCostPrice

        #本次开仓盈利情况
        CurrentProfit = IncreaseRate * PositionType

        #持仓资金数
        AssetsPositionFund = AssetsInvestedFund * (1 + CurrentProfit)

        #总资金曲线变化
        TotalFund = IdleFund + AssetsPositionFund

        #列表
        TodayDate = date_list[i]

        AverageIndex = Average.iloc[i]['itx']                     #Average的Index
        BuyAndSellIndex = BuyAndSellResult.iloc[k]['itx']         #BuyAndSell的Index
        Signal = BuyAndSellResult.iloc[k]['BuySellLabel']         #买卖信号

        #当二者的序列号相同的时候
        if AverageIndex == BuyAndSellIndex:

            #出现金叉信号，将仓位持有信号切换为多头仓位，同时更新持仓成本
            if Signal == 1:

                #平空仓逻辑(1.修改持仓成本，2.修改闲置资金，持仓资产，持仓初始投资成本，总资本 3.更新操作逻辑列表，4.修改持仓类型)
                if PositionType == -1:
                    PositionHoldingCostPrice = 0                       # 修改持仓资本为0
                    IdleFund = AssetsPositionFund + IdleFund           # 闲置资金设置为原闲置资金 + 原资产市场价值
                    AssetsPositionFund = 0                             # 原资产市场价值设置为0
                    AssetsInvestedFund = 0                             # 原资产成本价值设置为0
                    TotalFund = IdleFund                               # 总资产设置为平仓后的闲置资金
                    OperationLogic.UpdateList(TodayDate,TodayPrice,4,"平空",CurrentProfit,AverageIndex,0)
                    PositionType = 0

                #开多仓逻辑(1.修改持仓成本，2.更新操作逻辑列表，3.修改持仓类型)
                PositionHoldingCostPrice = TodayPrice
                PositionType = 1

                #仓位控制逻辑（1.计算仓位百分比，2.设定实时资产数额，3.计算闲置资金）
                PositionPercent = GetPositionByPETTM(PositionControlName,TodayElementValuation,1)
                AssetsInvestedFund = TotalFund * PositionPercent                    # 计算仓位
                AssetsPositionFund = AssetsInvestedFund                             # 设定实时资产数额
                IdleFund = TotalFund - AssetsPositionFund                           # 闲置资金 = 总资产 - 投资仓位

                #更新列表
                OperationLogic.UpdateList(TodayDate, PositionHoldingCostPrice, 1, "开多", 0, AverageIndex,PositionPercent)

            #出现死叉信号，将仓位持有信号切换为空头仓位，同时更新持仓成本
            if Signal == 2:

                # 平多仓逻辑(1修改持仓成本，2.更新操作逻辑列表，3.修改持仓类型)
                if PositionType == 1:
                    PositionHoldingCostPrice = 0                        # 修改持仓资本为0
                    IdleFund = AssetsPositionFund + IdleFund            # 闲置资金设置为原闲置资金 + 原资产市场价值
                    AssetsPositionFund = 0                              # 原资产市场价值设置为0
                    AssetsInvestedFund = 0                              # 原资产成本价值设置为0
                    TotalFund = IdleFund                                # 总资产设置为平仓后的闲置资金
                    OperationLogic.UpdateList(TodayDate, TodayPrice, 2, "平多", CurrentProfit, AverageIndex,0)
                    PositionType = 0

                #仅在允许做空时
                if OperationType == 'LongAndShort':

                    # 开空仓逻辑(1.修改持仓成本，2.更新操作逻辑列表，3.修改持仓类型)
                    PositionHoldingCostPrice = TodayPrice
                    PositionType = -1

                    # 仓位控制逻辑（1.计算仓位，2.设定实时资产数额，3.计算闲置资金）
                    PositionPercent = GetPositionByPETTM(PositionControlName,TodayElementValuation,-1)             # 计算仓位
                    AssetsInvestedFund = TotalFund * PositionPercent
                    AssetsPositionFund = AssetsInvestedFund                                                        # 设定实时资产数额
                    IdleFund = TotalFund - AssetsPositionFund                                                      # 闲置资金 = 总资产 - 投资仓位

                    OperationLogic.UpdateList(TodayDate, PositionHoldingCostPrice, 3, "开空", 0, AverageIndex,PositionPercent)

            k = k + 1

        #计算持仓资产收益情况(针对当日调仓进行补丁)
        if PositionType == 0:        #空仓时，没有收益
            PositionInterest = 0
        else:                        #否则计算收益
            PositionInterest = ((TodayPrice - PositionHoldingCostPrice) * PositionType) / PositionHoldingCostPrice

        # 更新资金列表
        FundManageMent.UpdateList(TodayDate,AverageIndex,TodayPrice,PositionHoldingCostPrice,PositionType,AssetsPositionFund,PositionInterest,
                                  IdleFund,TotalFund,TotalFund - 1)

        i = i + 1

    ResultDataFrame = FundManageMent.ToDataFrame()
    OperationDataFrame = OperationLogic.ToDataFrame()
    print(ResultDataFrame)
    print(OperationDataFrame)

    return ResultDataFrame,OperationDataFrame

# 策略特性计算函数
def StrategyPropertiesComput():

    return 0



# 双均线策略执行函数
# 返回类型DataFrame
# 包含列名[date,itx,close,BuySellLabel,BuySellInfo]
def BuyAndSellPoint(Average, date_list, MAtitleName):

    data_length = len(Average)

    # 获取均线名字
    ShortMAName = MAtitleName[0]
    LongMAName = MAtitleName[1]
    CloseName = 'close'

    # 设置列表
    DoDate = []
    DoIndex = []
    BuySellList = []
    BuySellInfo = []
    CloseList = []

    # T日迭代器
    i = 0

    while i < data_length - 1:

        # T+1日迭代器
        j = i + 1

        # T日价格
        T0ShortMAPrice = Average.iloc[i][ShortMAName]
        T0LongMAPrice = Average.iloc[i][LongMAName]

        # T+1日价格
        T1ShortMAPrice = Average.iloc[j][ShortMAName]
        T1LongMAPrice = Average.iloc[j][LongMAName]

        ClosePrice = Average.iloc[j][CloseName]

        # 用来画图的index
        index = Average.iloc[j][0]

        # 当日date
        TodayDate = date_list[j]

        # 金叉状态
        if T1ShortMAPrice >= T1LongMAPrice and T0ShortMAPrice <= T0LongMAPrice:
            BuySellInfo.append("金叉")
            BuySellList.append(1)
            DoDate.append(TodayDate)
            DoIndex.append(index)
            CloseList.append(ClosePrice)

        # 死叉状态
        if T1ShortMAPrice <= T1LongMAPrice and T0ShortMAPrice >= T0LongMAPrice:
            BuySellInfo.append("死叉")
            BuySellList.append(2)
            DoDate.append(TodayDate)
            DoIndex.append(index)
            CloseList.append(ClosePrice)

        i = i + 1

    ResultDict = {
        "date": DoDate,
        "itx": DoIndex,
        "close": CloseList,
        "BuySellLabel": BuySellList,
        "BuySellInfo": BuySellInfo,
    }

    ResultDataFrame = pd.DataFrame(ResultDict)

    print(ResultDataFrame)

    return ResultDataFrame

def GetRows(PositionControlName):

    if PositionControlName is None:
        return 1
    else:
        return 2

#测试函数
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