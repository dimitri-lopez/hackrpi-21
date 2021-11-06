#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc, Input, Output, State

import plotly.express as px
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
types = ['number', 'text']

types = ['Artist Name', "Year"]  # TODO add Year and what not later
input_types = ['text', 'number']

app.layout = html.Div(children = [
     html.H1(children='Spotify Data'),
     # html.Div(children='''Enter an Artist Name:'''),
    html.Div([
        dcc.Input(
            id = "artist-name-input",
            placeholder = "Artist...",
            type = "text",
            # min = 2000, max= 2020, step = 1,
            minLength = 0, maxLength = 100, #num of characters inside input box
            autoComplete = 'on',  
            required = False,  # requires user to put something into input box  SET TRUE LATER
            autoFocus = True,  # highlight the box on reload
            size = "20"
        )]),
    html.Button('Submit', id='artist-name-submit-button', n_clicks=0),

    html.Div(id='button-check-output',
             children='Enter a value and press submit'),
    html.Br(), #break (space between input and graph) 
    dcc.Graph(id = "graph", figure = {}),
    dcc.Graph(id = "example-graph", figure = fig)
])

@app.callback(
    Output('button-check-output', 'children'),
    Input('artist-name-submit-button', 'n_clicks'),
    State('artist-name-input', 'value')
)
def query_artist_name(n_clicks, artist_name):
    fig.update_layout(title_text='NEW TITLE', title_x=0.5)

    print(fig)

    return 'The user inputted the artist: "{}" and the button has been clicked {} times'.format(
        artist_name,
        n_clicks
    )
# dcc.Dropdown(id = "select_genre", 
#     options = [
#         {"label": "pop", "value": "Pop"},
#         multi = False,
#         value = 'Pop',
#         style = {'width' : '40%'}
#     ]
# )

# app.layout = html.Div(children=[
#     html.H1(children='Spotify Data'),
#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ]) 


if __name__ == '__main__':
    app.run_server(debug=True)
