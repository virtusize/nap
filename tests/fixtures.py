# -*- coding: utf-8 -*-

import sys

from fixture import DataSet
from fixture import SQLAlchemyFixture, TrimmedNameStyle

from sqlalchemy import Integer, String

from core.database import DbModel, engine, Field
from core.validation.validators import NotNone


class Stores(DataSet):
    class virtusize:
        name = 'Virtusize Demo Store'
        short_name = 'virtusize'


class Users(DataSet):
    class invalid_john:
        id = 1
        name = 'Invalid John'

    class john:
        id = 2
        name = 'John'
        email = 'john@virtusize.com'

    class jane:
        id = 3
        name = 'jane'
        email = 'jane@virtusize.com'


class Store(DbModel):

    id = Field(Integer, primary_key=True)
    name = Field(String)
    short_name = Field(String)


class User(DbModel):

    id = Field(Integer, primary_key=True)
    name = Field(String, validate_with=[NotNone()])
    email = Field(String, validate_with=[NotNone])


current_module = sys.modules[__name__]
db_fixture = SQLAlchemyFixture(env=current_module, style=TrimmedNameStyle(suffix='s'), engine=engine)
