from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app, server
from tabs import home, items, calculate

style = {'maxWidth': '960px', 'margin': 'auto'}
app.layout = html.Div([
    dcc.Markdown('# U Fill I Split'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Home', value='tab-home'),
        dcc.Tab(label='Items', value='tab-items'),
        dcc.Tab(label='Calculate', value='tab-calculate')
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-home': return home.layout
    elif tab == 'tab-items': return items.layout
    elif tab == 'tab-calculate': return calculate.layout

if __name__ == '__main__':
    app.run_server(debug=True)