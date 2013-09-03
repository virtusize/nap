# -*- coding: utf-8 -*-

import sys

from fixture import DataSet
from fixture import SQLAlchemyFixture, TrimmedNameStyle

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Integer, String

from core.database import SAModel, Field
from core.validation.validators import NotNone, Email
from tests.helpers import engine


class Stores(DataSet):
    class virtusize:
        id = 1
        name = 'Virtusize Demo Store'
        short_name = 'virtusize'
        api_key = 'asdf1234'


class Users(DataSet):

    class john:
        id = 1
        name = 'John'
        email = 'john@virtusize.com'
        store = Stores.virtusize

    class jane:
        id = 2
        name = 'jane'
        email = 'jane@virtusize.com'
        store = Stores.virtusize


class Store(SAModel):

    id = Field(Integer, primary_key=True)
    name = Field(String)
    short_name = Field(String)
    api_key = Field(String)


class User(SAModel):

    id = Field(Integer, primary_key=True)
    name = Field(String, validate_with=[NotNone()])
    email = Field(String, validate_with=[NotNone(), Email])
    store_id = Field(Integer, ForeignKey('stores.id'), nullable=True)

    store = relationship(Store, backref=backref('users'))


current_module = sys.modules[__name__]
fixture_loader = SQLAlchemyFixture(env=current_module, style=TrimmedNameStyle(suffix='s'), engine=engine)
