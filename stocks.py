import pandas as pd
import requests
from io import BytesIO
import yfinance as yf

def get_stocks(value):
    if value:
            # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={value}&apikey=SIL4U3K31W2M7AWM&datatype=csv'
            # response = requests.get(url)

            # if response.status_code == 200:
            #     df = pd.read_csv(BytesIO(response.content))
            #     df['timestamp'] = pd.to_datetime(df['timestamp'])
            #     return df
            dat = yf.Ticker(value)
            stock_data=dat.history(period='1y')
            stock_data = stock_data.drop(['Dividends', 'Stock Splits'], axis=1)
            stock_data = stock_data.reset_index()
            return stock_data
    else:
        return "Value has not been sent"