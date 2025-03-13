from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from functions.ticker_options import get_ticker_dropdown_options
from functions.stocks import get_stocks

import plotly.express as px


def stocks_graph():
    return html.Div([
        html.H3('Stock Price'),
        html.Div([
            dcc.Dropdown(
            id="dropdown-company-stocks",
            options=get_ticker_dropdown_options(),
            placeholder="Select a company",
            style={"width": "40%"}
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
            style={"width": "40%"}  # Appropriate width size for the dropdown
        ),
    ],style ={'display':'flex'}),
        dcc.Graph(id='stock-graph',style={"display":"None","width":"50%"})
    ])


@callback(
    Output('stock-graph', 'figure'),
    Output('stock-graph','style'),
    Input('dropdown-company-stocks', 'value'),
    Input('select-days-dropdown','value' ),
    prevent_initial_call=True
)
def update_graph(value, days ):
    fig = px.line()  # Empty figure as a fallback

    if value:

        df = get_stocks(value=value)
        df = df.sort_values(by='Date', ascending=False).head(days)
        fig = px.line(df, x='Date', y='Close',
                      title=f'{value} Stock Prices Over the Last {days} Days')
        fig.update_traces(mode='lines+markers')
        fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')
        
        return fig, {'display':'block'}
    else:
        return None, None
