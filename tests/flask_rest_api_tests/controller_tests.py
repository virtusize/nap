# -*- coding: utf-8 -*-

import flask

from tests.helpers import *
from core.model import SimpleModel
from flask_rest_api import Api, Controller


class Store(SimpleModel):
    pass

api = Api('api', '/api', 1)

controller = Controller(model=Store)
api.add_controller(controller)

app = flask.Flask(__name__)

app.register_blueprint(api)


def test_api_init():
    assert_equal(api.url_prefix, '/api/v1')
    assert_equal(api.name, 'api')
    assert_equal(api.import_name, 'api')


def test_controller_init():
    assert_equal(controller.endpoint, '/stores/')


