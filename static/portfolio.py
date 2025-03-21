from dash import Dash, html, dcc, callback, Output, Input, dash_table, State, callback_context
from functions.ticker_options import get_ticker_dropdown_options
import pandas as pd
import plotly.express as px

# Portfolio DataFrame
portfolio = pd.DataFrame(columns=['Ticker', 'Volume'])


def portfolio_entry():
    return html.Div([
        html.H3('Portfolio Manipulation'),

        # Input section with flexbox for alignment
        html.Div([
            dcc.Dropdown(
                id="dropdown_company_portfolio",
                options=get_ticker_dropdown_options(),
                placeholder="Select Stocks",
                style={"width": "90.5%", "margin-right": "10px"}
            ),
            dcc.Input(
                id='Volume',
                type="number",
                placeholder="Enter Volume",
                min=1,
                max=100,
                style={"width": "20%", "height": "30px", "textAlign": "center"}
            ),
            html.Button('Submit', id='submit-val', n_clicks=0,
                        style={"height": "30px", "width": "10%"}),
            html.Button('Clear', id='clear-btn', n_clicks=0,
                        style={"height": "30px", "width": "10%", "margin-left": "10px"})
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '80%'}),

        html.Br(),

        # Portfolio Data and Pie Chart Side by Side
        html.Div([
            html.Div([
                html.H4("Portfolio Data", style={'text-align': 'left'}),
                dash_table.DataTable(
                    id='portfolio-table',
                    columns=[
                        {"name": "Ticker", "id": "Ticker"},
                        {"name": "Volume", "id": "Volume"}
                    ],
                    data=[],  # Initially empty
                    style_table={'width': '100%'},
                    style_cell={
                        'textAlign': 'center',
                        'fontSize': '14px',
                        'padding': '10px'
                    },
                ),
            ], style={'width': '50%', 'padding': '10px'}),

            html.Div([
                html.H4("Portfolio Distribution",
                        style={'text-align': 'left'}),
                dcc.Graph(id='portfolio-pie-chart', figure={})
            ], style={'width': '50%', 'padding': '10px'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'flex-start', 'width': '100%'}),

        dcc.Store(id='portfolio-store', data=[], storage_type='session'),
    ])


# Callback to handle both initial load and updates
@callback(
    [Output('portfolio-table', 'data'),
     Output('portfolio-pie-chart', 'figure'),
     Output('portfolio-pie-chart', 'style')],
    [Input('portfolio-store', 'data')]
)
def update_display_from_store(stored_data):
    """Update table and pie chart from stored data"""
    if not stored_data:
        return [], {}, {'width': '50%', 'padding': '10px', 'display': 'none'}

    # Create pie chart
    portfolio_df = pd.DataFrame(stored_data)
    pie_fig = px.pie(portfolio_df, values='Volume',
                     names='Ticker', hover_data={'Volume': True})
    pie_fig.update_traces(textposition='inside', textinfo='label+percent')

    return stored_data, pie_fig, {'width': '50%', 'padding': '10px', 'display': 'block'}


# Callback to update portfolio data
@callback(
    Output('portfolio-store', 'data'),
    Input('submit-val', 'n_clicks'),
    [State('dropdown_company_portfolio', 'value'),
     State('Volume', 'value'),
     State('portfolio-store', 'data')],
    prevent_initial_call=True
)
def render_portfolio(n_clicks, ticker, volume, existing_portfolio):
    """Add or update ticker in the portfolio"""
    if existing_portfolio is None:
        existing_portfolio = []

    if ticker and volume:
        # Remove previous entry if ticker exists (to update volume)
        existing_portfolio = [
            entry for entry in existing_portfolio if entry['Ticker'] != ticker]
        existing_portfolio.append({"Ticker": ticker, "Volume": volume})

    return existing_portfolio


# Callback to clear the portfolio
@callback(
    Output('portfolio-store', 'data', allow_duplicate=True),
    Input('clear-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_portfolio(n_clicks):
    """Clear the portfolio data"""
    return []
