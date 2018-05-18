# https://pythonprogramming.net/dynamic-data-visualization-application-dash-python-tutorial
# Dynamic Graph based on User Input - Data Visualization GUIs with Dash and Python p.3

import datetime
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
from dash.dependencies import Input, Output
from pandas_datareader._utils import RemoteDataError
from flask import Flask

server = Flask(__name__)

app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True


app.layout = html.Div(children=[
    html.H1(children='Stock'),

    html.Div(children='''
        Symbol to graph:
    '''),

    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')


])


@app.callback(

    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
    )
def update_graph(input_data):

    try:

        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime.now()
        df = web.DataReader(input_data, 'quandl', start, end)

        return dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': df.index, 'y': df.Close,
                        'type': 'line', 'name': input_data}
                ],
                'layout': {
                    'title': input_data
                }
            }
        )
    except AssertionError:

        if not input_data:
            return "Please type a ticker, in CAPS"
        else:
            return "Incorrect Ticker"


if __name__ == '__main__':
    app.run_server(debug=True)
