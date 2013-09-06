# -*- coding: utf-8 -*-

from flask.json import JSONEncoder

from tests.helpers import *
from tests.flask_rest_api_tests.helpers import *
from tests.flask_rest_api_tests.api_fixtures import *
from nap.model import Model
from flask_rest_api import ModelView, BaseApiView
from tests.core_tests.database_fixtures import Stores, Users, fixture_loader


def _create_view(model_name):
    view = BaseApiView(underscore(pluralize(model_name)))
    return view


def test_api_init():
    assert_equal(api.url_prefix, '/api/v1')
    assert_equal(api.name, 'api')
    assert_equal(api.import_name, 'api')


#def test_base_api_view_endpoint():
    #assert_is_instance(_create_view('AwesomeOctopus'), BaseApiView)

    #assert_equal(_create_view('Store').route_prefix, '/stores/')
    #assert_equal(_create_view('AwesomeOctopus').route_prefix, '/awesome-octopi/')
    #assert_equal(_create_view('GreyhoundDog').route_prefix, '/greyhound-dogs/')
    #assert_equal(_create_view('Person').route_prefix, '/people/')

    #assert_equal(_create_view('Store').endpoint, 'stores')
    #assert_equal(_create_view('AwesomeOctopus').endpoint, 'awesome_octopi')
    #assert_equal(_create_view('GreyhoundDog').endpoint, 'greyhound_dogs')
    #assert_equal(_create_view('Person').endpoint, 'people')


def test_model_view_get_and_index():
    c = app.test_client()

    response = c.get('/api/v1/product-types/')
    assert_is_not_none(response.json)
    assert_equal(len(c.get('/api/v1/product-types/').json), 3)

    assert_is_not_none(c.get('/api/v1/product-types/1').json)
    assert_equal(c.get('/api/v1/product-types/1').json['name'], 'dress')
    assert_equal(c.get('/api/v1/product-types/3').json['name'], 'pants')


def test_samodel_view_get_and_index():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.get('/api/v1/stores/')
        assert_is_not_none(response.json)
        assert_equal(len(c.get('/api/v1/stores/').json), 3)

        assert_is_not_none(c.get('/api/v1/stores/1').json)
        assert_equal(c.get('/api/v1/stores/1').json['name'], 'Virtusize Demo Store')
        assert_equal(c.get('/api/v1/stores/3').json['name'], 'WeSC')


def test_samodel_view_post():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.post('/api/v1/stores/', **with_json_data({'name': 'New Store', 'owner_id': Users.john.id})).json
        assert_is_not_none(response)
        response = c.get('/api/v1/stores/4').json
        assert_equal(response['name'], 'New Store')


def test_samodel_view_put_patch():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        store = c.put('/api/v1/stores/1', **with_json_data({'name': 'Some other name'})).json
        assert_is_not_none(store)

        response = c.get('/api/v1/stores/1').json
        compare(response, store)
        assert_equal(response['name'], 'Some other name')

        store = c.patch('/api/v1/stores/1', **with_json_data({'name': 'Yet other name'})).json
        assert_is_not_none(store)

        response = c.get('/api/v1/stores/1').json
        compare(response, store)
        assert_equal(response['name'], 'Yet other name')


def test_samodel_view_delete():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        store = c.get('/api/v1/stores/1').json

        assert_equal(len(c.get('/api/v1/stores/').json), 3)
        response = c.delete('/api/v1/stores/1').json
        assert_is_not_none(response)
        assert_equal(len(c.get('/api/v1/stores/').json), 2)

        compare(store, response)

