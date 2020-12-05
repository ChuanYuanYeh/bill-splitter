import datetime
import math
import dash
import cv2
from dash.dependencies import Input, Output, State
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'U FILL I SPLIT'
server = app.server

style = {'maxWidth': '960px', 'margin': 'auto'}

app.layout = html.Div([
    html.Div([
        dcc.Markdown("""
        # U FILL I SPLIT
        ## A free, no-BS utility
        To lazy to add each item? Simply upload an image of your receipt!
        """),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    html.Div(id='output-image-upload')
    ]),
    dcc.Input(
            id='editing-columns-name',
            placeholder='Enter a person\'s name...',
            value='',
            style={'padding': 10}
        ),
    html.Button('Add Person', id='editing-columns-button', n_clicks=0),
    dash_table.DataTable(
    id='editing-columns',
    columns=[{
        'name': 'Items',
        'id': 'item',
        'deletable': False,
        'renamable': False
    }, {
        'name': 'Price',
        'id': 'price',
        'deletable': False,
        'renamable': False,
        'type': 'numeric',
        'format': FormatTemplate.money(0)
    }],
    data=[],
    editable=True,
    row_deletable=True
    ),
    html.Button('Add Item', id='editing-rows-button', n_clicks=0),
    html.Button('Calculate', id='calculate-button', n_clicks=0),
    dcc.Markdown(id='output-content')
], style=style)


@app.callback(
    Output('editing-columns', 'columns'),
    [Input('editing-columns-button', 'n_clicks')],
    [State('editing-columns-name', 'value'),
     State('editing-columns', 'columns')])
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns

@app.callback(
    Output('editing-columns', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('editing-columns', 'data'),
     State('editing-columns', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    Output('output-content', 'children'),
    [Input('editing-columns', 'data'),
     Input('calculate-button', 'n_clicks')],
    [State('editing-columns', 'data'),
     State('editing-columns', 'columns')])
def compute(rows, n_clicks, columns, obj):
    if n_clicks > 0:
        final = ""
        df = pd.DataFrame(rows)

        priceToPay = {}
        for col in df:
            if col not in ['item','price']:
                priceToPay[col]=0

        for idx,row in df.iterrows():
            final += '### Calculating item: {}\n\n '.format(row['item'])
            total=float(row['price'])
            denom=0
            final += '**People responsible:**\n\n '
            for idx, ate in enumerate(row[2:]):
                if ate.lower() != 'x':
                    final += '{}\n\n '.format(row[2:].index[idx])
                    denom += 1
            pricePerPerson = total/denom
            final += '**Price per person responsible:** {}\n\n '.format(pricePerPerson)
            for idx, ate in enumerate(row[2:]):
                if ate.lower() != 'x':
                    priceToPay[row[2:].index[idx]] += pricePerPerson

        final += '# FINAL CALCULATION:\n\n'
        for key,value in priceToPay.items():
            final += '{}: {} B\n\n '.format(key, math.floor(value))

        return final
    else:
        return ''

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = parse_contents(list_of_contents, list_of_names, list_of_dates)
        return children

# Helper methods
def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)