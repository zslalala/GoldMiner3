import numpy as np
import pandas as pd

#资金管理类
class FundCurveClass:

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

    def UpdateList(self,TodayDate,Index,TodayPrice,PositionCost,PositionType,AssetsPositionFund,AssetsIncrease,IdleFund,TotalFund,TotalInterest):

        self.DateList.append(TodayDate)
        self.itxList1.append(Index)
        self.CloseList.append(TodayPrice)
        self.PositionCostList.append(PositionCost)
        self.PositionTypeList.append(PositionType)
        self.AssetsFundList.append(AssetsPositionFund)
        self.AssetsIncreaseList.append(AssetsIncrease)
        self.IdleFundList.append(IdleFund)
        self.TotalFundList.append(TotalFund)
        self.TotalInterestList.append(TotalInterest)

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

    def UpdateList(self, TodayDate, TodayPrice, OperationType, OperationName, ProfitStatus, Index):
        self.OperationTimeList.append(TodayDate)
        self.itxList2.append(Index)
        self.OperationPriceList.append(TodayPrice)
        self.OperationTypeList.append(OperationType)
        self.OperationNameList.append(OperationName)
        self.ProfitList.append(ProfitStatus)

    def ToDataFrame(self):

        OperationList = {
            "date": self.OperationTimeList,
            "itx": self.itxList2,
            "OperationPrice": self.OperationPriceList,
            "OperationType": self.OperationTypeList,
            "OperationName": self.OperationNameList,
            "Profit": self.ProfitList,
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

        TotalCount = 0           #总(开/平)仓数
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
        print(AnalysisNumberDict)
        print(AnalysisStrDict)

        return AnalysisNumberDict,AnalysisStrDict

