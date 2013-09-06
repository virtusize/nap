# -*- coding: utf-8 -*-

from inflection import underscore, pluralize
from sqlalchemy import event, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import mapper
from nap.model import BaseModel, BaseSerializer
from nap.validation import ValidationContext, ValidationMixin
from nap.validation.validators import FieldValidator
from sa_nap.validators import SQLConstraintsValidator


class Field(Column):
    """
    This is a extension for Column type that allows us to pass in a list of validator classes
    to validate against.
    Example:
        name = Field(String, validate_constraints=True, validate_with=[EnsureNotNone])
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
