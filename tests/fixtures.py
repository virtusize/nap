# -*- coding: utf-8 -*-

import sys

from fixture import DataSet
from fixture import SQLAlchemyFixture, TrimmedNameStyle

from sqlalchemy import Column, Integer, String

from core.database import DbModel, engine
from core.validation import NotEmptyValidator


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

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)


class User(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    _validate_with = [NotEmptyValidator('name'), NotEmptyValidator('email')]


current_module = sys.modules[__name__]
db_fixture = SQLAlchemyFixture(env=current_module, style=TrimmedNameStyle(suffix='s'), engine=engine)
