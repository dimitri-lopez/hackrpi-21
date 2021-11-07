#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc, Input, Output, State

import plotly.express as px
import pandas as pd
import numpy as np

import spotipy_test as sp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Spotify Data'),
    # html.Div(children='''Enter an Artist Name:'''),
    html.Div([
        dcc.Input(
            id="artist-name-input",
            placeholder="Artist...",
            type="text",
            # min = 2000, max= 2020, step = 1,
            minLength=0, maxLength=100,  # num of characters inside input box
            autoComplete='on',
            required=False,  # requires user to put something into input box  SET TRUE LATER
            autoFocus=True,  # highlight the box on reload
            size="20"
        )]),
    html.Button('Submit', id='artist-name-submit-button', n_clicks=0),

    html.Div(id='button-check-output',
             children='Enter your favorite artist'),
    html.Br(),  # break (space between input and graph)
    dcc.Graph(id="graph", figure={}),

])


@app.callback(
    Output('graph', 'figure'),
    Input('artist-name-submit-button', 'n_clicks'),
    State('artist-name-input', 'value')
)
def query_artist_name(n_clicks, artist_name):
    if n_clicks == 0:
        return {}

    print("Getting Spotify Data...")
    df = sp.look_up_artist(artist_name)
    # fig = px.scatter(df, x p "date", y = "duration", text = "name")
    print(df)
    fig = px.scatter(df, x="duration", y="valence",
                     text="name", color="album name")
    return fig
    # return {data: [{'x': np.random.randint(0, 100, 1000), 'type': ''}]}


if __name__ == '__main__':
    app.run_server(debug=True)
