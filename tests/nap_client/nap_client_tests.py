# -*- coding: utf-8 -*-
from flask import g
from unittest import skip

from tests.fixtures import Stores, Users, fixture_loader
from tests.flask_nap_tests.fixtures import app, an_api
from tests.helpers import *

from nap.model import Model
from nap_client.nap_client import NapClient, HttpNapClient, Response


def test_response():
    r = Response('Gnarf', {'hi': 'ho'}, 200)
    assert_true(r.successful)
    assert_true(r.successful != r.error)
    assert_equal(r.first.hi, 'ho')
    assert_is_instance(r.first, Model)
    assert_equal(len(r), 1)
    compare(r.first, r[0])

    assert_equal(str(r), "{'status': 200, 'raw_data': {'hi': 'ho'}, 'resource': 'Gnarf', 'data': Model(**{'hi': 'ho'})}")
    assert_equal(repr(r), "Response(**{'status': 200, 'raw_data': {'hi': 'ho'}, 'resource': 'Gnarf', 'data': Model(**{'hi': 'ho'})})")

    r2 = Response('Gnarf', {'hi': 'ho'}, 200)
    r2._gnarf = 'does not matter'
    assert_equal(r, r2)

    r2 = Response('Gnarf', {'hi': 'ho2'}, 200)
    assert_not_equal(r, r2)


def test_response_error():
    r = Response('Gnarf', {'message': 'something'}, 300)
    assert_false(r.successful)
    assert_true(r.successful != r.error)
    assert_equal(len(r), 0)
    assert_is_none(r.first)
    assert_is_none(r[0])
    assert_equal(r.error.message, 'something')


def test_response_empty():
    r = Response('Gnarf', [], 200)
    assert_true(r.successful)
    assert_equal(len(r), 0)
    assert_is_none(r.first)

    r = Response('Gnarf', None, 200)
    assert_true(r.successful)
    assert_equal(len(r), 0)
    assert_is_none(r.first)

def test_not_equal_class():
    x = Response('Gnarf', None, 200)
    y = Model(hi='ho')

    assert_true(x != y)
    assert_false(x == y)


def test_nap_client():
    with db(), fixtures(Stores, Users, fixture_loader=fixture_loader):
        nc = NapClient(app, an_api, token='123xyz')
        _do_test(nc)
        _do_test_500(nc)


def test_call():
    with db(), fixtures(Stores, Users, fixture_loader=fixture_loader):
        nc = NapClient(app, an_api, token='123xyz')

        response = nc.call('User')
        assert_true(response.successful)
        assert_equal(len(response), 2)

        response = nc.call('User', Users.jane.id)
        assert_true(response.successful)
        assert_equal(response.first.name, 'Jane')


@skip
def test_http_nap_client():
    nc = HttpNapClient('http://local.virtusize.com:5000/api/v1/', token='123xyz')
    _do_test(nc)
    _do_test_500(nc)


def _do_test(nc):
    response = nc.index('ProductType')
    assert_true(response.successful)
    assert_equal(len(response), 3)
    assert_equal(response.first._resource, 'ProductType')

    response = nc.get('ProductType', 1)
    assert_true(response.successful)
    assert_equal(response.first.name, 'dress')
    assert_equal(response.resource, 'ProductType')

    response = nc.index('Store')
    assert_true(response.successful)
    assert_equal(len(response), 3)

    response = nc.get('Store', 1)
    assert_true(response.successful)
    assert_equal(response.first.name, 'Virtusize Demo Store')
    assert_equal(response.resource, 'Store')

    response = nc.index('User')
    assert_true(response.successful)
    assert_equal(len(response), 2)

    response = nc.get('User', 1)
    assert_true(response.successful)
    assert_equal(response.first.name, 'John')
    assert_equal(response.resource, 'User')

    response = nc.post('Store', {'name': 'A new store is born', 'owner_id': 1})
    assert_true(response.successful)
    assert_equal(response.first.name, 'A new store is born')

    response = nc.query('Store', {'name': 'A new store is born'})
    assert_true(response.successful)
    assert_equal(len(response), 1)
    assert_equal(response.first.name, 'A new store is born')
    assert_equal(response.first.owner_id, 1)
    assert_equal(response.first.active, True)

    store = response.first

    response = nc.put('Store', store.id, {'name': 'A different new store is born'})
    assert_true(response.successful)
    assert_equal(response.first.name, 'A different new store is born')

    response = nc.patch('Store', store.id, {'owner_id': 2})
    assert_true(response.successful)
    assert_equal(response.first.name, 'A different new store is born')

    response = nc.query('Store', {'name': 'A different new store is born'})
    assert_true(response.successful)

    store = response.first
    assert_equal(store.name, 'A different new store is born')
    assert_equal(store.owner_id, 2)

    store.name = 'Another kinda new store'
    response = nc.save(store)
    assert_true(response.successful)

    response = nc.delete('Store', store.id)
    assert_true(response.successful)
    assert_equal(response.first.name, 'Another kinda new store')

    response = nc.get('Store', store.id)
    assert_false(response.successful)
    assert_equal(response.status, 404)

    new_store = Model(name='A savable Store', owner_id=2, _resource='Store')
    response = nc.save(new_store)
    assert_true(response.successful)
    assert_equal(response.first.name, 'A savable Store')
    assert_greater(response.first.id, 3)

    nc.delete('Store', response.first.id)

    response = nc.index('Store')
    assert_true(response.successful)
    assert_equal(len(response), 3)

    stores = response.data

    responses = nc.save(stores)
    assert_true(all([item.successful for item in responses]))
    compare([item.data for item in responses], stores)


@raises(Exception)
def _do_test_500(nc):
    nc.post('Store', {'not_existent': 'boo'})
