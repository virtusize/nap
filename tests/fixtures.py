# -*- coding: utf-8 -*-

import sys

from fixture import DataSet
from fixture import SQLAlchemyFixture, TrimmedNameStyle
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Integer, String, Unicode

from nap.model import Model, Storage
from nap.validators import *
from sa_nap import SAModel
from sa_nap.model import Field
from tests.helpers import engine


class ProductType(Model):

    _validate_with = [
        FieldValidator('id', EnsureNotEmpty, EnsureInt),
        FieldValidator('name', EnsureNotEmpty, Unicode)
    ]


class ProductTypes(Storage):
    dress = ProductType(id=1, name='dress')
    shirt = ProductType(id=2, name='shirt')
    pants = ProductType(id=3, name='pants')


class Users(DataSet):

    class john:
        id = 1
        name = u'John'
        email = 'john@virtusize.com'
        password = '123456'

    class jane:
        id = 2
        name = u'jane'
        email = 'jane@virtusize.com'
        password = '123456'


class Stores(DataSet):

    class virtusize:
        id = 1
        name = u'Virtusize Demo Store'
        owner = Users.john

    class asos:
        id = 2
        name = u'Asos'
        owner = Users.john

    class wesc:
        id = 3
        name = u'WeSC'
        owner = Users.jane


class Products(DataSet):

    class dress:
        id = 1
        name = u'Black dress'
        store = Stores.virtusize
        product_type_id = ProductTypes.dress.id


class User(SAModel):

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(255), validate_constraints=True, validate_with=[EnsureMinLength(3), EnsureNotEmpty()])
    email = Field(String(255), validate_constraints=True, validate_with=[EnsureNotEmpty, EnsureEmail])
    password = Field(String(255), validate_constraints=True, validate_with=[EnsureNotEmpty])


class Store(SAModel):

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(255), validate_constraints=True, validate_with=[EnsureMinLength(3), EnsureNotEmpty])
    owner_id = Field(Integer, ForeignKey('users.id'), nullable=False, validate_constraints=True)

    owner = relationship(User, backref='stores')


class Product(SAModel):
    id = Field(Integer, primary_key=True)
    name = Field(Unicode(255), validate_constraints=True, validate_with=[EnsureMinLength(3), EnsureNotEmpty])
    store_id = Field(Integer, ForeignKey('stores.id'), nullable=False)
    product_type_id = Field(Integer, validate_constraints=True, validate_with=[EnsureOneOf(ProductTypes._pluck())])

    store = relationship(Store, backref='products')

    @property
    def product_type(self):
        return ProductTypes._get(self.product_type_id)


current_module = sys.modules[__name__]
fixture_loader = SQLAlchemyFixture(env=current_module, style=TrimmedNameStyle(suffix='s'), engine=engine)
