from dash import dcc, html


def create_layout():
    return html.Div([html.H1(children='Portfolio Manager', style={'textAlign': 'center'}),
                     dcc.Tabs(id='portfolio-tabs', value='tab-1', children=[
                         dcc.Tab(label='Stock Price', value='tab-1'),
                         dcc.Tab(label='Portfolio', value='tab-2'),
                     ]), html.Div(id='portfolio-tabs-content')])
