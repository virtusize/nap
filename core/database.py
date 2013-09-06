# -*- coding: utf-8 -*-
import re

from inflection import underscore, pluralize
from sqlalchemy import create_engine, event, types, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from core.model import BaseModel, BaseSerializer
from core.model.controller import BaseController
from core.validation import ValidationContext, ValidationMixin, ValueValidator
from core.validation.validators import FieldValidator, MaxLength, NotNone, IsType


class SQLConstraintsValidator(ValueValidator):

    def __init__(self, field):
        self.validators = []
        if field.primary_key:
            return

        if isinstance(field.type, types.String) and field.type.length:
            self.validators.append(MaxLength(field.type.length))

        if not field.nullable:
            self.validators.append(NotNone())

        if isinstance(field.type, (types.Unicode, types.UnicodeText)):
            self.validators.append(IsType(unicode))

    def validate(self, model_instance, field_name, value):
        errors = []
        for v in self.validators:
            errors.extend(v.validate(model_instance, field_name, value))
        return errors


@event.listens_for(mapper, 'mapper_configured')
def mapper_configured(mapper_ins, cls):
    """
    """
    validator_list = []

    for field in mapper_ins._columntoproperty.keys():
        if not isinstance(field, Field):
            continue

        value_validator_list = []
        if field.info.pop('_validate_constraints', False):
            value_validator_list.append(SQLConstraintsValidator(field))

        value_validator_list.extend(field.info.pop('_validator_list', []))
        if value_validator_list:
            validator_list.append(FieldValidator(field.name, *value_validator_list))

    if hasattr(cls, '_validate_with'):
        validator_list.extend(cls._validate_with)
        del cls._validate_with

    validation_context = getattr(cls, '_validation_context', ValidationContext([]))
    validation_context.validators.extend(validator_list)

    setattr(cls, '_validation_context', validation_context)

    @event.listens_for(cls, 'before_insert')
    @event.listens_for(cls, 'before_update')
    def validate_model(mapper, connection, model_instance):
        if isinstance(model_instance, ValidationMixin):
            model_instance.validate(raise_on_error=True)


class Field(Column):
    """
    This is a extension for Column type that allows us to pass in a list of validator classes
    to validate against.
    Example:
        name = Field(String, validate_constraints=True, validate_with=[NotNone])
    """
    def __init__(self, *args, **kwargs):

        info = kwargs.get('info', {})
        info['_validator_list'] = kwargs.pop('validate_with', [])
        info['_validate_constraints'] = kwargs.pop('validate_constraints', False)
        kwargs['info'] = info

        super(Field, self).__init__(*args, **kwargs)


class SAModel(BaseModel):
    """
    Base class for SqlAlchemy Models
    """
    @declared_attr
    def __tablename__(cls):
        return underscore(pluralize(cls.__name__))

    def update_attributes(self, attributes):
        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)


SAModel = declarative_base(cls=SAModel)


class SAModelSerializer(BaseSerializer):

    def serialize(self, subject):
        return {c.name: getattr(subject, c.name) for c in subject.__table__.columns}


class SAModelController(BaseController):

    def __init__(self, model, session_factory):
        self.model = model
        self.session_factory = session_factory

    @property
    def db_session(self):
        return self.session_factory()

    def index(self, context=None):
        return self.db_session.query(self.model)

    def read(self, id, context=None):
        return self._get_model(id)

    def create(self, attributes, context=None):
        model = self.model(**attributes)
        self.db_session.add(model)
        self.db_session.commit()
        return model

    def update(self, id, attributes, context=None):
        model = self._get_model(id)
        model.update_attributes(attributes)
        self.db_session.commit()
        return model

    def delete(self, id, context=None):
        model = self._get_model(id)
        self.db_session.delete(model)
        self.db_session.commit()
        return model

    def _get_model(self, id):
        return self.db_session.query(self.model).get(id)

