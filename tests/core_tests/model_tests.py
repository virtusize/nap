#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import skip
from core.model import SimpleModel, SimpleModelStore
from core.validation.validators import MinLength, Email, Int
from tests.helpers import *


class AModel(SimpleModel):
    pass


def test_assignment_of_attributes():
    model = AModel(id=1, name='foo', dct={})
    assert_equals(model.id, 1)
    assert_equals(model.name, 'foo')
    assert_true(isinstance(model.dct, dict))


def test_model_with_validation():
    class VModel(SimpleModel):

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
    class VModel(SimpleModel):

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
    class VModel(SimpleModel):

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
    class V1Model(SimpleModel):

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


def test_api_name():
    class AwesomeOctopus(SimpleModel):
        pass
    assert_equal(AwesomeOctopus.api_name(), 'awesome_octopi')

    class GreyhoundDog(SimpleModel):
        pass
    assert_equal(GreyhoundDog.api_name(), 'greyhound_dogs')

    class Person(SimpleModel):
        pass
    assert_equal(Person.api_name(), 'people')


class Thing(SimpleModel):

    _validate_with = [
        FieldValidator('id', NotNone, Int)
    ]


class Things(SimpleModelStore):
    pass


def test_simple_model_store_create():
    things = Things(Thing)
    assert_equal(things.count(), 0)


def test_simple_model_store_add():
    things = Things(Thing)
    thing_one = Thing(id=1, name='Thing One')
    thing_two = Thing(id=2, name='Thing Two')

    things.add(thing_one)
    assert_equal(things.count(), 1)

    things.add(thing_two)
    assert_equal(things.count(), 2)

    things.add(thing_two)
    assert_equal(things.count(), 2)


def test_simple_model_store_add_all():
    things = Things(Thing)
    thing_one = Thing(id=1, name='Thing One')
    thing_two = Thing(id=2, name='Thing Two')

    things.add_all([thing_one, thing_two])
    assert_equal(things.count(), 2)

    things.add_all([thing_one, thing_two])
    assert_equal(things.count(), 2)


def test_simple_model_store_get():
    things = Things(Thing)
    thing_one = Thing(id=1, name='Thing One')
    thing_two = Thing(id=2, name='Thing Two')

    things.add_all([thing_one, thing_two])

    assert_is_instance(things.get(1), Thing)
    assert_equal(things.get(1).name, 'Thing One')


def test_simple_model_store_get_all():
    things = Things(Thing)
    thing_one = Thing(id=1, name='Thing One')
    thing_two = Thing(id=2, name='Thing Two')

    things.add_all([thing_one, thing_two])

    assert_list_equal(things.get_all(), [thing_one, thing_two])


def test_simple_model_store_get_by():
    things = Things(Thing)
    thing_one = Thing(id=1, name='Thing One')
    thing_two = Thing(id=2, name='Thing Two')

    things.add_all([thing_one, thing_two])

    assert_equal(things.get_by('name', 'Thing One').id, 1)
    assert_equal(things.get_by('name', 'Thing Two').id, 2)

    assert_is_none(things.get_by('name', 'Not there'))
    assert_is_none(things.get_by('not_a_property', 'Thing One'))


@raises(TypeError)
def test_simple_model_store_add_wrong_model():
    things = Things(Thing)
    wrong_model = AModel(id=1, name='Plain wrong')

    things.add(wrong_model)


@raises(TypeError)
def test_simple_model_store_add_all_wrong_model():
    things = Things(Thing)
    wrong_model = AModel(id=1, name='Plain wrong')

    things.add_all([wrong_model])


@raises(AttributeError)
def test_simple_model_store_missing_id():
    things = Things(Thing)
    model = Thing(name='Missing something')

    things.add(model)
