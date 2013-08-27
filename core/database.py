# -*- coding: utf-8 -*-
import re

from sqlalchemy import create_engine, event, Column
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from core.model import Model
from core.validation import ValidationContext, ValidationMixin, FieldValidator


engine = create_engine('sqlite:///:memory:', echo=True)


@event.listens_for(mapper, 'mapper_configured')
def mapper_configured(mapper_ins, cls):
    """
    This callback is called for each declarative class we define and
    it instruments each class by creating and setting a _validation_context
    property on the class.

    The validators are harvested from Field instances and _validate_with
    property on the class.
    """
    validator_list = []

    for field in mapper_ins._columntoproperty.keys():
        if not isinstance(field, Field):
            continue

        field_validator_class_list = field.info.pop('_validation_class_list', [])
        field_validator_list = [FieldValidatorFactory.create_validator(validator_class, field.name, field)
                                for validator_class in field_validator_class_list]
        validator_list.extend(field_validator_list)

    if hasattr(cls, '_validate_with'):
        validator_list.extend(cls._validate_with)
        del cls._validate_with

    validation_context = getattr(cls, '_validation_context', ValidationContext([]))
    validation_context.validators.extend(validator_list)

    setattr(cls, '_validation_context', validation_context)


class SQLConstrainsValidator(FieldValidator):
    """
    TODO: Create a validator that based on the field_instance,
    but it should not have a reference to the field, will create a memory leak.
    """
    def validate(self, instance):
        return True, 'message'


class FieldValidatorFactory(object):

    @staticmethod
    def create_validator(validator_class, field_name, field_instance):
        """
        Given a validator_class, return an instance of the validator,
        with the field_name set to the name of the field.
        But make sure the class is a FieldValidator subclass.
        """
        assert issubclass(validator_class, FieldValidator)

        return validator_class(field_name, field_instance=field_instance)


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
        validation_class_list = []
        validation_class_list.extend(kwargs.pop('validate_with', []))

        if kwargs.pop('validate_constraints', False):
            validation_class_list.append(SQLConstrainsValidator)
        info = kwargs.get('info', {})
        info['_validation_class_list'] = validation_class_list

        kwargs['info'] = info

        super(Field, self).__init__(*args, **kwargs)


# class DeclarativeValidationMetaClass(DeclarativeMeta):
# 
#     def __new__(mcs, classname, bases, dct):
# 
#         if '_validate_with' in dct:
#             validator_list = dct.pop('_validate_with')
#             dct['_validation_context'] = ValidationContext(validators=validator_list)
#         return super(DeclarativeValidationMetaClass, mcs).__new__(mcs, classname, bases, dct)


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
