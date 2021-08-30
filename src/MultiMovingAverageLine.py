import pandas as pd
import numpy as np
import talib
import pandas_ta as ta

def DealMovingAverage(data,MAtype,windowList):

    if MAtype == 'SMA':
        return SimpleMovingAverage(data,windowList)

    if MAtype == 'EMA':
        return ExponentialMovingAverage(data,windowList)

    if MAtype == 'WMA':
        return WeightedMovingAverage(data,windowList)

    if MAtype == 'HMA':
        return HullMovingAverage(data,windowList)

def SimpleMovingAverage(data,windowList):

    close_np = np.asarray(data['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataSMA = talib.SMA(close_np, windowList[i])

        strName = 'SMA' + str(windowList[i])

        MAtitleName.append(strName)

        data[strName] = dataSMA

    return data,MAtitleName


def ExponentialMovingAverage(data,windowList):

    close_np = np.asarray(data['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataEMA = talib.EMA(close_np,windowList[i])

        strName = 'EMA' + str(windowList[i])

        MAtitleName.append(strName)

        data[strName] = dataEMA

    return data,MAtitleName

def WeightedMovingAverage(data,windowList):

    close_np = np.asarray(data['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataWMA = talib.WMA(close_np, windowList[i])

        strName = 'WMA' + str(windowList[i])

        MAtitleName.append(strName)

        data[strName] = dataWMA

    return data, MAtitleName

def HullMovingAverage(data,windowList):

    MAtitleName = []

    for i in range(len(windowList)):

        dataHMA = ta.hma(data['close'], windowList[i])

        strName = 'HMA' + str(windowList[i])

        MAtitleName.append(strName)

        data[strName] = dataHMA

    return data, MAtitleName
