import pandas as pd

# Read CSV file
df = pd.read_csv('./assets/ticker_data/listoftickers.csv')

df.rename(columns={
    "S.No.": "SNo",
    "Company Name": "Company",
    "Ticker": "Ticker",
    "Sector": "Sector"
}, inplace=True)

def get_ticker_dropdown_options():
        # Format the dropdown options
    dropdown_options = [
    {"label": f"{row['Company']} ({row['Ticker']})", "value": row['Ticker']}
    for _, row in df.iterrows()
    ]
    return dropdown_options

def get_company_by_name(ticker):
    company_name = df[df['Ticker'] == ticker]['Company'].values
    if len(company_name) > 0:
        return company_name[0]
    else:
        return "Ticker not found"
    
