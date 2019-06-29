from random import randrange

from flask.json import jsonify
from flask import Flask, render_template, Response

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

    def __init__(self, name=__name__, static_folder="templates"):
        self.app = Flask(name, static_folder=static_folder)
    
    def run(self):
        return self.app.run()
    
    def add_endpoint(self, rule, endpoint=None, view_func=None, handler=None, methods=['GET']):
        self.app.add_url_rule(rule, endpoint=endpoint, view_func=view_func, methods=methods)