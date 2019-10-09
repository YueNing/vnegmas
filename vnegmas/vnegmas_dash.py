import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import dash_app
from layouts import layout_run_new, layout_load, layout_runnable
import flask

url_bar_and_content_div =  html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content'
        )
    ]
)

def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        layout_runnable,
        layout_run_new,
        
    ])

dash_app.layout = serve_layout

from callbacks import update_progress


@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout_run_new
    elif pathname == '/load':
        return layout_load
    elif pathname == '/run_new':
        # from callbacks import update_progress
        return layout_run_new
    elif pathname == '/checkpoint':
        return 
    elif pathname == '/runnable':
        return 
    elif pathname == '/not_runnable':
        return
    else:
        return '404'

if __name__ == "__main__":
  dash_app.run_server(debug=True)