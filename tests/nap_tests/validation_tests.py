# -*- coding: utf-8 -*-

from nap.validation import ValidationResult, ModelValidator, ValueValidator, ValidationMixin
from tests.helpers import *


@raises(NotImplementedError)
def test_model_validator():
    mv = ModelValidator()
    mv.validate(None)


@raises(NotImplementedError)
def test_value_validator():
    mv = ValueValidator()
    mv.validate(None, None, None)


def test_validation_result():
    vr = ValidationResult([])
    assert_true(vr.valid)

    errors = ['Some error occurred.']
    vr = ValidationResult(errors)
    assert_false(vr.valid)

    assert_equal(str(vr), 'ValidationResult: False\nErrors:\nSome error occurred.')


def test_validation_mixin():
    vm = ValidationMixin()

    assert_is_instance(vm.validate(), ValidationResult)
    assert_true(vm.validate().valid)
