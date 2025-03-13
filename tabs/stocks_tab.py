from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from functions.ticker_options import get_ticker_dropdown_options
from functions.stocks import get_stocks
import plotly.express as px
import pandas as pd


def stocks_graph():
    return html.Div([
        html.H3('Stock Price'),

        # Dropdowns for stock selection and days
        html.Div([
            dcc.Dropdown(
                id="dropdown-company-stocks",
                options=get_ticker_dropdown_options(),
                placeholder="Select up to 5 companies",
                multi=True,
                maxHeight=200,
                style={"width": "50%"}
            ),
            dcc.Dropdown(
                id="select-days-dropdown",
                options=[
                    {'label': '7 Days', 'value': 7},
                    {'label': '30 Days', 'value': 30},
                    {'label': '60 Days', 'value': 60},
                    {'label': '90 Days', 'value': 90},
                    {'label': '6 Months', 'value': 180},
                    {'label': '1 Year', 'value': 365}
                ],
                placeholder="Select number of days",
                style={"width": "50%"}
            ),
        ], style={'display': 'flex', 'gap': '10px'}),

        html.Br(),

        # Initially hidden graph
        dcc.Graph(id='stock-graph', style={"display": "none", "width": "80%"})
    ])


@callback(
    Output('stock-graph', 'figure'),
    Output('stock-graph', 'style'),
    Input('dropdown-company-stocks', 'value'),
    Input('select-days-dropdown', 'value'),
    prevent_initial_call=True
)
def update_graph(selected_stocks, days):
    if not selected_stocks or not days:
        # Hide the graph if inputs are missing
        return {}, {"display": "none"}

    combined_df = pd.DataFrame()

    for stock in selected_stocks[:5]:  # Limit to max 5 stocks
        df = get_stocks(value=stock)
        if df.empty:
            continue
        df = df.sort_values(by='Date', ascending=False).head(days)
        df['Stock'] = stock  # Add stock name for differentiation
        combined_df = pd.concat([combined_df, df])

    if combined_df.empty:
        # Hide the graph if there's no data
        return {}, {"display": "none"}

    # Create a single graph with color differentiation
    fig = px.line(
        combined_df,
        x='Date',
        y='Close',
        color='Stock',
        title=f'Stock Prices Over the Last {days} Days',
        markers=True
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')

    # Display the graph after valid input
    return fig, {"display": "block", "width": "100%"}
