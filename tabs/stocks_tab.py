from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from functions.ticker_options import get_ticker_dropdown_options
from functions.stocks import get_stocks
from functions.ticker_options import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def stocks_graph():
    return html.Div([
        html.H3('Stock Price'),

        # Dropdowns for stock selection and days
        html.Div([
            dcc.Dropdown(
                id="dropdown-company-stocks",
                options=get_ticker_dropdown_options(),
                placeholder="Select company",
                multi=True,  # Enable multiple selection
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


def sma(df, days):
    """
    Determines the stock trend based on the provided number of days.
    Returns 'green' for a positive trend and 'red' for a negative trend.
    """
    if df.empty or len(df) < days:
        return "gray"  # Not enough data to determine trend

    # Define the short and long windows dynamically
    short_window = max(1, int(days * 0.25))  # 25% of the period
    long_window = max(1, int(days * 0.75))   # 75% of the period

    # Calculate SMAs
    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()

    # Compare the last SMA values to determine the trend
    if df['SMA_Short'].iloc[-1] > df['SMA_Long'].iloc[-1]:
        return "green"  # Positive trend
    else:
        return "red"  # Negative trend


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

    # Check if we have a list (multiple stocks) or a single stock
    is_multi = isinstance(selected_stocks, list)

    # If it's a single stock or just one stock in the list
    if not is_multi or len(selected_stocks) == 1:
        # Handle single stock case
        stock = selected_stocks[0] if is_multi else selected_stocks

        df = get_stocks(stock)
        if df.empty:
            return {}, {"display": "none"}

        df = df.sort_values(by='Date', ascending=False).head(days)
        df['Stock'] = stock  # Add stock name for differentiation
        last_close_value = df.iloc[-1]['Close']
        c_name = get_company_by_name(stock)

        # Determine color based on SMA
        color = sma(df, days)
        line_color = 'green' if color == "green" else 'red'

        # Create a single graph with color differentiation
        fig = px.line(
            df,
            x='Date',
            y='Close',
            color='Stock',
            title=f'{c_name}',
            subtitle = f'${last_close_value:.2f}',
            labels={"Close": "Price ($)"}
        )

        # # Add subtitle with current price
        # fig.add_annotation(
        #     text=f"${last_close_value:.2f}",
        #     xref="paper", yref="paper",
        #     # x=0.5, y=0.95,
        #     showarrow=False,
        #     font=dict(size=14)
        # )

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title_text='Stocks',
            hovermode='closest',
            hoverdistance=20,
            dragmode=False
        )

        fig.update_traces(
            line=dict(color=line_color, width=2),
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Close: %{y:.2f}',
            hoveron='points+fills',
            fill='tozeroy',
            # Gradient-like fill color
            fillcolor='rgba(0, 128, 0, 0.1)' if color == "green" else 'rgba(255, 0, 0, 0.1)'
        )

        # Update axes
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    else:
        # Handle multiple stocks case
        combined_df = pd.DataFrame()

        for stock in selected_stocks[:5]:  # Limit to max 5 stocks
            df = get_stocks(stock)
            if df.empty:
                continue
            df = df.sort_values(by='Date', ascending=False).head(days)
            df['Stock'] = stock  # Add stock name for differentiation
            combined_df = pd.concat([combined_df, df])

        if combined_df.empty:
            # Hide the graph if there's no data
            return {}, {"display": "none"}

        # Create a multi-stock graph
        fig = px.line(
            combined_df,
            x='Date',
            y='Close',
            color='Stock',
            title=f'Stock Comparison Over the Last {days} Days',
            labels={"Close": "Price ($)"}
        )

        # Enhance the multi-stock visualization
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Close Price ($)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title_text='Companies',
            hovermode='closest'
        )

        # Add custom hover template for multiple stocks
        fig.update_traces(
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Price: $%{y:.2f}',
            line=dict(width=2)
        )
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    # Display the graph after valid input
    return fig, {"display": "block", "width": "100%"}
