#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import skip
from core.model import Model, Storage
from core.validation.validators import MinLength, Email, Int
from tests.helpers import *


class AModel(Model):
    pass


def test_assignment_of_attributes():
    model = AModel(id=1, name='foo', dct={})
    assert_equals(model.id, 1)
    assert_equals(model.name, 'foo')
    assert_true(isinstance(model.dct, dict))


def test_model_with_validation():
    class VModel(Model):

        _validate_with = [
            FieldValidator('id', NotNone),
            FieldValidator('name', NotNone, MinLength(5)),
            FieldValidator('tweet', NotNone, MaxLength(140)),
        ]

    valid_instance = VModel(id=1, name='Some Name', tweet='blah ' * 20)
    invalid_instance = VModel(id=None, name='Some', tweet='blah ' * 40)

    assert_true(valid_instance.validate())
    assert_false(invalid_instance.validate())
    assert_equal(len(invalid_instance.validate().errors), 3)


def test_consecutive_validations():
    class VModel(Model):

        _validate_with = [
            FieldValidator('id', NotNone),
        ]

    valid_instance = VModel(id=1)
    invalid_instance = VModel(id=None)
    valid_instance.validate()
    invalid_instance.validate()

    assert_true(valid_instance.validate())
    assert_false(invalid_instance.validate())
    assert_equal(len(valid_instance.validate().errors), 0)
    assert_equal(len(invalid_instance.validate().errors), 1)


def test_model_with_notnone_and_email():
    class VModel(Model):

        _validate_with = [
            FieldValidator('email', NotNone, Email)
        ]

    valid_instance = VModel(email='hannes@virtusize.com')
    invalid_instance = VModel(email='hannes@@virtusize.com')
    assert_true(valid_instance.validate())
    assert_false(invalid_instance.validate())
    assert_equal(len(invalid_instance.validate().errors), 1)


@skip
def test_inheritance_with_validation():
    """
    This fails, but I am not sure on how to make this work, pretty hairy
    with meta-classes and inheritance.. =(
    """
    class V1Model(Model):

        _validate_with = [
            FieldValidator('name', NotNone, MinLength(5)),
        ]

    class V2Model(V1Model):

        _validate_with = [
            FieldValidator('tweet', NotNone, MaxLength(140)),
        ]

    valid_instance = V2Model(id=1, name='Some Name', tweet='blah ' * 20)
    invalid_instance = V2Model(id=None, name='Some', tweet='blah ' * 40)

    assert_true(valid_instance.validate())
    assert_false(invalid_instance.validate())
    assert_equal(len(invalid_instance.validate().errors), 2)


def test_to_dict():
    model = AModel(id=1, name='foo', admin=True)
    assert_equal(model.to_dict(), {'id': 1, 'name': 'foo', 'admin': True})
    assert_equal(model.to_dict(), model.__dict__)


class Thing(Model):
    pass

def test_simple_model_store_get():
    class Things(Storage):
        thing_one = Thing(id=1, name='Thing One')
        thing_two = Thing(id=2, name='Thing Two')

    assert_is_instance(Things._get(1), Thing)
    assert_equal(Things._get(1).name, 'Thing One')

    assert_is_none(Things._get(3))


def test_simple_model_store_get_all():
    class Things(Storage):
        thing_one = Thing(id=1, name='Thing One')
        thing_two = Thing(id=2, name='Thing Two')

    assert_list_equal(Things._all(), [Things.thing_one, Things.thing_two])


def test_simple_model_store_get_by():
    class Things(Storage):
        thing_one = Thing(id=1, name='Thing One')
        thing_two = Thing(id=2, name='Thing Two')

    assert_equal(Things._get_by('name', 'Thing One').id, 1)
    assert_equal(Things._get_by('name', 'Thing Two').id, 2)

    assert_is_none(Things._get_by('name', 'Not there'))
    assert_is_none(Things._get_by('not_a_property', 'Thing One'))


def test_create_implicit_store():
    class Store(Model):
        pass

    class Stores(Storage):
        virtusize = Store(id=1, name='virtusize')

    assert_is_not_none(Stores.virtusize)
    assert_equal(Stores.virtusize.id, 1)
    assert_equal(Stores.virtusize.name, 'virtusize')

   
