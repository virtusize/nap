# -*- coding: utf-8 -*-
import re

from sqlalchemy import create_engine, event, types, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from core.model import Model
from core.validation import ValidationContext, ValidationMixin, ValueValidator
from core.validation.validators import FieldValidator, MaxLength, NotNone, IsType


engine = create_engine('sqlite:///:memory:', echo=True)


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


class DbModel(Model, ValidationMixin):
    """
    Base class for DB Models
    """
    @declared_attr
    def __tablename__(cls):
        """
        Convert CamelCase class name to underscores_between_words (plural) table name.
        """
        name = cls.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: "_" + m.group(0).lower(), name[1:]) + 's'
        )

    def to_dict(self):
        return {k: v for k, v in self.__dict__.iteritems() if k != '_sa_instance_state'}


DbModel = declarative_base(cls=DbModel)

db_session = scoped_session(sessionmaker(bind=engine))
