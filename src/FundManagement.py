import numpy as np
import pandas as pd
from PositionControl import GetPositionByPETTM

#资金管理类，用于资金逻辑的处理
class FundManagementClass:

    def __init__(self):
        self.PositionHoldingCostPrice = 0          #持仓单价成本
        self.IdleFund = 0                          #现有闲置资金
        self.AssetsPositionFund = 0                #现有资产价值
        self.AssetsInvestedFund = 0                #资产购入所花费总资金(总成本)
        self.TotalFund = 0                         #总资产
        self.PositionType = 0                      #仓位类型
        self.IncreaseRate = 0                      #开仓资产变动率
        self.CurrentProfit = 0                     #盈利率

    def Init(self):
        self.PositionHoldingCostPrice = 0          #初始持仓成本单价为0
        self.IdleFund = 1                          #初始闲置资金为1
        self.TotalFund = 1                         #初始总资金为1
        self.AssetsPositionFund = 0                #初始现有资产价值为0(空仓)
        self.AssetsInvestedFund = 0                #初始资产购入所花费总资金为0(空仓)
        self.PositionType = 0                      #仓位类型(0:空仓)
        self.IncreaseRate = 0                      #开仓资产变动率
        self.CurrentProfit = 0                     #盈利率

    #根据比较基准价格更新收益率
    def UpdateIncreaseRate(self,price):

        #先计算股票变动率
        if self.PositionType == 0:
            self.IncreaseRate = 0
        else:
            self.IncreaseRate = (price - self.PositionHoldingCostPrice) / self.PositionHoldingCostPrice

        #考虑开仓方向，计算本次开仓盈利情况
        self.CurrentProfit = self.IncreaseRate * self.PositionType

        #根据盈利情况，得到新的资产市值
        self.AssetsPositionFund = self.AssetsInvestedFund * (1 + self.CurrentProfit)

        #总资金 = 闲置资金 + 资产市值
        self.TotalFund = self.IdleFund + self.AssetsPositionFund

    def CloseThePosition(self):

        self.PositionHoldingCostPrice = 0                           # 修改持仓资本为0
        self.IdleFund = self.AssetsPositionFund + self.IdleFund     # 闲置资金设置为原闲置资金 + 原资产市场价值
        self.AssetsPositionFund = 0                                 # 原资产市场价值设置为0
        self.AssetsInvestedFund = 0                                 # 原资产成本价值设置为0
        self.TotalFund = self.IdleFund                              # 总资产设置为平仓后的闲置资金
        self.PositionType = 0                                       # 设置仓位类型为空仓

    def OpenThePosition(self,price,PositionType,PositionControlName,TodayElementValuation):

        self.PositionHoldingCostPrice = price
        self.PositionType = PositionType

        # 仓位控制逻辑（1.计算仓位百分比，2.设定实时资产数额，3.计算闲置资金）
        PositionPercent = GetPositionByPETTM(PositionControlName, TodayElementValuation, PositionType)
        self.AssetsInvestedFund = self.TotalFund * PositionPercent              # 计算仓位
        self.AssetsPositionFund = self.AssetsInvestedFund                       # 设定实时资产数额
        self.IdleFund = self.TotalFund - self.AssetsPositionFund                # 闲置资金 = 总资产 - 投资仓位

        return PositionPercent


