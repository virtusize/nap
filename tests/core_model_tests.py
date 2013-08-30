#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import skip
from core.model import SimpleModel
from core.validation.validators import MinLength, Email
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
