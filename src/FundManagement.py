import numpy as np
import pandas as pd

#资金管理类
class FundCurveClass:

    #资金管理属性列表集合
    def __init__(self):
        self.DateList = []
        self.itxList1 = []
        self.CloseList = []
        self.IncreaseList = []
        self.PositionList = []
        self.AssetsFundList = []
        self.FundList = []

    def UpdateList(self,TodayDate,TodayPrice,IncreaseRate,PositionHolding,AssetsPositionFund,EarningCurve,Index):

        self.DateList.append(TodayDate)
        self.itxList1.append(Index)
        self.CloseList.append(TodayPrice)
        self.IncreaseList.append(IncreaseRate)
        self.PositionList.append(PositionHolding)
        self.AssetsFundList.append(AssetsPositionFund)
        self.FundList.append(EarningCurve)

    def ToDataFrame(self):

        ResultDict = {
            "date": self.DateList,
            "itx": self.itxList1,
            "close": self.CloseList,
            "IncreaseRate": self.IncreaseList,
            "PositionHolding": self.PositionList,
            "NowFund": self.AssetsFundList,
            "FundProfit": self.FundList
        }

        ResultDataFrame = pd.DataFrame(ResultDict)
        ResultDataFrame.to_csv("1.csv")

        return ResultDataFrame

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