# -*- coding: utf-8 -*-


from core.validation import ValidationResult
from tests.helpers import *

from core.validation.validators import IsNone, MinLength, MaxLength, IsType, Int, NotEmpty


def assert_value_validator(validator_instance, value, expected):
    result = ValidationResult(validator_instance.validate(None, 'test_field', value))
    assert_equals(bool(result), expected)


def test_value_validators():
    cases = [
        (IsNone(), None, True),
        (IsNone(), '', False),
        (NotNone(), None, False),
        (NotNone(), '', True),
        (MaxLength(100), True, False),
        (MaxLength(0), '', True),
        (MaxLength(1), '', True),
        (MaxLength(2), '', True),
        (MaxLength(2), '_' * 3, False),
        (MinLength(100), True, False),
        (MinLength(2), '_' * 3, True),
        (MinLength(2), '_' * 2, True),
        (MinLength(2), '_', False),
        (MinLength(2), '', False),
        (IsType(str), '', True),
        (IsType(str), u'', False),
        (IsType(bool), '', False),
        (IsType(unicode), '', False),
        (IsType(unicode), u'', True),
        (IsType(basestring), '', True),
        (IsType(basestring), u'', True),
        (Int(), '', False),
        (Int(), u'', False),
        (Int(), '10', False),
        (Int(), u'10', False),
        (Int(), 10, True),
        (Int(min=11), 10, False),
        (Int(max=9), 10, False),
        (Int(min=1, max=9), 7, True),
        (Int(min=1, max=9), 1, True),
        (Int(min=1, max=9), 9, True),
        (NotEmpty(), '_', True),
        (NotEmpty(), None, False),
        (NotEmpty(), '', False),
        (NotEmpty(), 1123, True),
        (NotEmpty(), ' ', True),
        (NotEmpty(), 0, True),
        (NotEmpty(), [], False),
        (NotEmpty(), ["_"], True),
        (NotEmpty(), {}, False),
        (NotEmpty(), {1: '_'}, True),
        (NotEmpty(), False, True),
        (NotEmpty(), True, True),
    ]

    for case in cases:
        yield (assert_value_validator,) + case
