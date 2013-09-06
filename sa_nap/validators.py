# -*- coding: utf-8 -*-
from sqlalchemy import types
from nap.validation import ValueValidator
from nap.validation.validators import EnsureMaxLength, EnsureNotNone, EnsureType


class SQLConstraintsValidator(ValueValidator):

    def __init__(self, field):
        self.validators = []
        if field.primary_key:
            return

        if isinstance(field.type, types.String) and field.type.length:
            self.validators.append(EnsureMaxLength(field.type.length))

        if not field.nullable:
            self.validators.append(EnsureNotNone())

        if isinstance(field.type, (types.Unicode, types.UnicodeText)):
            self.validators.append(EnsureType(unicode))

    def validate(self, model_instance, field_name, value):
        errors = []
        for v in self.validators:
            errors.extend(v.validate(model_instance, field_name, value))
        return errors
