import plotly.graph_objects as go

import pandas as pd
from datetime import datetime


def draw(data_frame):
    df = data_frame
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()
