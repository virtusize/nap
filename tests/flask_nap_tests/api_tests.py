# -*- coding: utf-8 -*-
from tests.flask_nap_tests.fixtures import AnApi
from tests.helpers import assert_equal


def test_api_init():
    an_api = AnApi()
    assert_equal(an_api.url_prefix, '/api/v1')
    assert_equal(an_api.name, 'api')
    assert_equal(an_api.import_name, 'api')

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
