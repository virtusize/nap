# -*- coding: utf-8 -*-

from flask.json import JSONEncoder, JSONDecoder

from inflection import underscore, pluralize
from sqlalchemy import event, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import mapper
from sqlalchemy.types import TypeDecorator, Text
from nap.model import BaseModel, Model, BaseSerializer, ModelSerializer
from nap.validation import ValidationContext, ValidationMixin
from nap.validators import FieldValidator
from sa_nap.validators import SQLConstraintsValidator


class NoSessionBound(Exception):
    pass


class Field(Column):
    """
    This is a extension for Column type that allows us to pass in a list of validator classes
    to validate against.
    Example:
        name = Field(String, validate_with=[EnsureNotNone])
    """
    def __init__(self, *args, **kwargs):

        info = kwargs.get('info', {})
        info['_validator_list'] = kwargs.pop('validate_with', [])
        info['_validate_constraints'] = kwargs.pop('validate_constraints', True)
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

    @classmethod
    def get_session(cls):
        if hasattr(cls, '__db_session__') and cls.__db_session__:
            return cls.__db_session__
        raise NoSessionBound('No session bound to SAModel, bind it with SAModel.__db_session__ = db_session')

SAModel = declarative_base(cls=SAModel)


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


class SAModelSerializer(BaseSerializer):

    def serialize(self, subject):
        return {c.name: getattr(subject, c.name) for c in subject.__table__.columns}


class ModelJSON(TypeDecorator):
    impl = Text
    serializer = ModelSerializer()

    def __init__(self, model_class):
        super(ModelJSON, self).__init__()
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = JSONEncoder().encode(self.serializer.serialize(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.model_class(**JSONDecoder().decode(value))
        return value


class FieldModel(Model, Mutable):
    """ Mutable base class """
    @classmethod
    def coerce(cls, key, value):
        return value

    def __setattr__(self, name, value):
        Model.__setattr__(self, name, value)
        self.changed()

FieldModel.associate_with(ModelJSON)
