# -*- coding: utf-8 -*-

import flask

from tests.helpers import *
from core.model import SimpleModel
from flask_rest_api import Api, Controller


class Store(SimpleModel):
    pass

api = Api('api', '/api', 1)

api.add_controller(Controller(model=Store))

app = flask.Flask(__name__)

app.register_blueprint(api)
