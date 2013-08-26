# -*- coding: utf-8 -*-


class ValidationContext(object):

    def __init__(self, validators):
        self.validators = validators

    def validate(self, instance):

        _errors = []
        for validator in self.validators:
            try:
                validator.validate_and_raise(instance)
            except ValueError as error:
                _errors.append(error.message)

        return ValidationResult(_errors)


class ValidationResult(object):

    def __init__(self, errors):
        self.errors = errors

    @property
    def valid(self):
        return not self.errors

    def __nonzero__(self):
        return self.valid

    def __repr__(self):
        return "ValidationResult: %s " % self.valid


class ValidationMetaClass(type):

    def __new__(mcs, classname, bases, dct):

        if '_validate_with' in dct:
            validator_list = dct.pop('_validate_with')
            dct['_validation_context'] = ValidationContext(validators=validator_list)
        return super(ValidationMetaClass, mcs).__new__(mcs, classname, bases, dct)


class ValidationMixin(object):

    def validate(self):
        if hasattr(self.__class__, '_validation_context'):
            return self.__class__._validation_context.validate(self)

        return ValidationResult([])


### Validators


class BaseValidator(object):

    def validate(self, instance):
        raise NotImplementedError

    def validate_and_raise(self, instance):
        result, message = self.validate(instance)
        if not result:
            raise ValueError(message)


class FieldValidator(BaseValidator):

    def __init__(self, field):
        self.field = field

    def get_field(self, instance):
        return getattr(instance, self.field)

    def set_field(self, instance, value):
        return setattr(instance, self.field, value)

    def has_field(self, instance):
        return hasattr(instance, self.field)


class NotEmptyValidator(FieldValidator):

    def validate(self, instance):
        return self.has_field(instance) and not self.get_field(instance) is None,\
            'Required field %s is not present' % self.field


class EqualValidator(BaseValidator):

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def validate(self, instance):
        return getattr(instance, self.field1) == getattr(instance, self.field2),\
            'Model %s is not equal to %s' % (self.field1, self.field2)