#工具类，用于更新资金相关变化
class FundCurveToolClass:

    #资金管理属性列表集合
    def __init__(self):
        self.DateList = []                       #日期
        self.itxList1 = []                       #Index索引
        self.CloseList = []                      #当日收盘价
        self.PositionCostList = []               #持仓成本
        self.PositionTypeList = []               #持仓类型
        self.AssetsFundList = []                 #持仓总资产
        self.AssetsIncreaseList = []             #持仓收益率
        self.IdleFundList = []                   #闲置资产
        self.TotalFundList = []                  #总资产
        self.TotalInterestList = []              #总资产收益率

    def UpdateList(self,TodayDate,Index,TodayPrice,AssetsIncrease,FundManagementTool):

        self.DateList.append(TodayDate)
        self.itxList1.append(Index)
        self.CloseList.append(TodayPrice)
        self.PositionCostList.append(FundManagementTool.PositionHoldingCostPrice)
        self.PositionTypeList.append(FundManagementTool.PositionType)
        self.AssetsFundList.append(FundManagementTool.AssetsPositionFund)
        self.AssetsIncreaseList.append(AssetsIncrease)
        self.IdleFundList.append(FundManagementTool.IdleFund)
        self.TotalFundList.append(FundManagementTool.TotalFund)
        self.TotalInterestList.append(FundManagementTool.TotalFund - 1)

    def ToDataFrame(self):

        ResultDict = {
            "Date": self.DateList,
            "itx": self.itxList1,
            "Close": self.CloseList,
            "PositionCost": self.PositionCostList,
            "PositionType": self.PositionTypeList,
            "AssetsFund":self.AssetsFundList,
            "AssetsIncrease":self.AssetsIncreaseList,
            "IdleFund":self.IdleFundList,
            "TotalFund":self.TotalFundList,
            "TotalInterest":self.TotalInterestList,
        }

        ResultDataFrame = pd.DataFrame(ResultDict)
        ResultDataFrame.to_csv("1.csv")

        return ResultDataFrame

#操作逻辑类
class OperationLogicClass:

    # 操作逻辑列表集合
    def __init__(self):
        self.OperationTimeList = []
        self.itxList2 = []
        self.OperationPriceList = []
        self.OperationTypeList = []
        self.OperationNameList = []
        self.ProfitList = []
        self.PositionList = []

    def UpdateList(self, TodayDate, TodayPrice, OperationType, OperationName, ProfitStatus, Index, Position):
        self.OperationTimeList.append(TodayDate)
        self.itxList2.append(Index)
        self.OperationPriceList.append(TodayPrice)
        self.OperationTypeList.append(OperationType)
        self.OperationNameList.append(OperationName)
        self.ProfitList.append(ProfitStatus)
        self.PositionList.append(Position)

    def ToDataFrame(self):

        OperationList = {
            "date": self.OperationTimeList,
            "itx": self.itxList2,
            "OperationPrice": self.OperationPriceList,
            "OperationType": self.OperationTypeList,
            "OperationName": self.OperationNameList,
            "Profit": self.ProfitList,
            "Position": self.PositionList
        }

        ResultDataFrame = pd.DataFrame(OperationList)
        ResultDataFrame.to_csv("2.csv")

        return ResultDataFrame


