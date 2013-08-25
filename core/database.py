#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from core.model import Model


engine = create_engine('sqlite:///:memory:', echo=True)


class DbModel(Model):
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