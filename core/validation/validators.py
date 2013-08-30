# -*- coding: utf-8 -*-

import re

from core.validation import ModelValidator, ValueValidator


class FieldValidator(ModelValidator):

    def __init__(self, field_name, *validator_or_class_list):
        self.field_name = field_name
        self.value_validators = []

        for validator in validator_or_class_list:
            if isinstance(validator, ValueValidator):
                self.value_validators.append(validator)
            if isinstance(validator, type) and issubclass(validator, ValueValidator):
                self.value_validators.append(validator())

    def get_field(self, model_instance):
        return getattr(model_instance, self.field_name)

    def set_field(self, model_instance, value):
        return setattr(model_instance, self.field_name, value)

    def has_field(self, model_instance):
        return hasattr(model_instance, self.field_name)

    def validate(self, model_instance):
        if not self.has_field(model_instance):
            return ['Model {model} is missing field {field_name}'.format(model=model_instance,
                                                                         field_name=self.field_name)]
        _value_errors = []
        for validator in self.value_validators:
            _value_errors.extend(
                validator.validate(model_instance, self.field_name, self.get_field(model_instance))
            )
        return _value_errors


class IsNone(ValueValidator):

    def validate(self, model_instance, field_name, value):
        if not value is None:
            return ['Field {field} must be None'.format(field=field_name)]
        return []


class NotNone(ValueValidator):

    def validate(self, model_instance, field_name, value):
        if value is None:
            return ['Field {field} is not allowed to be None'.format(field=field_name)]
        return []


class NotEmpty(ValueValidator):

    def validate(self, model_instance, field_name, value):
        if value != 0 and not value:
            return ['Field {field} is not allowed to be empty'.format(field=field_name)]

        return []

Required = NotEmpty


class MaxLength(ValueValidator):

    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self, model_instance, field_name, value):
        try:
            length = len(value)
        except:  # TypeError
            return ['Field {field} does not have a length'.format(field=field_name)]

        if length > self.max_length:
            return ['Field {field} is longer than {max_length}'.format(field=field_name, max_length=self.max_length)]

        return []


class MinLength(ValueValidator):

    def __init__(self, min_length):
        self.min_length = min_length

    def validate(self, model_instance, field_name, value):
        try:
            length = len(value)
        except:  # TypeError
            return ['Field {field} does not have a length'.format(field=field_name)]

        if length < self.min_length:
            return ['Field {field} is shorter than {min_length}'.format(field=field_name, min_length=self.min_length)]

        return []


class IsType(ValueValidator):

    def __init__(self, typ):
        self.typ = typ

    def validate(self, model_instance, field_name, value):
        if not isinstance(value, self.typ):
            return ['Field {field} is not of type {type}'.format(field=field_name, type=self.typ)]
        return []

OfType = IsType


class Int(ValueValidator):

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def validate(self, model_instance, field_name, value):
        if not isinstance(value, int):
            return ['Field {field} is not an integer value'.format(field=field_name)]

        errors = []
        if not self.min is None and value < self.min:
            errors.append('Field {field} must be equal or larger than {min}'.format(field=field_name, min=self.min))

        if not self.max is None and value > self.max:
            errors.append('Field {field} must be equal or smaller than {max}'.format(field=field_name, max=self.max))

        return errors


class Regex(ValueValidator):
    
    message = 'Field {field} does not match'

    def __init__(self, regex):
        self.regex = regex if not isinstance(regex, basestring) else re.compile(regex)

    def validate(self, model_instance, field_name, value):
        if value is not None and not self.regex.search(value):
            return [self.message.format(field=field_name)]
        return []


class PlainText(Regex):

    message = 'Field {field} can only contain letters, numbers, underscores and dashes'

    def __init__(self):
        super(self.__class__, self).__init__(r"^[a-zA-Z_\-0-9]*$")


class Email(Regex):

    message = 'Field {field} is not a valid email'

    def __init__(self):
        # Pattern from http://stackoverflow.com/questions/46155/validate-email-address-in-javascript
        # See the pattern visually at http://www.regexper.com
        
        regex = re.compile(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-z\-0-9]+\.)+[a-z]{2,}))$", re.IGNORECASE)

        super(self.__class__, self).__init__(regex)
