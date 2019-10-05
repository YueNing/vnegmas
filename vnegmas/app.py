from random import randrange
from flask import Flask, Response, render_template
from flask.json import jsonify

import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
dash_app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = dash_app.server

app = Flask(__name__, static_folder="templates")


class EndpointAction(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name=__name__, template_folder="templates", static_folder="stats"):
        # import pdb; pdb.set_trace()
        self.app = Flask(name, template_folder=template_folder, static_folder=static_folder)

    def run(self):
        return self.app.run()

    def add_endpoint(
        self, rule, endpoint=None, view_func=None, handler=None, methods=["GET"]
    ):
        self.app.add_url_rule(
            rule, endpoint=endpoint, view_func=view_func, methods=methods
        )
