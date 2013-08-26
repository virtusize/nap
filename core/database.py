#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declared_attr, declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from core.model import Model
from core.validation import ValidationContext, ValidationMixin


engine = create_engine('sqlite:///:memory:', echo=True)


@event.listens_for(mapper, 'mapper_configured')
def mapper_configured(mapper_ins, cls):
    print str(cls)


class ValidationMetaClass(DeclarativeMeta):

    def __new__(mcs, classname, bases, dct):

        if '_validate_with' in dct:
            validator_list = dct.pop('_validate_with')
            dct['_validation_context'] = ValidationContext(validators=validator_list)
        print classname + ' is created'
        return super(ValidationMetaClass, mcs).__new__(mcs, classname, bases, dct)



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

DbModel = declarative_base(cls=DbModel, metaclass=ValidationMetaClass)

db_session = scoped_session(sessionmaker(bind=engine))
