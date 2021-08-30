from __future__ import print_function, absolute_import
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from DataProcess import StaffAnalysis,PEAnalysis
import plotly

import pandas as pd
from gm.api import *
from DataPrepare import DataPreprocess,get_DateList
from HigherDraw import HigherDrawing
from PlotlyDraw import ETFPlotDrawing

set_token('08fabd471462703dfe3f43b43d480f6e7dd1b5b6')
StockId = 'SHSE.600000'
start_time = '2014-01-01'
end_time = '2021-08-31'

price_Data = history(symbol=StockId, frequency='1d', start_time=start_time, end_time=end_time, fields='open,high,low,close,eob', df=True)
fundamental_Data = get_fundamentals(table='trading_derivative_indicator', symbols=StockId, start_date=start_time, end_date=end_time, fields='PETTM',limit = 10000, df=True)

price_Data,fundamental_Data= DataPreprocess(price_Data,Stock=True,fundamental_Data = fundamental_Data)

data = pd.merge(price_Data,fundamental_Data,left_index=True,right_index=True)

date_list = data.index.values.tolist()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Slider(
        id='slider-width', min=0, max=1,
        value=0.5, step=0.01),

    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')

])


@app.callback(
    Output("graph", "figure"),
    [Input("slider-width", "value")])
def MainGraphPlot(slider):

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2,
                        subplot_titles=(StockId, 'PETTM'), row_width=[0.2, 0.7])

    fig.add_trace(go.Candlestick(x=data.itx,
                                 open=data.open, high=data.high,
                                 low=data.low, close=data.close, increasing_line_color='#f6416c',
                                 decreasing_line_color='#7bc0a3', name="Price",
                                 hovertext=date_list,
                                 ), row=1, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig

if __name__ == '__main__':
    app.run_server()