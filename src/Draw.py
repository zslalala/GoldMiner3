import matplotlib as mpl   # 用于设置曲线参数
import matplotlib.pyplot as plt
import mplfinance as mpf

def Drawing(data):
    # 设置线的上升下降及边缘颜色
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='i',
        wick='i',
        inherit=True)

    # 设置网格线类型
    s = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=mc)

    mpf.plot(data,
             type='candle',
             style=s)

    plt.show()