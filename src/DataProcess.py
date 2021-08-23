import numpy as np
import pandas as np
from sklearn import linear_model


def PEAnalysis(data):
    return 0


def StaffAnalysis(data):
    reg = linear_model.LinearRegression()

    # 展成N行一列的向量，如[[1],[2],[3]]
    tempitx = data['itx'].values.reshape(-1, 1)

    #线性回归
    reg.fit(tempitx,data['close'])

    #打印斜率
    print("回归直线的斜率为",reg.coef_)
    #打印截距
    print("回归直线的截距为",reg.intercept_)

    #带入x求y
    data['priceTL'] = reg.intercept_ + data['itx'] * reg.coef_[0]

    #误差
    data['y-pTL'] = data['close'] - data['priceTL']

    #求标准差
    psd = data['y-pTL'].std()

    #分别计算上下一个和两个标准差
    data['TL+SD'] = data['priceTL'] + psd
    data['TL+2SD'] = data['priceTL'] + 2 * psd
    data['TL-SD'] = data['priceTL'] - psd
    data['TL-2SD'] = data['priceTL'] - 2 * psd

    return data