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
from StopLossLogic import DynamicStopLoss


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
                html.Div(id='DoubleAverageContainer3'),
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
     Output("DoubleAverageContainer2","children"),
     Output("DoubleAverageContainer3","children")],
    [Input('MAStrategyButton','n_clicks')],
    [State("MAStrategyTypeDown","value"),
     State("DBPositionControl","value"),
     State("DShortMA","value"),
     State("DLongMA","value"),
     State("OperationType","value")]
)
def MainGraphPlot(n_clicks,MAType,PositionControlName,DShortMA,DLongMA,OperationType):

    result = r.get("LossControl")
    print('****************************************')
    print(result)

    windowList = [DShortMA,DLongMA]

    data,date_list = GetData()

    if data is None:
        return 0

    #获取估值要素的动态比例
    data,PercentageName = GetPercentage(PositionControlName,data)

    # print(data)

    Average,MAtitleName = DealMovingAverage(data=data,MAtype=MAType,windowList=windowList)

    if PercentageName is not None:
        Average[PositionControlName] = data[PositionControlName]
        Average[PercentageName] = data[PercentageName]

    VolatilityData = CalVolatility(Average, "ATR")

    print(VolatilityData)

    BuyAndSellResult = BuyAndSellPoint(Average,date_list,MAtitleName)

    ResultDataFrame,OperationDataFrame = FundCurveCal(Average,date_list,BuyAndSellResult,PositionControlName,PercentageName,OperationType,VolatilityData)

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
    fig2.update(layout_xaxis_rangeslider_visible=False)
    fig2.update_layout(title="资金变化曲线")

    tableDiv1 = LayOutTemplate.GetTables(SADataFrame,'DBTable1',True,'tabelDiv1P',"策略信号运行结果")
    tableDiv2 = LayOutTemplate.GetTables(OADataFrame,'DBTable2',True,'tabelDiv2P',"策略开仓运行结果")
    tableDiv3 = LayOutTemplate.GetTables(OperationDataFrame,'DBTable3',True,"tableDiv3P","详细操作列表",)

    return fig,fig2,tableDiv1,tableDiv2,tableDiv3


# 资金曲线计算函数
def FundCurveCal(Average,date_list,BuyAndSellResult,PositionControlName,PercentageName,OperationType,VolatilityData):

    #获取主数据长度
    Average_length = len(Average)

    #获取结果数据长度
    BuyAndSellResultLength = len(BuyAndSellResult)

    #Average数据遍历器
    i = 0
    #BuyAndSellResult数据遍历器
    k = 0

    #今日估值要素
    TodayElementValuation = -1

    #资金曲线逻辑
    FundCurveTool = FM.FundCurveToolClass()
    OperationLogic = FM.OperationLogicClass()
    FundManagementTool = FM.FundManagementClass()

    #初始化资产情况
    FundManagementTool.Init()

    #双重遍历
    while i < Average_length and k < BuyAndSellResultLength:

        TodayPrice = Average.iloc[i]['close']                            #今日股价

        if PositionControlName != 'None':                               #若使用了仓位管理
            TodayElementValuation = Average.iloc[i][PercentageName]     #则今日估值要素的值

        # 计算持仓股票的涨跌幅
        FundManagementTool.UpdateIncreaseRate(TodayPrice)

        #列表
        TodayDate = date_list[i]

        AverageIndex = Average.iloc[i]['itx']                     #Average的Index
        BuyAndSellIndex = BuyAndSellResult.iloc[k]['itx']         #BuyAndSell的Index
        Signal = BuyAndSellResult.iloc[k]['BuySellLabel']         #买卖信号

        #获取动态止损信号以及动态止损价格
        DynamicStopLossSignal,DynamicStopLossPrice = DynamicStopLoss(i,FundManagementTool.PositionType,Average,VolatilityData)

        #如果触发了动态止损信号
        if DynamicStopLossSignal == 1:
            #重新核算资金
            FundManagementTool.UpdateIncreaseRate(DynamicStopLossPrice)

            #平仓逻辑
            FundManagementTool.CloseThePosition()
            if FundManagementTool.PositionType == 1:
                OperationLogic.UpdateList(TodayDate, TodayPrice, 2, "平多", FundManagementTool.CurrentProfit, AverageIndex, 0)
            else:
                OperationLogic.UpdateList(TodayDate, TodayPrice, 4, "平空", FundManagementTool.CurrentProfit, AverageIndex, 0)

        #当二者的序列号相同的时候——触发策略信号时
        if AverageIndex == BuyAndSellIndex:

            #出现金叉信号，将仓位持有信号切换为多头仓位，同时更新持仓成本
            if Signal == 1:

                #平空仓逻辑
                if FundManagementTool.PositionType == -1:
                    FundManagementTool.CloseThePosition()           #平仓逻辑
                    OperationLogic.UpdateList(TodayDate,TodayPrice,4,"平空",FundManagementTool.CurrentProfit,AverageIndex,0)

                #开多仓
                PositionPercent = FundManagementTool.OpenThePosition(TodayPrice,1,PositionControlName,TodayElementValuation)
                #更新列表
                OperationLogic.UpdateList(TodayDate, FundManagementTool.PositionHoldingCostPrice, 1, "开多", 0, AverageIndex,PositionPercent)

            #出现死叉信号，将仓位持有信号切换为空头仓位，同时更新持仓成本
            if Signal == 2:

                # 平多仓逻辑(1修改持仓成本，2.更新操作逻辑列表，3.修改持仓类型)
                if FundManagementTool.PositionType == 1:
                    FundManagementTool.CloseThePosition()
                    OperationLogic.UpdateList(TodayDate, TodayPrice, 2, "平多", FundManagementTool.CurrentProfit, AverageIndex,0)

                #仅在允许做空时
                if OperationType == 'LongAndShort':
                    #开空仓
                    PositionPercent = FundManagementTool.OpenThePosition(TodayPrice,-1,PositionControlName,TodayElementValuation)                                                     # 闲置资金 = 总资产 - 投资仓位
                    #更新列表
                    OperationLogic.UpdateList(TodayDate, FundManagementTool.PositionHoldingCostPrice, 3, "开空", 0, AverageIndex,PositionPercent)

            k = k + 1

        #计算持仓资产收益情况(针对当日调仓进行补丁)
        if FundManagementTool.PositionType == 0:        #空仓时，没有收益
            PositionInterest = 0
        else:                        #否则计算收益
            PositionInterest = ((TodayPrice - FundManagementTool.PositionHoldingCostPrice) * FundManagementTool.PositionType) / FundManagementTool.PositionHoldingCostPrice

        # 更新资金列表
        FundCurveTool.UpdateList(TodayDate,AverageIndex,TodayPrice,PositionInterest,FundManagementTool)

        i = i + 1

    ResultDataFrame = FundCurveTool.ToDataFrame()
    OperationDataFrame = OperationLogic.ToDataFrame()

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
        index = Average.iloc[j].itx

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

    return ResultDataFrame

def GetRows(PositionControlName):

    if PositionControlName is None:
        return 1
    else:
        return 2