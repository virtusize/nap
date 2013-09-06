# -*- coding: utf-8 -*-
from inflection import underscore, pluralize
from flask.ext.nap.view import BaseApiView, KeyFilter, CamelizeFilter, ExcludeFilter

from tests.helpers import *
from tests.flask_nap_tests.helpers import *
from tests.fixtures import Stores, Users, fixture_loader


def _create_view(model_name):
    view = BaseApiView(underscore(pluralize(model_name)))
    return view


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


def test_key_filter():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    def do_something_weird(key):
        return key.upper() + '_k'

    result = KeyFilter(do_something_weird).filter(dct)

    assert_equal(result['NAME_k'], dct['name'])
    assert_equal(result['FULL_NAME_k'], dct['full_name'])
    assert_equal(result['FAVORITE_STORE_PRODUCT_ID_k'], dct['favorite_store_product_id'])


def test_camelize():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    result = CamelizeFilter().filter(dct)

    assert_equal(result['name'], dct['name'])
    assert_equal(result['fullName'], dct['full_name'])
    assert_equal(result['favoriteStoreProductId'], dct['favorite_store_product_id'])


def test_exclude():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    result = ExcludeFilter(exclude=['favorite_store_product_id']).filter(dct)

    assert_equal(result['name'], dct['name'])
    assert_equal(result['full_name'], dct['full_name'])
    assert_false('favorite_store_product_id' in result)
