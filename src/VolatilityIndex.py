import pandas as pd
import numpy as np
import talib
import pandas_ta as ta
from Start import r
from MultiMovingAverageLineDash import DealMovingAverage

def CalVolatility(data, VolatilityType):

    if VolatilityType == 'ATR':
        return GetATR(data)


def GetATR(data):

    #选取data中特定的一些列构建新DataFrame
    columns = ['itx','open','close','low','high']
    VolatilityData = pd.DataFrame(data,columns=columns)

    #获取ATR计算相关数据，送入Talib库
    close_np = np.asarray(VolatilityData.close)
    low_np = np.asarray(VolatilityData.low)
    high_np = np.asarray(VolatilityData.high)

    #获取中心线类型
    ATRAverageType = r.get("ATRAverageType")
    ATRAverageLineWS = int(r.get("ATRAverageLineWS"))
    ATRWS = int(r.get("ATRWS"))

    #计算中心线，不需要再出现新DataFrame
    VolatilityData,MAtitleName = DealMovingAverage(VolatilityData,ATRAverageType,[ATRAverageLineWS],False)

    #更改中心线名称
    VolatilityData = VolatilityData.rename(columns = {MAtitleName[0]:"CenterLine"})

    #计算ATR数据
    ATR = talib.ATR(high_np,low_np,close_np,timeperiod = ATRWS)
    VolatilityData['ATR'] = ATR

    return VolatilityData