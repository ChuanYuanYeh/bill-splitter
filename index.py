from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app, server

style = {'maxWidth': '960px', 'margin': 'auto'}
app.layout = html.Div([
    dcc.Markdown('# Bill Splitter'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Home', value='tab-home')
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    pass
if __name__ == '__main__':
    app.run_server(debug=True)