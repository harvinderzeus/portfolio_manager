from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px

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
                )
    ])

    @app.callback(
        Output('stock-graph', 'figure'),
        Input('company-dropdown', 'value')
    )
    def update_graph(value):
        fig = px.line()  # Empty figure as fallback

        if value:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={value}&apikey=75R803GKTBBIARXF&datatype=csv'
            response = requests.get(url)

            if response.status_code == 200:
                df = pd.read_csv(BytesIO(response.content))
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values(by='timestamp', ascending=False).head(30)

                fig = px.line(df, x='timestamp', y='close',
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
            share_portfolio = pd.concat([share_portfolio, new_data], ignore_index=True)

        return share_portfolio.to_dict('records')
