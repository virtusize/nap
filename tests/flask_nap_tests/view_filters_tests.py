# -*- coding: utf-8 -*-

from nap.authorization import Identity, Role, Guard
from nap.util import Context
from flask_nap.view_filters import Filter, CamelizeFilter, ExcludeFilter, ExcludeActionFilter, KeyFilter

from tests.helpers import *


@raises(NotImplementedError)
def test_filter():
    Filter().filter({}, {})


def test_key_filter():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    def do_something_weird(key):
        return key.upper() + '_k'

    result = KeyFilter(do_something_weird).filter(dct, ctx=Context())

    assert_equal(result['NAME_k'], dct['name'])
    assert_equal(result['FULL_NAME_k'], dct['full_name'])
    assert_equal(result['FAVORITE_STORE_PRODUCT_ID_k'], dct['favorite_store_product_id'])


def test_camelize():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    result = CamelizeFilter().filter(dct, ctx=Context())

    assert_equal(result['name'], dct['name'])
    assert_equal(result['fullName'], dct['full_name'])
    assert_equal(result['favoriteStoreProductId'], dct['favorite_store_product_id'])


def test_exclude():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'favorite_store_product_id': 123
    }

    result = ExcludeFilter(exclude=['favorite_store_product_id']).filter(dct, ctx=Context())

    assert_equal(result['name'], dct['name'])
    assert_equal(result['full_name'], dct['full_name'])
    assert_false('favorite_store_product_id' in result)


def test_exclude_action_filter():

    dct = {
        'name': 'John',
        'full_name': 'John Doe',
        'secret': 123
    }

    role = Role()
    role.grant('read_secrets', 'user')

    valid_identity = Identity([role])
    invalid_identity = Identity([])

    ctx = Context()
    ctx.subject = 'user'
    ctx.identity = valid_identity

    result = ExcludeActionFilter(
        exclude=['secret'],
        action='read_secrets',
        guard=Guard()
    ).filter(dct, ctx)

    assert_true('secret' in result)
    assert_equal(result['secret'], 123)

    ctx.identity = invalid_identity

    result = ExcludeActionFilter(
        exclude=['secret'],
        action='read_secrets',
        guard=Guard()
    ).filter(dct, ctx)

    assert_false('secret' in result)
