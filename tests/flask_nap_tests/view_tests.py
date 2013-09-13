# -*- coding: utf-8 -*-
from flask_nap.view import BaseView, ModelView, route, InvalidRuleError

from nap.model import Model
from sa_nap.model import SAModelSerializer

from tests.helpers import *
from tests.flask_nap_tests.helpers import *
from tests.flask_nap_tests.fixtures import UserView, UserController
from tests.fixtures import Stores, Users, fixture_loader


def test_base_view():
    class SomeView(BaseView):
        endpoint_prefix = 'st'

        @route('/something/')
        def something(self):
            return 'Some thing'

    v = SomeView()
    v._route_options = {}
    v._register_on(app)

    urls = app.url_map.bind('example.com', '/')

    compare(urls.match('/something/', 'GET'), ('st_something', {}))
    assert_equal(app.view_functions['st_something']().data, 'Some thing')
    assert_is_not_none(app.view_functions['st_something'])


@raises(InvalidRuleError)
def test_base_view_invalid_route():
    class SomeView(BaseView):
        endpoint_prefix = 'st'

        @route(None)
        def something(self):
            return 'Some thing'

    v = SomeView()
    v._route_options = {}
    v._register_on(app)


def test_base_api_view_endpoint():
    class AView(ModelView):
        controller = UserController
        filter_chain = []
        serializer = SAModelSerializer

    class AwesomeOctopus(Model):
        pass
    AView.controller.model = AwesomeOctopus
    view = AView()
    assert_equal(view.endpoint_prefix, 'awesome_octopi')
    assert_equal(view.dashed_endpoint, 'awesome-octopi')

    class GreyhoundDog(Model):
        pass
    AView.controller.model = GreyhoundDog
    view = AView()
    assert_equal(view.endpoint_prefix, 'greyhound_dogs')
    assert_equal(view.dashed_endpoint, 'greyhound-dogs')

    class Person(Model):
        pass
    AView.controller.model = Person
    view = AView()
    assert_equal(view.endpoint_prefix, 'people')
    assert_equal(view.dashed_endpoint, 'people')

    class Store(Model):
        pass
    AView.controller.model = Store
    view = AView()
    assert_equal(view.endpoint_prefix, 'stores')
    assert_equal(view.dashed_endpoint, 'stores')


@raises(TypeError)
def test_model_view_apply_filter_not_a_base_model():
    class NotAModel(object):
        pass

    view = UserView()
    view.filter(NotAModel())


def test_model_view_get_and_index():
    c = app.test_client()

    response = c.get('/api/v1/product-types/')
    assert_equal(response.status_code, 200)
    assert_is_not_none(response.json)
    assert_equal(len(c.get('/api/v1/product-types/').json), 3)

    assert_is_not_none(c.get('/api/v1/product-types/1').json)
    assert_equal(c.get('/api/v1/product-types/1').json['name'], 'dress')
    assert_equal(c.get('/api/v1/product-types/3').json['name'], 'pants')


def test_samodel_view_get_and_index():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.get('/api/v1/stores/')
        assert_equal(response.status_code, 200)
        assert_is_not_none(response.json)
        assert_equal(len(c.get('/api/v1/stores/').json), 3)

        assert_is_not_none(c.get('/api/v1/stores/1').json)
        assert_equal(c.get('/api/v1/stores/1').json['name'], 'Virtusize Demo Store')
        assert_equal(c.get('/api/v1/stores/3').json['name'], 'WeSC')


def test_samodel_view_post():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.post('/api/v1/stores/', **with_json_data({'name': 'New Store', 'owner_id': Users.john.id}))
        assert_equal(response.status_code, 201)

        response = response.json
        assert_is_not_none(response)
        response = c.get('/api/v1/stores/4').json
        assert_equal(response['name'], 'New Store')


def test_samodel_view_put_patch():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        store = c.put('/api/v1/stores/1', **with_json_data({'name': 'Some other name'})).json
        assert_is_not_none(store)

        response = c.get('/api/v1/stores/1')
        assert_equal(response.status_code, 200)

        response = response.json
        compare(response, store)
        assert_equal(response['name'], 'Some other name')

        response = c.patch('/api/v1/stores/1', **with_json_data({'name': 'Yet other name'}))
        assert_equal(response.status_code, 200)

        store = response.json
        assert_is_not_none(store)

        response = c.get('/api/v1/stores/1').json
        compare(response, store)
        assert_equal(response['name'], 'Yet other name')


def test_samodel_view_delete():
    with db(), fixtures(Stores, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.get('/api/v1/stores/1')
        assert_equal(response.status_code, 200)

        store = response.json

        assert_equal(len(c.get('/api/v1/stores/').json), 3)
        response = c.delete('/api/v1/stores/1').json
        assert_is_not_none(response)
        assert_equal(len(c.get('/api/v1/stores/').json), 2)

        compare(store, response)


def test_unauthorized_samodel_view_get_index():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = app.test_client()

        response = c.get('/api/v1/users/')
        assert_equal(response.status_code, 403)
        assert_equal(response.json['model_name'], 'User')
        assert_equal(response.json['message'], 'Unauthorized.')


