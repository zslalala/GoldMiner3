import pandas as pd
import numpy as np
import talib
import pandas_ta as ta

def DealMovingAverage(data,MAtype,windowList,Copy=True):

    if MAtype == 'SMA':
        return SimpleMovingAverage(data,windowList,Copy)

    if MAtype == 'EMA':
        return ExponentialMovingAverage(data,windowList,Copy)

    if MAtype == 'WMA':
        return WeightedMovingAverage(data,windowList,Copy)

    if MAtype == 'HMA':
        return HullMovingAverage(data,windowList,Copy)

def SimpleMovingAverage(data,windowList,Copy):

    #定义新的Dataframe
    Average = data.copy(deep=True)

    close_np = np.asarray(Average['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataSMA = talib.SMA(close_np, windowList[i])

        strName = 'SMA' + str(windowList[i])

        MAtitleName.append(strName)

        Average[strName] = dataSMA

        if Copy is False:
            data[strName] = dataSMA

    if Copy is True:
        return Average, MAtitleName
    else:
        return data, MAtitleName



def ExponentialMovingAverage(data,windowList,Copy):

    #定义新的Dataframe
    Average = data.copy(deep=True)

    close_np = np.asarray(Average['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataEMA = talib.EMA(close_np,windowList[i])

        strName = 'EMA' + str(windowList[i])

        MAtitleName.append(strName)

        Average[strName] = dataEMA

        if Copy is False:
            data[strName] = dataEMA

    if Copy is True:
        return Average, MAtitleName
    else:
        return data, MAtitleName

def WeightedMovingAverage(data,windowList,Copy):

    # 定义新的Dataframe
    Average = data.copy(deep=True)

    close_np = np.asarray(Average['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataWMA = talib.WMA(close_np, windowList[i])

        strName = 'WMA' + str(windowList[i])

        MAtitleName.append(strName)

        Average[strName] = dataWMA

        if Copy is False:
            data[strName] = dataWMA

    if Copy is True:
        return Average, MAtitleName
    else:
        return data, MAtitleName

def HullMovingAverage(data,windowList,Copy):

    # 定义新的Dataframe
    Average = data.copy(deep=True)

    close_np = np.asarray(Average['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataHMA = ta.hma(data['close'], windowList[i])

        strName = 'HMA' + str(windowList[i])

        MAtitleName.append(strName)

        Average[strName] = dataHMA

        if Copy is False:
            data[strName] = dataHMA

    if Copy is True:
        return Average, MAtitleName
    else:
        return data, MAtitleName