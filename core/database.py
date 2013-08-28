# -*- coding: utf-8 -*-
import re

from sqlalchemy import create_engine, event, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from core.model import Model
from core.validation import ValidationContext, ValidationMixin, ValueValidator
from core.validation.validators import FieldValidator


engine = create_engine('sqlite:///:memory:', echo=True)


class SQLConstraintsValidator(ValueValidator):

    def __init__(self, field):
        pass

    def validate(self, model_instance, field_name, value):
        return []

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


class Field(Column):
    """
    This is a extention for Column type that allows us to pass in a list of validator classes
    to validate against.
    Example:
        name = Field(String, validate_constraints=True, validate_with=[EnsureNotNull])

    The validate_constrains keywords adds the SQLConstraintsValidator class to the
    validate_with array.
    """
    def __init__(self, *args, **kwargs):
        validator_list = []
        validator_list.extend(kwargs.pop('validate_with', []))

        info = kwargs.get('info', {})
        info['_validator_list'] = validator_list
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

DbModel = declarative_base(cls=DbModel)

db_session = scoped_session(sessionmaker(bind=engine))
