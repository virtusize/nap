# -*- coding: utf-8 -*-

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

Required = NotNone


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
