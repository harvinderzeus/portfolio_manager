from dash import Dash, html, dcc, callback, Output, Input
from static.portfolio import portfolio_entry, render_portfolio
from tabs.stocks_tab import stocks_graph
from tabs.var_analysis_tab import analysis_portfolio

import dash
import pandas as pd


dark_mode_style = {
    'backgroundColor': '#333333',  # Dark background
    'color': '#ffffff',  # White text color
    'height': '100vh',  # Full viewport height
    'fontFamily': 'Arial, sans-serif'
}


# Initialize Dash app
app = dash.Dash(__name__,suppress_callback_exceptions=True)

# Define the app layout, including the portfolio entry and an additional store to persist the portfolio data
app.layout = html.Div(#style={'backgroundColor': '#f0f0f0', 'height': '100vh'},
                      children=[
                          html.H1("Portfolio Manager", style={'align-text':'center'}),
    
    html.Div([
        portfolio_entry(),
    
]),
    html.Div([
     html.Br()   
    ]),
        dcc.Tabs([
    
                dcc.Tab(label='Stock Graph', children=[stocks_graph()]),
        dcc.Tab(label='VaR analysis', children=[
         analysis_portfolio()
            ])
        ])
    ])


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
