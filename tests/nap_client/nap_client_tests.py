# -*- coding: utf-8 -*-
from flask import g
from unittest import skip

from tests.fixtures import Stores, Users, fixture_loader
from tests.flask_nap_tests.fixtures import app, an_api
from tests.helpers import *

from nap_client.nap_client import NapClient, HttpNapClient


def test_nap_client():
    with db(), fixtures(Stores, Users, fixture_loader=fixture_loader):
        nc = NapClient(app, an_api, token='123xyz')
        _do_test(nc)
        _do_test_500(nc)


@skip
def test_http_nap_client():
    nc = HttpNapClient('http://local.virtusize.com:5000/api/v1/', token='123xyz')
    _do_test(nc)
    _do_test_500(nc)


def _do_test(nc):
    response = nc.index('ProductType')
    assert_equal(len(response), 3)

    response = nc.get('ProductType', 1)
    assert_equal(response.name, 'dress')

    response = nc.index('Store')
    assert_equal(len(response), 3)

    response = nc.get('Store', 1)
    assert_equal(response.name, 'Virtusize Demo Store')

    response = nc.index('User')
    assert_equal(len(response), 2)

    response = nc.get('User', 1)
    assert_equal(response.name, 'John')

    response = nc.post('Store', {'name': 'A new store is born', 'ownerId': 1})
    assert_equal(response.name, 'A new store is born')

    response = nc.query('Store', {'name': 'A new store is born'})
    assert_equal(len(response), 1)
    assert_equal(response[0].name, 'A new store is born')
    assert_equal(response[0].ownerId, 1)
    assert_equal(response[0].active, True)

    store = response[0]

    response = nc.put('Store', store.id, {'name': 'A different new store is born'})
    assert_equal(response.name, 'A different new store is born')

    response = nc.patch('Store', store.id, {'ownerId': 2})
    assert_equal(response.name, 'A different new store is born')

    response = nc.query('Store', {'name': 'A different new store is born'})
    assert_equal(len(response), 1)
    assert_equal(response[0].name, 'A different new store is born')
    assert_equal(response[0].ownerId, 2)

    response = nc.delete('Store', store.id)
    assert_equal(response.name, 'A different new store is born')

    response = nc.get('Store', store.id)
    if hasattr(response, 'statusCode'):
        assert_equal(response.statusCode, 404)
    else:
        assert_equal(response.status_code, 404)


@raises(Exception)
def _do_test_500(nc):
    nc.post('Store', {'notExistent': 'boo'})
