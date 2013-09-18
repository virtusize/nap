# -*- coding: utf-8 -*-
from flask.json import JSONEncoder

from tests.helpers import *
from tests.flask_nap_tests.helpers import *
from tests.fixtures import Users, Stores, fixture_loader


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


def test_unauthorized():
    with db(), fixtures(Users, fixture_loader=fixture_loader):

        c = app.test_client()

        response = c.get('/api/v1/users/1')
        assert_equal(response.status_code, 403)

        response = response.json
        assert_equal(response['status_code'], 403)
        assert_equal(response['model_name'], 'User')
        assert_equal(response['message'], 'Unauthorized.')


def test_not_found_exception():
    c = app.test_client()
    response = c.get('/api/v1/not-existent/1')

    assert_equal(response.status_code, 404)

    response = response.json
    assert_equal(response['status_code'], 404)
    assert_equal(response['message'], 'Not Found')


def test_wrong_call_exception():
    c = app.test_client()

    response = c.post('/api/v1/stores/', **with_json_data({'not_existent': 'Something'}))

    assert_equal(response.status_code, 500)

    response = response.json
    assert_equal(response['status_code'], 500)
    assert_equal(response['message'], "u'not_existent' is an invalid keyword argument for Store")


def test_invalid_json_exception():
    c = app.test_client()

    response = c.post('/api/v1/stores/', data="really=wrong", content_type='application/json')

    assert_equal(response.status_code, 400)

    response = response.json
    assert_equal(response['status_code'], 400)


def test_invalid_mimetype_exception():
    c = app.test_client()

    data = JSONEncoder().encode({'valid': 'json'})
    response = c.post('/api/v1/stores/', data=data, content_type='text/xml')
    print response

    assert_equal(response.status_code, 415)

    response = response.json
    assert_equal(response['status_code'], 415)
