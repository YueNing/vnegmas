import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import dash_app
from layouts import run_new

dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content'
        )
    ]
)

@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/app/app1':
        return 'hello world app1'
    elif pathname=='/':
        # from callbacks import update_progress
        return run_new
    else:
        return '404'

if __name__ == "__main__":
  dash_app.run_server(debug=True)