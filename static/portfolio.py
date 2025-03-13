from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from functions.ticker_options import get_ticker_dropdown_options
import pandas as pd


# Portfolio DataFrame
portfolio = pd.DataFrame(columns=['Ticker', 'Volume'])


def portfolio_entry():
    return html.Div([
        html.H3('Portfolio Manipulation'),

        # Flexbox for proper alignment of elements
        html.Div([
            dcc.Dropdown(
                id="dropdown_company_portfolio",
                options=get_ticker_dropdown_options(),  # Dropdown includes all tickers
                placeholder="Select Stocks",
                style={"width": "100%", "margin-right": "10px"}
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
                style={"margin-left": "10px", "height": "30px",
                       "width": "10%", "margin-right": "10px"}
            ),
            html.Button('Clear',
                        id='clear-btn',
                        n_clicks=0,
                        style={"margin-left": "auto", "height": "30px", "width": "10%", "margin-right": "10px"})
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '70%'}),

        html.Br(),

        html.H4("Portfolio Data"),
        dash_table.DataTable(
            id='portfolio-table',
            columns=[
                {"name": "Ticker", "id": "Ticker"},
                {"name": "Volume", "id": "Volume"}
            ],
            data=[],  # Initially empty
            style_table={'width': '50%', 'align-items': 'center'}
        ),
        dcc.Store(id='portfolio-store', data=[], storage_type='session'),


    ])

# Callback to manage portfolio updates


@callback(
    Output('portfolio-table', 'data', allow_duplicate=True),
    # Output updated portfolio to the store
    Output('portfolio-store', 'data', allow_duplicate=True),
    Input('submit-val', 'n_clicks'),
    State('dropdown_company_portfolio', 'value'),
    State('Volume', 'value'),
    # Get current portfolio data from the store
    State('portfolio-store', 'data'),
    prevent_initial_call=True
)
def render_portfolio(n_clicks, ticker, volume, existing_portfolio):

    # If portfolio is None (i.e., no data), initialize it as an empty list
    if existing_portfolio is None:
        existing_portfolio = []

    # Check if both ticker and volume are valid (i.e., not None or empty)
    if ticker and volume:
        # Add new entry to the portfolio
        new_data = {"Ticker": ticker, "Volume": volume}
        existing_portfolio.append(new_data)

    # Return the updated portfolio data for both the table and the store
    return existing_portfolio, existing_portfolio

# Callback to clear the portfolio


@callback(
    Output('portfolio-table', 'data'),
    Output('portfolio-store', 'data'),  # Clear the data in the store as well
    Input('clear-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_portfolio(n_clicks):
    # Clear the portfolio stored in dcc.Store
    return [], []  # Empty the data in both the table and store
