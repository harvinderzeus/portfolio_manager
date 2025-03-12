import requests
import pandas as pd
from io import BytesIO
import store_data

value = 'AAPL'

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=NBQAAHR8VV2B9YTX&datatype=csv'

data = requests.get(url)
df = pd.read_csv(BytesIO(data.content))
store_data.upload_to_blob_storage(df,value)
print(df)

# def get_data(values):
    
    
#     if values:
#         url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={value}&apikey=AR76335FQMQ04HNZ&datatype=csv'
#         for val in values:
            
#             data = requests.get(url)
#             print(data.content)
#             df = pd.read_csv(BytesIO(data.content))
#             df.head()
            
#             store_data.upload_to_blob_storage(df,value)
#         return val