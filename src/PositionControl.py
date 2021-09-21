import pandas as pd
import numpy as np
import talib
import pandas_ta as ta

def GetPositionByPETTM(PositionControlName,TodayElementValuation,PositionType):

    # 如果不使用仓位管理，直接满仓
    if PositionControlName == 'None':
        return 1

    # 如果今日估值要素在阈值日期内
    if TodayElementValuation == -1:
        return 0

    result = 0

    #空头仓位，估值要素百分比越高
    if PositionType == -1:
        result = TodayElementValuation
    if PositionType == 1:
        result = 1 - TodayElementValuation

    if result < 0.1:
        return 0
    if result > 0.9:
        return 1

    return result




def InsertPercentage(targetList,threshold):

    resultList = []

    SortList = []

    length = len(targetList)

    i = 0

    while i < length:

        targetNum = targetList[i]

        SortListLength = len(SortList)

        #重置j
        j = 0

        while j <= SortListLength:

            if j == SortListLength:
                if i < threshold:
                    resultList.append(-1)
                else:
                    SortList.insert(length,targetNum)
                    resultList.append(1)
                break

            if targetNum < SortList[j]:
                SortList.insert(j,targetNum)
                if i < threshold:
                    resultList.append(-1)
                else:
                    resultList.append(j/SortListLength)
                break

            j = j + 1

        i = i + 1

    return SortList,resultList

def GetPercentage(Name,data,threshold = 100):

    if Name == 'None':
        return data,None

    targetList = data[Name].tolist()

    SortList,resultList = InsertPercentage(targetList,threshold)

    print(resultList)

    #设置估值要素百分比列名
    PercentageName = "Percentage" + Name

    data[PercentageName] = resultList

    return data,PercentageName