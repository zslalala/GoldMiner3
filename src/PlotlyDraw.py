import plotly.graph_objects as go
import plotly
from DataProcess import StaffAnalysis
from plotly.subplots import make_subplots

def plotDrawing(StockId,data,NeedStaff = True,NeedPE = True):

    # 创建五线谱绘图
    if NeedStaff is True:
        data = StaffAnalysis(data)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.2,
                         subplot_titles=(StockId,'PETTM'),row_width=[0.2,0.7])

    fig.add_trace(go.Candlestick(x=data.index,
                                  open=data.open, high=data.high,
                                  low=data.low, close=data.close, increasing_line_color='#f6416c',
                                  decreasing_line_color='#7bc0a3', name="Price"),row=1,col=1)


    #设置布局
    layout = go.Layout(title_text=StockId, title_font_size=30, autosize=True, margin=go.layout.Margin(l=10, r=1, b=10),
                       xaxis=dict(type='category'),
                       )


    #绘制五线谱
    if NeedStaff is True:
        for i in ['priceTL', 'TL-2SD', 'TL-SD',
                  'TL+SD', 'TL+2SD']:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[i],
                    name=i,
                ),row = 1,col = 1)

    #绘制PETTM
    if NeedPE is True:
        fig.add_trace(go.Scatter(x=data.index,y=data.PETTM,name='PETTM',showlegend=True),row=2,col=1)

    fig.update_layout(layout)
    fig.update(layout_xaxis_rangeslider_visible=False)

    plotly.offline.plot(fig)