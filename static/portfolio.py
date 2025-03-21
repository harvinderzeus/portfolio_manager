from dash import html, dcc, callback, Output, Input, dash_table, State
from functions.ticker_options import get_ticker_dropdown_options
import pandas as pd
import plotly.express as px

# Portfolio DataFrame
portfolio = pd.DataFrame(columns=['Ticker', 'Volume'])

def portfolio_entry():
    return html.Div([
        html.H3('Portfolio Manipulation'),
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
        html.Div([
            html.Div([
                html.H4("Portfolio Data", style={'text-align': 'left'}),
                dash_table.DataTable(
                    id='portfolio-table',
                    columns=[
                        {"name": "Ticker", "id": "Ticker", "editable": False},
                        {"name": "Volume", "id": "Volume", "editable": True, "type": "numeric"}
                    ],
                    data=[],
                    style_table={'width': '100%'},
                    style_cell={
                        'textAlign': 'center',
                        'fontSize': '14px',
                        'padding': '10px'
                    },
                ),
            ], style={'width': '50%', 'padding': '10px'}),
            html.Div([
                html.H4("Portfolio Distribution", style={'text-align': 'left'}),
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
    portfolio_df = pd.DataFrame(stored_data)
    pie_fig = px.pie(portfolio_df, values='Volume', names='Ticker', hover_data={'Volume': True})
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
        existing_portfolio = [entry for entry in existing_portfolio if entry['Ticker'] != ticker]
        existing_portfolio.append({"Ticker": ticker, "Volume": volume})
    return existing_portfolio

# Callback to update the store when the DataTable is edited with 1-100 validation
@callback(
    Output('portfolio-store', 'data', allow_duplicate=True),
    Input('portfolio-table', 'data'),
    State('portfolio-store', 'data'),
    prevent_initial_call=True
)
def update_portfolio_from_table(edited_data, existing_portfolio):
    """Update stored portfolio data when DataTable is edited, enforce 1-100 range"""
    if not edited_data:
        return existing_portfolio or []
    updated_portfolio = []
    for row in edited_data:
        try:
            new_volume = float(row['Volume'])
            if 1 <= new_volume <= 100:
                volume = new_volume
            else:
                old_entry = next((e for e in (existing_portfolio or []) if e['Ticker'] == row['Ticker']), None)
                volume = old_entry['Volume'] if old_entry else 1
        except (ValueError, TypeError):
            old_entry = next((e for e in (existing_portfolio or []) if e['Ticker'] == row['Ticker']), None)
            volume = old_entry['Volume'] if old_entry else 1
        updated_portfolio.append({"Ticker": row['Ticker'], "Volume": volume})
    return updated_portfolio

# Callback to clear the portfolio
@callback(
    Output('portfolio-store', 'data', allow_duplicate=True),
    Input('clear-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_portfolio(n_clicks):
    """Clear the portfolio data"""
    return []