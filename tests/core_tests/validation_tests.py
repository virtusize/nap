# -*- coding: utf-8 -*-

import re

from nap.validation import ValidationResult
from tests.helpers import *

from nap.validation.validators import *


def assert_value_validator(validator_instance, value, expected):
    result = ValidationResult(validator_instance.validate(None, 'test_field', value))

    validator = validator_instance.__class__.__name__

    if expected:
        assert_list_equal(result.errors, [])
        msg = validator + " validation failed with errors: " + str(result.errors)
    else:
        msg = validator + " validation did unexpectedly not fail"

    msg += " for value: %s" % value

    assert_equals(bool(result), expected, msg)


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

        (Regex(re.compile(r"^[a-z]*$")), "abc", True),
        (Regex(r"^[a-z]*$"), "aBc", False),
        (Regex(r"^[\d]*$"), "123", True),
        (Regex(r"^[\d]*$"), "abc", False),
        (Regex(r"^[a-z]*$"), "abc", True),
        (Regex(r"^[a-z]*$"), "aBc", False),

        (PlainText(), "aB12-Xy_Z", True),
        (PlainText(), "!", False),
        (PlainText(), "ab$12", False),

        (Email(), "hannes@virtusize.com", True),
        (Email(), "hannes+a@virtusize.com", True),
        (Email(), "hannes+a+11@virtusize.com", True),
        (Email(), "hannes@virt@usize.com", False),
        (Email(), " hannes@virtusize.com", False),
        (Email(), "hannes@virtusize.com ", False),
        (Email(), "hannes@virt usize.com ", False),
        (Email(), "hannesvirtusize.com", False),

        (Email(), "email@domain.com", True),
        (Email(), "firstname.lastname@domain.com", True),
        (Email(), "email@subdomain.domain.com", True),
        (Email(), "firstname+lastname@domain.com", True),
        #(Email(), "email@123.123.123.123", True), # Should be a valid address, but fails with our regex
        (Email(), "email@[123.123.123.123]", True),
        (Email(), "\"email\"@domain.com", True),
        (Email(), "1234567890@domain.com", True),
        (Email(), "email@domain-one.com", True),
        (Email(), "_______@domain.com", True),
        (Email(), "email@domain.name", True),
        (Email(), "email@domain.co.jp", True),
        (Email(), "firstname-lastname@domain.com", True),

        (Email(), "plainaddress", False),
        (Email(), "#@%^%#$@#$@#.com", False),
        (Email(), "@domain.com", False),
        (Email(), "Joe Smith <email@domain.com>", False),
        (Email(), "email.domain.com", False),
        (Email(), "email@domain@domain.com", False),
        (Email(), ".email@domain.com", False),
        (Email(), "email.@domain.com", False),
        (Email(), "email..email@domain.com", False),
        #(Email(), "あいうえお@domain.com", False), # Should not be allowed (unicode username), but currently is
        (Email(), "email@domain.com (Joe Smith)", False),
        (Email(), "email@domain", False),
        #(Email(), "email@-domain.com", False), # Should not be allowed (invalid domain name), but currently is
        #(Email(), "email@domain.web", False), # Should not be allowed (invalid top level domain), but currently is
        (Email(), "email@111.222.333.44444", False),
        (Email(), "email@domain..com", False),


        (OneOf([1, '2', 3.0]), 1, True),
        (OneOf([1, '2', 3.0]), '2', True),
        (OneOf([1, '2', 3.0]), 3.0, True),
        (OneOf([1, '2', 3.0]), '1', False),
        (OneOf([1, '2', 3.0]), 2, False),
        (OneOf({1, '2', 3.0}), 1, True),
        (OneOf({1, '2', 3.0}), '2', True),
        (OneOf({1, '2', 3.0}), 3.0, True),
        (OneOf({1, '2', 3.0}), '1', False),
        (OneOf({1, '2', 3.0}), 2, False),

        (Unicode(), 'not unicöde', False),
        (Unicode(), u'not unicöde', True),
        (Unicode(), unicode('not unicode'), True),

    ]

    for case in cases:
        yield (assert_value_validator,) + case
