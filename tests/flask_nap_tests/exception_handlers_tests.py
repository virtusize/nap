# -*- coding: utf-8 -*-
from tests.helpers import *
from tests.flask_nap_tests.helpers import *
from tests.fixtures import Stores, fixture_loader


def test_unsupported_method():
    c = app.test_client()

    response = c.post('/api/v1/product-types/', **with_json_data({'name': 'New ProductType'}))
    assert_equal(response.status_code, 405)

    response = response.json
    assert_equal(response['status_code'], 405)
    assert_equal(response['model_name'], 'ProductType')
    assert_equal(response['message'], 'Method not supported.')


def test_model_not_found():
    c = app.test_client()

    response = c.get('/api/v1/product-types/9999')
    assert_equal(response.status_code, 404)

    response = response.json
    assert_equal(response['status_code'], 404)
    assert_equal(response['model_id'], 9999)
    assert_equal(response['model_name'], 'ProductType')
    assert_equal(response['message'], 'Model not found.')


def test_sa_model_not_found():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):

        c = app.test_client()

        response = c.get('/api/v1/stores/9999')
        assert_equal(response.status_code, 404)

        response = response.json
        assert_equal(response['status_code'], 404)
        assert_equal(response['model_id'], 9999)
        assert_equal(response['model_name'], 'Store')
        assert_equal(response['message'], 'Model not found.')
