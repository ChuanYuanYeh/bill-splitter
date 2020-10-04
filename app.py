import math
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

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
        ### How it works
        1. Add the names of everyone.
        2. Add all items and their corresponding prices.
        3. Mark an 'x' under a person's name if he/she is not responsible for paying that specific item.
        4. You're welcome.
        """),
        dcc.Input(
            id='editing-columns-name',
            placeholder='Enter a person\'s name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Person', id='editing-columns-button', n_clicks=0)
    ]),
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
                if ate != 'x':
                    final += '{}\n\n '.format(row[2:].index[idx])
                    denom += 1
            pricePerPerson = total/denom
            final += '**Price per person responsible:** {}\n\n '.format(pricePerPerson)
            for idx, ate in enumerate(row[2:]):
                if ate != 'x':
                    priceToPay[row[2:].index[idx]] += pricePerPerson

        final += '# FINAL CALCULATION:\n\n'
        for key,value in priceToPay.items():
            final += '{}: {} B\n\n '.format(key, round(math.floor(value), -1))

        return final
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)