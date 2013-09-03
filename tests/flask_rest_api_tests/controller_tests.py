# -*- coding: utf-8 -*-

import flask

from tests.helpers import *
from core.model import Model, Storage
from flask_rest_api import Api, ModelView, ImplicitModelView


class Store(Model):
    pass

api = Api('api', '/api', 1)


class Stores(Storage):
    store1 = Store(id=1, name='store1')
    store2 = Store(id=2, name='store2')
    store3 = Store(id=3, name='store3')


class StoreController(ImplicitModelView):
    model = Store
    store = Stores


StoreController.register_on(api)

app = flask.Flask(__name__)

app.register_blueprint(api)


def _create_view(model_name):
    model_class = type(model_name, (Model,), {}) 
    view_class = type(model_name + 'View', (ModelView,), dict(model=model_class)) 
    return view_class


def test_api_init():
    assert_equal(api.url_prefix, '/api/v1')
    assert_equal(api.name, 'api')
    assert_equal(api.import_name, 'api')


def test_controller_init():
    assert_equal(_create_view('Store').endpoint(), '/stores/')


def test_model_controller_endpoint():
    assert_is_instance(_create_view('AwesomeOctopus')(), ModelView)

    assert_equal(_create_view('AwesomeOctopus').endpoint(), '/awesome-octopi/')
    assert_equal(_create_view('GreyhoundDog').endpoint(), '/greyhound-dogs/')
    assert_equal(_create_view('Person').endpoint(), '/people/')


def test_implicit_model_controller_get():
    c = app.test_client()

    assert_is_not_none(c.get('/api/v1/stores/').data)

    assert_is_not_none(c.get('/api/v1/stores/1').data)

