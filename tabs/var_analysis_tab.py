from functions.stocks import get_stocks
from functions.azure_blob_utils import upload_stocks_data, upload_user_portfolio, read_output_blob
from functions.databricks_job_utils import run_db_job
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px

import pandas as pd


# Layout of the analysis page
from dash import dcc

def analysis_portfolio():
    return html.Div([
        html.Div([
            html.H3('Stock Price'),
            html.Div([
                # Dropdown for selecting number of days
                dcc.Dropdown(
                    id="select-days-var-dropdown",
                    options=[
                        {'label': '7 Days', 'value': 7},
                        {'label': '30 Days', 'value': 30},
                        {'label': '60 Days', 'value': 60},
                        {'label': '90 Days', 'value': 90},
                        {'label': '6 Months', 'value': 180},
                        {'label': '1 Year', 'value': 365}
                    ],
                    placeholder="Select number of days",
                    style={"width": "30%"}
                ),

                # Numeric input for confidence level
                dcc.Input(
                    id="confidence-level-input",
                    type="number",
                    min=90,
                    max=99,
                    step=0.1,
                    placeholder="Confidence Level (e.g., 95)",
                    style={"width": "20%", "margin-left": "10px"}
                ),

                # Generate Report Button
                html.Button(
                    'Generate Report',
                    id='generate-report',
                    n_clicks=0,
                    disabled=True,  # Initially disabled
                    style={"margin-left": "10px", "height": "30px", "width": "15%", "margin-right": "10px"}
                )
            ], style={'display': 'flex', 'alignItems': 'center'}),

            # Error message when portfolio is empty
            html.Div("Enter your portfolio details",
                     id="error-message", style={'display': 'None'}),

            # Loading spinner
            dcc.Loading(
                id="loading",
                type="circle",
                children=html.Div(id="loading-output")
            ),

            # Store components
            dcc.Store(id='stock-data-store'),
            dcc.Store(id='blob-update', data=False),
            dcc.Store(id='histogram-trigger', data=False),
            dcc.Store(id='confidence-level-store')  # New store to hold confidence level
        ]),

        # Div for triggering Databricks-related callbacks
        html.Div(id="databricks-trigger"),
        html.Br(),
            # Portfolio Return Histogram
        dcc.Graph(
        id='histogram-plot',
        style={'display':'None'}
    ),
        html.Div(id='VaR-text')
    ])


# Callback to enable/disable the generate report button based on dropdown selection


@callback(
    Output('generate-report', 'disabled'),
    Input('select-days-var-dropdown', 'value'),
    Input('confidence-level-input', 'value')
)
def toggle_generate_button(selected_days, confidence_level):
    return selected_days is None or confidence_level is None

# Callback to manage portfolio and stock data


@callback(
    Output('error-message', 'style'),
    Output('loading-output', 'children', allow_duplicate=True),
    Output('stock-data-store', 'data'),
    Output('confidence-level-store', 'data'),  # Store confidence level
    Input('generate-report', 'n_clicks'),
    State('portfolio-table', 'data'),
    State('select-days-var-dropdown', 'value'),
    State('confidence-level-input', 'value'),
    prevent_initial_call=True
)
def render_var_analysis(n_clicks, existing_portfolio, days, confidence_level):
    if not existing_portfolio:
        return (
            {'color': 'red', 'fontWeight': 'bold', 'fontSize': '16px',
                'marginTop': '10px', 'display': 'block'},
            '',
            [],
            None
        )

    # Hide error message
    portfolio_df = pd.DataFrame(existing_portfolio)

    # Fetch stock data
    all_stock_data = pd.DataFrame()
    tickers = portfolio_df['Ticker'].tolist()
    for ticker in tickers:
        stock_data = get_stocks(ticker)
        stock_data = stock_data.sort_values(
            by='Date', ascending=False).head(days)

        stock_data['Ticker'] = ticker
        all_stock_data = pd.concat([all_stock_data, stock_data], ignore_index=True)

    # Store stock data in dcc.Store
    stock_data_dict = all_stock_data.to_dict('records')

    return {'display': 'None'}, 'Data fetched. Generating report...', stock_data_dict, confidence_level

# Callback to upload data to Blob Storage


@callback(
    Output('blob-update', 'data'),
    Input('stock-data-store', 'data'),
    State('portfolio-table', 'data'),
    prevent_initial_call=True
)
def blob_update(stock_data, portfolio_data):
    if not portfolio_data or not stock_data:
        return False

    stock_df = pd.DataFrame(stock_data)
    portfolio_df = pd.DataFrame(portfolio_data)

    upload_user_portfolio(portfolio_df)
    upload_stocks_data(stock_df)
    return True

# Callback to trigger Databricks processing


# Callback to trigger Databricks processing
@callback(
    Output('databricks-trigger', 'children'),
    Output('histogram-trigger', 'data'),
    Output('loading-output', 'children'),  # To show loading message
    Input('blob-update', 'data'),
    State('confidence-level-store', 'data'),  # Retrieve confidence level
    prevent_initial_call=True
)
def databrick_call(flag, confidence_level):
    if flag:
        style = {
            'padding': '15px',
            'backgroundColor': '#e6ffed',
            'border': '1px solid #2ecc71',
            'borderRadius': '8px',
            'color': '#27ae60',
            'fontWeight': 'bold',
            'fontSize': '16px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginTop': '20px'
        }
        con_value = float(confidence_level / 100)
        loading_message = "Processing Databricks job... Please wait."
        
        # Trigger Databricks job
        if run_db_job(con_value):  # Pass confidence level
            return html.Div(
                f"✅ Results successfully calculated with {confidence_level}% confidence level.",
                style=style
            ), True, loading_message
        else:
            return html.Div(
                "❌ An error occurred while processing the Calculation job!",
                style=style
            ), False, "Failed to process the job."

# Callback to render histogram and VaR after Databricks job is complete
@callback(
    Output('histogram-plot', 'figure'),
    Output('histogram-plot', 'style'),
    Output('VaR-text', 'children'),
    Input('histogram-trigger', 'data'),
    prevent_initial_call=True
)
def render_histogram(flag):
    if flag:
        # The job is complete and we can now fetch results from the blob storage
        df, text = read_output_blob()

        # Create histogram plot of portfolio returns
        fig = px.histogram(df, x="total_return", nbins=30, title="Portfolio Return Histogram", labels={"PortfolioReturn": "Portfolio Return"})

        return fig, {'display': 'block'}, html.Div([
            html.H3("Value at Risk (VaR) Result"),
            html.P(text)  # Display the VaR result
        ])
    else:
        return None, None, None