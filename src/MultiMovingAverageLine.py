import pandas as pd
import numpy as np
import talib

def SimpleMovingAverage(data,windowList):

    close_np = np.asarray(data['close'])

    MAtitleName = []

    for i in range(len(windowList)):

        dataSMA = talib.SMA(close_np, windowList[i])

        strName = 'SMA' + str(windowList[i])

        MAtitleName.append(strName)

        data[strName] = dataSMA

    return data,MAtitleName
