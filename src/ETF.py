# coding=utf-8
from __future__ import print_function, absolute_import

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from HigherDraw import HigherDrawing
from PlotlyDraw import plotDrawing
from sklearn.model_selection import RandomizedSearchCV


set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')
ETFId = 'SHSE.510300'
start_time = '2014-01-01'
end_time = '2021-08-31'

price_Data = history(symbol=ETFId, frequency='1d', start_time=start_time, end_time=end_time, fields='open,high,low,close,eob', df=True)
print(price_Data)

price_Data,fundamental_Data= DataPreprocess(price_Data,False)

data = price_Data

print(data)

plotDrawing(ETFId,data,True,False)