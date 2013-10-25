# -*- coding: utf-8 -*-
from sqlalchemy import types
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from nap.validation import ValueValidator
from nap.validators import EnsureMaxLength, EnsureNotNone, EnsureType


class EnsureUnique(ValueValidator):

    def validate(self, model_instance, field_name, value):
        db_session = model_instance.get_session()
        try:
            existing = db_session.query(type(model_instance)).filter_by(**{field_name: value}).one()

            if existing == model_instance:
                return []

        except NoResultFound:
            return []
        except MultipleResultsFound:
            pass

        return ['Field "{field}" must be unique. "{value}" already exists.'.format(field=field_name, value=value)]


class SQLConstraintsValidator(ValueValidator):

    def __init__(self, field):
        self.validators = []
        if field.primary_key or field.default:
            return

        if isinstance(field.type, types.String) and field.type.length:
            self.validators.append(EnsureMaxLength(field.type.length))

        if not field.nullable:
            self.validators.append(EnsureNotNone())

        if field.unique:
            self.validators.append(EnsureUnique())

        if isinstance(field.type, (types.Unicode, types.UnicodeText)):
            self.validators.append(EnsureType(unicode))

    def validate(self, model_instance, field_name, value):
        errors = []
        for v in self.validators:
            errors.extend(v.validate(model_instance, field_name, value))
        return errors
