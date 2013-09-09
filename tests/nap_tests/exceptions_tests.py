# -*- coding: utf-8 -*-

from nap.exceptions import NapException, ModelNotFoundException, ModelInvalidException
from tests.helpers import compare


def test_nap_exception():
    ne = NapException()
    compare(str(ne), u"{'message': 'NapException'}")

    ne = NapException('A nice message')
    compare(str(ne), u"{'message': 'A nice message'}")

    ne = NapException('A nice message', some='some123', values='values321')
    compare(str(ne), u"{'some': 'some123', 'message': 'A nice message', 'values': 'values321'}")


def test_model_not_found_exception():
    ne = ModelNotFoundException(model_name='User', model_id=1)
    compare(str(ne), u"{'model_id': 1, 'message': 'Model not found.', 'model_name': 'User'}")


def test_model_invalid_exception():
    ne = ModelInvalidException(model_name='User', errors=['Field missing'])
    compare(str(ne), u"{'message': 'Model is invalid.', 'errors': ['Field missing'], 'model_name': 'User'}")


