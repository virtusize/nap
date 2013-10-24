# -*- coding: utf-8 -*-
from flask import g

from nap.util import Context
from flask_nap.view import BaseView
from flask_nap.api import Api, ApiMixin, Debug, JsonRequestParser, InvalidJSONException, InvalidMimetypeException
from tests.flask_nap_tests.fixtures import AnApi
from tests.flask_nap_tests.helpers import app
from tests.helpers import *


def test_api_init():
    an_api = AnApi()
    assert_equal(an_api.url_prefix, '/api/v1')
    assert_equal(an_api.name, 'api')
    assert_equal(an_api.import_name, 'api')


def test_api_mixin():
    mixin = ApiMixin()
    mixin.before()


def test_debug_mixin():
    with app.test_request_context('/'):
        assert_is_none(g.get('debug'))

        mixin = Debug()
        mixin.before()
        assert_true(g.get('debug'))

        mixin.after({})


def test_json_request_parser_valid_json():

    data = {'one': 1, 'two': '2', u'äåö': u'-.öäå'}

    import json

    with app.test_request_context('/?one=1', content_type='application/json', data=json.dumps(data)):
        g.ctx = Context()

        mixin = JsonRequestParser()
        mixin.before()

        compare(g.ctx.input, data)


@raises(InvalidMimetypeException)
def test_json_request_parser_valid_json_but_invalid_content_type():

    data = {'one': 1, 'two': '2', u'äåö': u'-.öäå'}

    import json

    with app.test_request_context('/?one=1', content_type='text/json', data=json.dumps(data)):
        g.ctx = Context()

        mixin = JsonRequestParser()
        mixin.before()


@raises(InvalidJSONException)
def test_json_request_parser_invalid_json_with_valid_content_type():

    with app.test_request_context('/?one=1', content_type='application/json', data='{"one": 1, "two": "2", "äåö": -.öäå"}'):
        g.ctx = Context()

        mixin = JsonRequestParser()
        mixin.before()
