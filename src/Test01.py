# coding=utf-8
from __future__ import print_function, absolute_import

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from HigherDraw import HigherDrawing
from PlotlyDraw import plotDrawing


set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')
StockId = 'SHSE.600000'
start_time = '2014-01-01'
end_time = '2021-08-31'

price_Data = history(symbol=StockId, frequency='1d', start_time=start_time, end_time=end_time, fields='open,high,low,close,eob', df=True)
fundamental_Data = get_fundamentals(table='trading_derivative_indicator', symbols=StockId, start_date=start_time, end_date=end_time, fields='PETTM',limit = 10000, df=True)

date_list = get_DateList(start_time,end_time)

price_Data,fundamental_Data,dateTime_list = DataPreprocess(price_Data,fundamental_Data)

print(dateTime_list)
print(type(date_list[0]))

data = pd.merge(price_Data,fundamental_Data,left_index=True,right_index=True)


print(data)

# plotDrawing(StockId,data)

# HigherDrawing(data)