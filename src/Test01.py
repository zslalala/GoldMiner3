# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import matplotlib as mpl   # 用于设置曲线参数
import matplotlib.pyplot as plt
import mplfinance as mpf
from DataPrepare import DataPreprocess
from Draw import Drawing
import pandas as pd
import numpy as np

set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')
StockId = 'SHSE.600000'
data = history(symbol='SHSE.600000', frequency='1d', start_time='2020-01-01', end_time='2021-01-31', fields='open,high,low,close,eob', adjust=ADJUST_PREV, adjust_end_time='2020- 12-31', df=True)

data = DataPreprocess(data)

Drawing(data)