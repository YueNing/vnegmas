from random import randrange

from flask import Flask, Response, render_template
from flask.json import jsonify

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
        return self.app.run(host="0.0.0.0", port="80")

    def add_endpoint(
        self, rule, endpoint=None, view_func=None, handler=None, methods=["GET"]
    ):
        self.app.add_url_rule(
            rule, endpoint=endpoint, view_func=view_func, methods=methods
        )
