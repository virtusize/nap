# -*- coding: utf-8 -*-
from nap.exceptions import ModelNotFoundException, ModelInvalidException
from nap.authorization import Guard
from sa_nap.controller import SAModelController
from tests.fixtures import Users, User, Stores, Store, Products, Product, fixture_loader
from tests.helpers import *


class UserController(SAModelController):
    model = User
    session_factory = db_session


class StoreController(SAModelController):
    model = Store
    session_factory = db_session


class ProductController(SAModelController):
    model = Product
    session_factory = db_session


def test_controller():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = UserController()

        user = c.read(1)
        assert_is_not_none(user)

        email = 'somebody@example.com'
        c.update(user.id, {'email': email})

        user = c.read(1)
        compare(user.email, email)

        user = c.create({'name': u'Anybody', 'email': 'anybody@example.com', 'password': '123456'})
        assert_is_not_none(user)
        compare(c.read(user.id), user)
        compare(user.name, 'Anybody')


@raises(ModelNotFoundException)
def test_controller_delete():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = UserController()

        c.delete(Users.john.id)
        c.read(Users.john.id)


@raises(ModelInvalidException)
def test_unique_validator_by_db_insert_same_commit():
    with db():
        c = UserController()
        c.create({'name': u'Joe', 'email': 'valid@example.com', 'password': '123456'})
        c.create({'name': u'Other Joe', 'email': 'valid@example.com', 'password': '123456'})
