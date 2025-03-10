import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests
import layout
import callbacks
from io import BytesIO


# Initialize the Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the app layout with card bodies
app.layout = layout.create_layout()
callbacks.register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


















# df = pd.read_csv('./data/listoftickers.csv')


# df.rename(columns={
#     "S.No.": "SNo",
#     "Company Name": "Company",
#     "Ticker": "Ticker",
#     "Sector": "Sector"
# }, inplace=True)

# # Format the dropdown options
# dropdown_options = [
#     {"label": f"{row['Company']} ({row['Ticker']})", "value": row['Ticker']} 
#     for _, row in df.iterrows()
# ]

# app = Dash()

# # Requires Dash 2.17.0 or later
# # app.layout = [
# #     html.H1(children='Portfolio Manager', style={'textAlign':'center'}),
# #     dcc.Tabs(id='portfolio-tabs', value='tab-1', children=[
# #         dcc.Tab(label='Stock Price', value='tab-1'),
# #         dcc.Tab(label='Tab two', value='tab-2'),
# #     ]),html.Div(id='portfolio-tabs-content')
    
# # ]
# @callback(
#     Output('portfolio-tabs-content', 'children'),
#     Input('portfolio-tabs', 'value')
# )
# def render_content(tab):
#     if tab == 'tab-1':
#         return html.Div([
#             html.H3('Stock Price'),
#             dcc.Dropdown(
#                 id="company-dropdown",
#                 options=dropdown_options,
#                 multi=True,
#                 placeholder="Select a company",
#                 style={"width": "40%"}
#             ),
#              dcc.Graph(id='stock-graph') 
#         ])
#     elif tab == 'tab-2':
#         return html.Div([
#             html.H3('Tab content 2'),
          
#         ])

# @app.callback(
#     Output('stock-graph', 'figure'),
#     Input('company-dropdown', 'value')
# )
# def update_graph(values):
#     #dff = df[df.Ticker==value]
#     #print(value)
#     df = get_data(values)
#     fig=px.line()
#     if values:
  
        
#         print(df)
#         # Plotly Line Graph
#         fig = px.line(df, x='timestamp', y='close', title=f'{value} Stock Prices Over Time')
#         fig.update_traces(mode='lines+markers')
#         fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')
#         return fig
#     return fig



# if __name__ == '__main__':
#     app.run(debug=True)