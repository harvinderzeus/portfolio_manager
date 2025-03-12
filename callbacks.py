from dash.dependencies import Input, Output, State
from dash import html
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import requests
from io import BytesIO
import plotly.express as px
import upload_to_blob as ub
import stocks
from datetime import datetime, timedelta


# Read CSV file
df = pd.read_csv('./data/listoftickers.csv')

df.rename(columns={
    "S.No.": "SNo",
    "Company Name": "Company",
    "Ticker": "Ticker",
    "Sector": "Sector"
}, inplace=True)

# Format the dropdown options
dropdown_options = [
    {"label": f"{row['Company']} ({row['Ticker']})", "value": row['Ticker']}
    for _, row in df.iterrows()
]

# Initialize portfolio DataFrame
share_portfolio = pd.DataFrame(columns=["Ticker", "Volume"])

def register_callbacks(app):
    df = pd.read_csv('./data/listoftickers.csv')

    df.rename(columns={
        "S.No.": "SNo",
        "Company Name": "Company",
        "Ticker": "Ticker",
        "Sector": "Sector"
    }, inplace=True)

# Format the dropdown options
    dropdown_options = [
        {"label": f"{row['Company']} ({row['Ticker']})",
         "value": row['Ticker']}
        for _, row in df.iterrows()
    ]

    @app.callback(
        Output('portfolio-tabs-content', 'children'),
        Input('portfolio-tabs', 'value')
    )
    def render_content(tab):
        if tab == 'tab-1':
            return html.Div([
                html.H3('Stock Price'),
                dcc.Dropdown(
                    id="company-dropdown",
                    options=dropdown_options,

                    placeholder="Select a company",
                    style={"width": "40%"}
                ),
                dcc.Graph(id='stock-graph')
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.H3('Portfolio Manipulation'),

                # Flexbox for proper alignment of elements
                html.Div([
                    dcc.Dropdown(
                        id="company-dropdown-tab2",
                        options=dropdown_options,  # Dropdown includes all tickers
                        placeholder="Select Stocks",
                        style={"width": "40%", "margin-right": "10px"}  # Adds spacing
                    ),
                    dcc.Input(
                        id='Volume',
                        type="number",
                        placeholder="Enter Volume",
                        min=1,
                        max=100,
                        style={"width": "20%", "height": "30px"}
                    ),
                    html.Button(
                        'Submit', 
                        id='submit-val', 
                        n_clicks=0,
                        style={"margin-left": "auto", "height": "30px", "width": "20%" }
                    )
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '100%'}),

                html.Br(),

                html.H4("Portfolio Data"),
                dash_table.DataTable(
                    id='portfolio-table',
                    columns=[
                        {"name": "Ticker", "id": "Ticker"},
                        {"name": "Volume", "id": "Volume"}
                    ],
                    data=[],  # Initially empty
                    style_table={'width': '75%', 'align-items': 'center'}
                ),
                html.Button(
                        'Generate Report', 
                        id='generate-report', 
                        n_clicks=0,
                        style={"margin-left": "auto", "height": "30px", "width": "20%" }
                    ),
                html.Div("Generation is done",id="gen-done",style={"display":"None"}),
    ])



    @app.callback(
    Output('stock-graph', 'figure'),
    Input('company-dropdown', 'value')
)
    def update_graph(value):
        fig = px.line()  # Empty figure as a fallback
    
        if value:

            df = stocks.get_stocks(value=value)
            df = df.sort_values(by='Date', ascending=False).head(30)
            fig = px.line(df, x='Date', y='Close',
                              title=f'{value} Stock Prices Over the Last 30 Days')
            fig.update_traces(mode='lines+markers')
            fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')

        return fig
        
    @app.callback(
        Output('portfolio-table', 'data'),
        Input('submit-val', 'n_clicks'),
        State('company-dropdown-tab2', 'value'),
        State('Volume', 'value'),
        prevent_initial_call=True
    )
    def update_portfolio(n_clicks, ticker, volume):
        global share_portfolio 
        
        if ticker and volume:
            new_data = pd.DataFrame([{"Ticker": ticker, "Volume": volume}])
            share_portfolio = pd.concat(
                [share_portfolio, new_data], ignore_index=True)
        return share_portfolio.to_dict('records')

    @app.callback(
        Output('gen-done','children'),
        Output('gen-done','style'),
        Input('generate-report', 'n_clicks'),

        prevent_initial_call=True
    )
    def update_blob(n_clicks):
        print(share_portfolio.head())
        if not share_portfolio.empty:
            ub.upload_portfolio_to_blob_storage(share_portfolio)
            for index, row in share_portfolio.iterrows():
                ticker = row['Ticker']
                df = stocks.get_stocks(ticker)
                print(df.head())
                # Sort the DataFrame by timestamp in descending order (latest first)
                df = df.sort_values(by='Date', ascending=False)
                # Get the last 100 stock trading days (assuming data is sorted by 'timestamp')
                df = df.head(100)
                print(df.head())
                ub.upload_ticker_record_to_blob_storage(df=df, ticker=ticker)
                
            return html.Div("uploaded"),{"display":"block"}
        else:
            return html.Div("empty"),{"display":"block"}
        

