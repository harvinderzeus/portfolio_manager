from dash.dependencies import Input, Output, State
from dash import html
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import requests
from io import BytesIO
import plotly.express as px


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
                html.H3('Tab content 2'),

            ])



    @app.callback(
    Output('stock-graph', 'figure'),
    Input('company-dropdown', 'value')
)
    def update_graph(value):
        fig = px.line()  # Empty figure as a fallback
    
        if value:
        # Fetch data from the API
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={value}&apikey=75R803GKTBBIARXF&datatype=csv'
            response = requests.get(url)
        
            if response.status_code == 200:
                df = pd.read_csv(BytesIO(response.content))
            
            # Convert 'timestamp' to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df[(df['timestamp'].dt.year >= 2024) & (df['timestamp'].dt.year <= 2025)]


            # Group by month and get the first entry for each month
                df['month'] = df['timestamp'].dt.to_period('M')
                df = df.groupby('month').first().reset_index()

            # Convert 'month' back to timestamp for plotting
                df['timestamp'] = df['month'].dt.to_timestamp()
                df = df.drop(columns=['month'])

            # Filter to the last 12 months
                df = df.head(12)

            # Plotting the graph
                fig = px.line(df, x='timestamp', y='close',
                          title=f'{value} Stock Prices Over the Last 12 Months')
                fig.update_traces(mode='lines+markers')
                fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')
            else:
                print(f"Error fetching data: {response.status_code}")
    
        return fig
