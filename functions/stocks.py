import pandas as pd
import requests
from io import BytesIO
import yfinance as yf

def get_stocks(value):
    if value:
            dat = yf.Ticker(value)
            stock_data=dat.history(period='1y')
            stock_data = stock_data.drop(['Dividends', 'Stock Splits'], axis=1)
            stock_data = stock_data.reset_index()
            return stock_data
    else:
        return "Value has not been sent"