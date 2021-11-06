#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html
from dash import dcc

import plotly.express as px
import pandas as pd
import numpy as np



app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
types = ['number', 'text']

types = ['Artist Name', 'Year']
input_types = ['text', 'number']

app.layout = html.Div(children = [
     html.H1(children='Spotify Data'),
     html.Div(children='''Dash: A web application framework for your data'''),
    html.Div([
        dcc.Input(
            id = "my_{}".format([types[x]]),
            placeholder = "{}".format(types[x]),
            type = input_types[x],
            min = 2000, max= 2020, step = 1, 
            minLength = 0, maxLength = 20, #num of characters inside input box
            autoComplete = 'on',  
            disabled = False,  #disable input
            readOnly = False,  #make input box read only
            required = False,  #requires user to put something into input box  SET TRUE LATER
            size = "20"
            #style = {'',''}
            #className = ''
            #persistence = ''
            #persistence_type = ''
        ) for x in range(len(input_types))
    ]),
    html.Br(), #break (space between input and graph) 
    dcc.Graph(id = "example-graph", figure = fig)
])

@app.callback( #call back links the data inputted with the graph  (Still working on this stuff below)
    [Output(component_id = "example-graph", component_property = 'figure')],
    [Input(component_id= "Year", component_property = "value")]
)

#function for the call back
def update_graph(compprop):
    print(compprop)
    print(type(compprop))

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
