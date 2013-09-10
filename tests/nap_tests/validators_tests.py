# -*- coding: utf-8 -*-

import re

from nap.validation import ValidationResult
from tests.helpers import *

from nap.validators import *


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


def test_field_validator():
    class SomeModel(object):
        pass

    sm = SomeModel()
    sm.some_field = 'some_value'

    fv = FieldValidator('some_field')

    assert_true(fv.has_field(sm))
    compare(fv.get_field(sm), 'some_value')

    fv.set_field(sm, 'another_value')
    compare(fv.get_field(sm), 'another_value')

    fv = FieldValidator('another_field')
    result = fv.validate(sm)

    assert_false(fv.has_field(sm))
    assert_is_instance(result, list)
    assert_equal(len(result), 1)
    compare(result[0], 'Model SomeModel is missing field another_field')


def test_value_validators():
    cases = [
        (EnsureNone(), None, True),
        (EnsureNone(), '', False),

        (EnsureNotNone(), None, False),
        (EnsureNotNone(), '', True),

        (EnsureMaxLength(100), True, False),
        (EnsureMaxLength(0), '', True),
        (EnsureMaxLength(1), '', True),
        (EnsureMaxLength(2), '', True),
        (EnsureMaxLength(2), '_' * 3, False),

        (EnsureMinLength(100), True, False),
        (EnsureMinLength(2), '_' * 3, True),
        (EnsureMinLength(2), '_' * 2, True),
        (EnsureMinLength(2), '_', False),
        (EnsureMinLength(2), '', False),

        (EnsureType(str), '', True),
        (EnsureType(str), u'', False),
        (EnsureType(bool), '', False),
        (EnsureType(unicode), '', False),
        (EnsureType(unicode), u'', True),
        (EnsureType(basestring), '', True),
        (EnsureType(basestring), u'', True),

        (EnsureInt(), '', False),
        (EnsureInt(), u'', False),
        (EnsureInt(), '10', False),
        (EnsureInt(), u'10', False),
        (EnsureInt(), 10, True),
        (EnsureInt(min=11), 10, False),
        (EnsureInt(max=9), 10, False),
        (EnsureInt(min=1, max=9), 7, True),
        (EnsureInt(min=1, max=9), 1, True),
        (EnsureInt(min=1, max=9), 9, True),

        (EnsureNotEmpty(), '_', True),
        (EnsureNotEmpty(), None, False),
        (EnsureNotEmpty(), '', False),
        (EnsureNotEmpty(), 1123, True),
        (EnsureNotEmpty(), ' ', True),
        (EnsureNotEmpty(), 0, True),
        (EnsureNotEmpty(), [], False),
        (EnsureNotEmpty(), ["_"], True),
        (EnsureNotEmpty(), {}, False),
        (EnsureNotEmpty(), {1: '_'}, True),
        (EnsureNotEmpty(), False, True),
        (EnsureNotEmpty(), True, True),

        (EnsureRegex(re.compile(r"^[a-z]*$")), "abc", True),
        (EnsureRegex(r"^[a-z]*$"), "aBc", False),
        (EnsureRegex(r"^[\d]*$"), "123", True),
        (EnsureRegex(r"^[\d]*$"), "abc", False),
        (EnsureRegex(r"^[a-z]*$"), "abc", True),
        (EnsureRegex(r"^[a-z]*$"), "aBc", False),

        (EnsurePlainText(), "aB12-Xy_Z", True),
        (EnsurePlainText(), "!", False),
        (EnsurePlainText(), "ab$12", False),

        (EnsureEmail(), "hannes@virtusize.com", True),
        (EnsureEmail(), "hannes+a@virtusize.com", True),
        (EnsureEmail(), "hannes+a+11@virtusize.com", True),
        (EnsureEmail(), "hannes@virt@usize.com", False),
        (EnsureEmail(), " hannes@virtusize.com", False),
        (EnsureEmail(), "hannes@virtusize.com ", False),
        (EnsureEmail(), "hannes@virt usize.com ", False),
        (EnsureEmail(), "hannesvirtusize.com", False),

        (EnsureEmail(), "email@domain.com", True),
        (EnsureEmail(), "firstname.lastname@domain.com", True),
        (EnsureEmail(), "email@subdomain.domain.com", True),
        (EnsureEmail(), "firstname+lastname@domain.com", True),
        #(EnsureEmail(), "email@123.123.123.123", True), # Should be a valid address, but fails with our regex
        (EnsureEmail(), "email@[123.123.123.123]", True),
        (EnsureEmail(), "\"email\"@domain.com", True),
        (EnsureEmail(), "1234567890@domain.com", True),
        (EnsureEmail(), "email@domain-one.com", True),
        (EnsureEmail(), "_______@domain.com", True),
        (EnsureEmail(), "email@domain.name", True),
        (EnsureEmail(), "email@domain.co.jp", True),
        (EnsureEmail(), "firstname-lastname@domain.com", True),

        (EnsureEmail(), "plainaddress", False),
        (EnsureEmail(), "#@%^%#$@#$@#.com", False),
        (EnsureEmail(), "@domain.com", False),
        (EnsureEmail(), "Joe Smith <email@domain.com>", False),
        (EnsureEmail(), "email.domain.com", False),
        (EnsureEmail(), "email@domain@domain.com", False),
        (EnsureEmail(), ".email@domain.com", False),
        (EnsureEmail(), "email.@domain.com", False),
        (EnsureEmail(), "email..email@domain.com", False),
        #(EnsureEmail(), "あいうえお@domain.com", False), # Should not be allowed (unicode username), but currently is
        (EnsureEmail(), "email@domain.com (Joe Smith)", False),
        (EnsureEmail(), "email@domain", False),
        #(EnsureEmail(), "email@-domain.com", False), # Should not be allowed (invalid domain name), but currently is
        #(EnsureEmail(), "email@domain.web", False), # Should not be allowed (invalid top level domain), but currently is
        (EnsureEmail(), "email@111.222.333.44444", False),
        (EnsureEmail(), "email@domain..com", False),


        (EnsureOneOf([1, '2', 3.0]), 1, True),
        (EnsureOneOf([1, '2', 3.0]), '2', True),
        (EnsureOneOf([1, '2', 3.0]), 3.0, True),
        (EnsureOneOf([1, '2', 3.0]), '1', False),
        (EnsureOneOf([1, '2', 3.0]), 2, False),
        (EnsureOneOf({1, '2', 3.0}), 1, True),
        (EnsureOneOf({1, '2', 3.0}), '2', True),
        (EnsureOneOf({1, '2', 3.0}), 3.0, True),
        (EnsureOneOf({1, '2', 3.0}), '1', False),
        (EnsureOneOf({1, '2', 3.0}), 2, False),

        (EnsureUnicode(), 'not unicöde', False),
        (EnsureUnicode(), u'not unicöde', True),
        (EnsureUnicode(), unicode('not unicode'), True),

    ]

    for case in cases:
        yield (assert_value_validator,) + case
