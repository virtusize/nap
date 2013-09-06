# -*- coding: utf-8 -*-
import os


class ModelValidator(object):
    """
    ModelValidator is an abstract class for validators that validate entire
    model instances. Any validator that acts on the full instance will need
    to subclass ModelValidator

    Example of this can be a ConfirmFieldValidator that ensures that two fields
    are the same. BTW, this is a really bad example as this should be on the
    form level and not in the model.
    """

    def validate(self, model_instance):
        raise NotImplementedError


class ValueValidator(object):
    """
    ValueValidator validates just a single value from a model.
    Example subclasses are NotNone, MaxLength, ValidEmail, etc...
    """
    def validate(self, model_instance, field_name, value):
        raise NotImplementedError


class ValidationContext(object):

    def __init__(self, validators):
        self.validators = validators

    def validate(self, model_instance, raise_on_error):

        _errors = []
        for validator in self.validators:
            if isinstance(validator, ModelValidator):
                errors = validator.validate(model_instance)
                _errors.extend(errors)

        if _errors and raise_on_error:
            raise ValueError(os.linesep.join(_errors))

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
        return  'ValidationResult: %s ' % self.valid + os.linesep +\
                'Errors:' + os.linesep +\
                os.linesep.join(self.errors)


class ValidationMetaClass(type):

    def __new__(mcs, classname, bases, dct):

        if '_validate_with' in dct:
            validator_list = dct.pop('_validate_with')
            dct['_validation_context'] = ValidationContext(validators=validator_list)
        return super(ValidationMetaClass, mcs).__new__(mcs, classname, bases, dct)


class ValidationMixin(object):

    def validate(self, raise_on_error=False):
        if hasattr(self.__class__, '_validation_context'):
            return self.__class__._validation_context.validate(self, raise_on_error=raise_on_error)

        return ValidationResult([])