#结果分析类
class ResultAnalysisClass:

    #结果分析类初始化
    def __init__(self,OperationDataFrame):
        self.OperationDataFrame = OperationDataFrame

    def Analysis(self):

        length = len(self.OperationDataFrame)       #获取操作列表的长度

        TotalCount = 0           #总(开/平)数
        ProfitableCount = 0      #盈利开仓数
        MaxProfit = -9999        #最大盈利
        MaxLoss = 9999           #最大回撤

        # j指向结算操作，i指向开仓操作
        j = 1
        while j < length:
            i = j - 1

            #增加总次数
            TotalCount = TotalCount + 1

            #增加盈利次数
            if self.OperationDataFrame.iloc[j].Profit > 0:
                ProfitableCount = ProfitableCount + 1

            if self.OperationDataFrame.iloc[j].Profit > MaxProfit:
                MaxProfit = self.OperationDataFrame.iloc[j].Profit

            if self.OperationDataFrame.iloc[j].Profit < MaxLoss:
                MaxLoss = self.OperationDataFrame.iloc[j].Profit

            j = j + 2

        WinningProbability = ProfitableCount / TotalCount

        StrMaxProfit = '{:.2f}%'.format(MaxProfit*100)
        StrMaxLoss = '{:.2f}%'.format(MaxLoss*100)
        StrWinningProbability = '{:.2f}%'.format(WinningProbability*100)


        AnalysisNumberDict = {"TotalCount": TotalCount, "ProfitableCount": ProfitableCount,'MaxProfit':MaxProfit,'MaxLoss':MaxLoss,'WinningProbability':WinningProbability}
        AnalysisStrDict = {"TotalCount": TotalCount, "ProfitableCount": ProfitableCount,'MaxProfit':StrMaxProfit,'MaxLoss':StrMaxLoss,'WinningProbability':StrWinningProbability}

        return AnalysisNumberDict,AnalysisStrDict


    def SignalAndOpeningAnalysis(self):

        length = len(self.OperationDataFrame)       #获取操作列表的长度

        TotalSignalCount = 0                  #总信号发生(开/平)数
        TotalOpeningCount = 0                 #总开仓数
        SignalProfitableCount = 0             #信号盈利数
        OpeningProfitableCount = 0            #开仓盈利数
        SignalMaxProfit = -9999               #信号最大盈利
        SignalMaxLoss = 9999                  #信号最大亏损
        OpeningMaxProfit = -9999              #开仓最大盈利
        OpeningMaxLoss = 9999                 #开仓最大亏损

        # j指向结算操作，i指向开仓操作
        j = 1
        while j < length:
            i = j - 1

            #增加总次数
            TotalSignalCount = TotalSignalCount + 1

            #信号处理
            if self.OperationDataFrame.iloc[j].Profit > 0:
                SignalProfitableCount = SignalProfitableCount + 1

            if self.OperationDataFrame.iloc[j].Profit > SignalMaxProfit:
                SignalMaxProfit = self.OperationDataFrame.iloc[j].Profit

            if self.OperationDataFrame.iloc[j].Profit < SignalMaxLoss:
                SignalMaxLoss = self.OperationDataFrame.iloc[j].Profit

            #开仓处理
            if self.OperationDataFrame.iloc[i].Position > 0:

                TotalOpeningCount = TotalOpeningCount + 1

                if self.OperationDataFrame.iloc[j].Profit > 0:
                    OpeningProfitableCount = OpeningProfitableCount + 1

                if self.OperationDataFrame.iloc[j].Profit > OpeningMaxProfit:
                    OpeningMaxProfit = self.OperationDataFrame.iloc[j].Profit

                if self.OperationDataFrame.iloc[j].Profit < OpeningMaxLoss:
                    OpeningMaxLoss = self.OperationDataFrame.iloc[j].Profit

            j = j + 2

        SignalWinningProbability = SignalProfitableCount / TotalSignalCount
        OpeningWinningProbability = OpeningProfitableCount / TotalOpeningCount

        StrSignalMaxProfit = '{:.2f}%'.format(SignalMaxProfit*100)
        StrSignalMaxLoss = '{:.2f}%'.format(SignalMaxLoss*100)
        StrSignalWinningProbability = '{:.2f}%'.format(SignalWinningProbability*100)

        StrOpeningMaxProfit = '{:.2f}%'.format(OpeningMaxProfit * 100)
        StrOpeningMaxLoss = '{:.2f}%'.format(OpeningMaxLoss * 100)
        StrOpeningWinningProbability = '{:.2f}%'.format(OpeningWinningProbability * 100)


        SignalAnalysisNumberDict = {"TotalSignalCount": TotalSignalCount, "SignalProfitableCount": SignalProfitableCount,'SignalMaxProfit':SignalMaxProfit,'SignalMaxLoss':SignalMaxLoss,'SignalWinningProbability':SignalWinningProbability}
        SignalAnalysisStrDict = {"TotalSignalCount": TotalSignalCount, "SignalProfitableCount": SignalProfitableCount,'SignalMaxProfit':StrSignalMaxProfit,'SignalMaxLoss':StrSignalMaxLoss,'SignalWinningProbability':StrSignalWinningProbability}

        OpeningAnalysisNumberDict = {"TotalOpeningCount": TotalOpeningCount, "OpeningProfitableCount": OpeningProfitableCount,
                              'OpeningMaxProfit': OpeningMaxProfit, 'OpeningMaxLoss': OpeningMaxLoss,
                              'OpeningWinningProbability': OpeningWinningProbability}
        OpeningAnalysisStrDict = {"TotalOpeningCount": TotalOpeningCount, "OpeningProfitableCount": OpeningProfitableCount,
                           'OpeningMaxProfit': StrOpeningMaxProfit, 'OpeningMaxLoss': StrOpeningMaxLoss,
                           'OpeningWinningProbability': StrOpeningWinningProbability}

        return SignalAnalysisStrDict,OpeningAnalysisStrDict

