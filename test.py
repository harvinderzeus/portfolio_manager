import requests
import pandas as pd
from io import BytesIO

value = 'AAPL'

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=NBQAAHR8VV2B9YTX&datatype=csv'

data = requests.get(url)
df = pd.read_csv(BytesIO(data.content))

print(df)

def get_data(values):
    if values:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={value}&apikey=AR76335FQMQ04HNZ&datatype=csv'
        for val in values:
            
            data = requests.get(url)
            print(data.content)
            df = pd.read_csv(BytesIO(data.content))
        return val