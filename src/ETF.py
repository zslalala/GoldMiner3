# coding=utf-8
from __future__ import print_function, absolute_import

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from MultiMovingAverageLine import DealMovingAverage
from HigherDraw import HigherDrawing
from PlotlyDraw import ETFPlotDrawing

#账户设置
set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')

#ETFId,起始终止时间设置
ETFId = 'SHSE.000300'
start_time = '2014-01-01'
end_time = '2021-08-31'

#五线谱设置
UseFive = False

#移动平均线设置
UseMA = True
MAType = 'HMA'
windowList = [5,20,60,120]


price_Data = history(symbol=ETFId, frequency='1d', start_time=start_time, end_time=end_time, fields='open,high,low,close,eob', df=True)

price_Data,_= DataPreprocess(price_Data,False)

data = price_Data

data,MAtitleName = DealMovingAverage(data,MAType,windowList)

ETFPlotDrawing(ETFId,data,UseFive,UseMA,MAtitleName)