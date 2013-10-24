# -*- coding: utf-8 -*-
from flask import g
from unittest import skip

from tests.fixtures import Stores, Users, fixture_loader
from tests.flask_nap_tests.fixtures import app, an_api
from tests.helpers import *

from nap.model import Model
from nap_client.nap_client import NapClient, HttpNapClient


def test_nap_client():
    with db(), fixtures(Stores, Users, fixture_loader=fixture_loader):
        nc = NapClient(app, an_api, token='123xyz')
        _do_test(nc)
        _do_test_500(nc)


def test_call():
    with db(), fixtures(Stores, Users, fixture_loader=fixture_loader):
        nc = NapClient(app, an_api, token='123xyz')

        response = nc.call('User')
        assert_equal(len(response), 2)

        response = nc.call('User', Users.jane.id)
        assert_equal(response.name, 'Jane')


#@skip
def test_http_nap_client():
    nc = HttpNapClient('http://local.virtusize.com:5000/api/v1/', token='123xyz')
    _do_test(nc)
    _do_test_500(nc)


def _do_test(nc):
    response = nc.index('ProductType')
    assert_equal(len(response), 3)
    assert_equal(response[0]._resource, 'ProductType')

    response = nc.get('ProductType', 1)
    assert_equal(response.name, 'dress')
    assert_equal(response._resource, 'ProductType')

    response = nc.index('Store')
    assert_equal(len(response), 3)

    response = nc.get('Store', 1)
    assert_equal(response.name, 'Virtusize Demo Store')
    assert_equal(response._resource, 'Store')

    response = nc.index('User')
    assert_equal(len(response), 2)

    response = nc.get('User', 1)
    assert_equal(response.name, 'John')
    assert_equal(response._resource, 'User')

    response = nc.post('Store', {'name': 'A new store is born', 'owner_id': 1})
    assert_equal(response.name, 'A new store is born')

    response = nc.query('Store', {'name': 'A new store is born'})
    assert_equal(len(response), 1)
    assert_equal(response[0].name, 'A new store is born')
    assert_equal(response[0].owner_id, 1)
    assert_equal(response[0].active, True)

    store = response[0]

    response = nc.put('Store', store.id, {'name': 'A different new store is born'})
    assert_equal(response.name, 'A different new store is born')

    response = nc.patch('Store', store.id, {'owner_id': 2})
    assert_equal(response.name, 'A different new store is born')

    store = nc.query('Store', {'name': 'A different new store is born'})[0]
    assert_equal(store.name, 'A different new store is born')
    assert_equal(store.owner_id, 2)

    store.name = 'Another kinda new store'
    response = nc.save(store)

    response = nc.delete('Store', store.id)
    assert_equal(response.name, 'Another kinda new store')

    response = nc.get('Store', store.id)
    assert_equal(response.status_code, 404)

    new_store = Model(name='A savable Store', owner_id=2, _resource='Store')
    response = nc.save(new_store)
    assert_equal(response.name, 'A savable Store')
    assert_greater(response.id, 3)

    nc.delete('Store', response.id)

    stores = nc.index('Store')
    assert_equal(len(stores), 3)

    response = nc.save(stores)
    compare(response, stores)


@raises(Exception)
def _do_test_500(nc):
    nc.post('Store', {'not_existent': 'boo'})
