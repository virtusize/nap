# -*- coding: utf-8 -*-

from tests.helpers import *
from tests.flask_rest_api_tests.helpers import *
from tests.flask_rest_api_tests.api_fixtures import *
from core.model import Model
from flask_rest_api import ModelView, BaseApiView


def _create_view(model_name):
    model_class = type(model_name, (Model,), {})
    view = BaseApiView(model_class)
    return view


def test_api_init():
    assert_equal(api.url_prefix, '/api/v1')
    assert_equal(api.name, 'api')
    assert_equal(api.import_name, 'api')


def test_base_api_view_endpoint():
    assert_is_instance(_create_view('AwesomeOctopus'), BaseApiView)

    assert_equal(_create_view('Store').endpoint, '/stores/')
    assert_equal(_create_view('AwesomeOctopus').endpoint, '/awesome-octopi/')
    assert_equal(_create_view('GreyhoundDog').endpoint, '/greyhound-dogs/')
    assert_equal(_create_view('Person').endpoint, '/people/')


def test_implicit_model_controller_get():
    c = app.test_client()

    assert_is_not_none(c.get('/api/v1/product-types/').json)
    assert_equal(len(c.get('/api/v1/product-types/').json), 3)

    assert_is_not_none(c.get('/api/v1/product-types/1').json)
    assert_equal(c.get('/api/v1/product-types/1').json['name'], 'dress')
    assert_equal(c.get('/api/v1/product-types/3').json['name'], 'pants')

