# -*- coding: utf-8 -*-

import flask

from tests.helpers import *
from core.model import SimpleModel, ImplicitModelStore
from flask_rest_api import Api, ModelController, ImplicitModelController


class Store(SimpleModel):
    pass

api = Api('api', '/api', 1)


class Stores(ImplicitModelStore):
    store1 = Store(id=1, name='store1')
    store2 = Store(id=2, name='store2')
    store3 = Store(id=3, name='store3')


class StoreController(ImplicitModelController):
    model = Store
    store = Stores

StoreController.register_on(api)

app = flask.Flask(__name__)

app.register_blueprint(api)


def _create_controller(model_name):
    model_class = type(model_name, (Model,), {}) 
    controller_class = type(model_name + 'Controller', (ModelController,), dict(model=model_class)) 
    return controller_class


def test_api_init():
    assert_equal(api.url_prefix, '/api/v1')
    assert_equal(api.name, 'api')
    assert_equal(api.import_name, 'api')


def test_controller_init():
    assert_equal(_create_controller('Store').endpoint(), '/stores/')


def test_model_controller_endpoint():
    assert_is_instance(_create_controller('AwesomeOctopus')(), ModelController)

    assert_equal(_create_controller('AwesomeOctopus').endpoint(), '/awesome-octopi/')
    assert_equal(_create_controller('GreyhoundDog').endpoint(), '/greyhound-dogs/')
    assert_equal(_create_controller('Person').endpoint(), '/people/')


def test_implicit_model_controller_get():
    c = app.test_client()

    assert_is_not_none(c.get('/api/v1/stores/').data)

    assert_is_not_none(c.get('/api/v1/stores/1').data)

