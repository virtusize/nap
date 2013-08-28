# -*- coding: utf-8 -*-


class ModelValidator(object):

    def validate(self, model_instance):
        raise NotImplementedError


class ValueValidator(object):

    def validate(self, model_instance, field_name, value):
        raise NotImplementedError


class ValidationContext(object):

    def __init__(self, validators):
        self.validators = validators

    def validate(self, model_instance):

        _errors = []
        for validator in self.validators:
            if isinstance(validator, ModelValidator):
                errors = validator.validate(model_instance)
                _errors.extend(errors)

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


